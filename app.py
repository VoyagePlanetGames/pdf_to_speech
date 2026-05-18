"""
Day 91 — Flask web app for the PDF-to-Speech audiobook tool.

Run locally:
    pip install -r requirements.txt
    python app.py
    → open http://127.0.0.1:5000

Reuses extract_text() and synthesise_gtts() from pdf_to_speech.py.
"""

from __future__ import annotations

import io
import os
import tempfile
import uuid
from pathlib import Path

from flask import (
    Flask, render_template, request, send_file, abort, jsonify, url_for
)

from pdf_to_speech import extract_text, synthesise_gtts, synthesise_offline

# ---------- Config -----------------------------------------------------------

MAX_UPLOAD_MB = 25
ALLOWED_EXT = {".pdf"}
JOB_DIR = Path(tempfile.gettempdir()) / "pdf2speech_jobs"
JOB_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024


# ---------- Routes -----------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", max_mb=MAX_UPLOAD_MB)


@app.route("/convert", methods=["POST"])
def convert():
    """Accept a PDF upload, return JSON with the download URL of the MP3."""
    file = request.files.get("pdf")
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded."}), 400

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": "Please upload a .pdf file."}), 400

    engine = request.form.get("engine", "gtts")
    lang = request.form.get("lang", "en")
    start = _to_int(request.form.get("start"))
    end = _to_int(request.form.get("end"))

    # Save the upload to a per-job folder
    job_id = uuid.uuid4().hex[:12]
    job_path = JOB_DIR / job_id
    job_path.mkdir()
    pdf_path = job_path / "input.pdf"
    file.save(pdf_path)

    try:
        text = extract_text(pdf_path, start, end)
    except SystemExit as e:
        return jsonify({"error": str(e)}), 400

    mp3_path = job_path / "audiobook.mp3"
    try:
        if engine == "offline":
            synthesise_offline(text, mp3_path)
        else:
            synthesise_gtts(text, lang, mp3_path)
    except Exception as e:  # network errors, gTTS rate limits, etc.
        return jsonify({"error": f"TTS failed: {e}"}), 500

    return jsonify({
        "download_url": url_for("download", job_id=job_id),
        "char_count": len(text),
        "size_kb": round(mp3_path.stat().st_size / 1024, 1),
    })


@app.route("/download/<job_id>")
def download(job_id: str):
    safe = "".join(c for c in job_id if c.isalnum())
    mp3 = JOB_DIR / safe / "audiobook.mp3"
    if not mp3.exists():
        abort(404)
    return send_file(mp3, as_attachment=True, download_name="audiobook.mp3")


@app.errorhandler(413)
def too_large(_e):
    return jsonify({"error": f"File too large. Max {MAX_UPLOAD_MB} MB."}), 413


# ---------- Helpers ----------------------------------------------------------

def _to_int(value):
    try:
        return int(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    app.run(debug=True)
