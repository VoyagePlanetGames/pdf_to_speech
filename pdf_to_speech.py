"""
Day 91 — PDF to Speech (Free Audiobook Generator)
--------------------------------------------------
Take a PDF, extract the text, and convert it to an MP3 audiobook.

Two TTS engines are supported:
  1. gTTS  → Google Translate TTS over HTTP. Sounds natural, needs internet.
  2. pyttsx3 → Offline OS voices (SAPI5 / NSSpeechSynthesizer / espeak).

USAGE
    python pdf_to_speech.py path/to/book.pdf
    python pdf_to_speech.py path/to/book.pdf --engine offline
    python pdf_to_speech.py path/to/book.pdf --lang en --start 1 --end 10

INSTALL
    pip install pypdf gTTS pyttsx3
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from pathlib import Path


# ---------- 1. PDF TEXT EXTRACTION -------------------------------------------

def extract_text(pdf_path: Path, start: int | None, end: int | None) -> str:
    """Pull text out of a PDF. `start` and `end` are 1-indexed, inclusive."""
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install pypdf")

    reader = PdfReader(str(pdf_path))
    total = len(reader.pages)
    first = (start - 1) if start else 0
    last = end if end else total
    first = max(0, first)
    last = min(total, last)

    chunks = []
    for i in range(first, last):
        page_text = reader.pages[i].extract_text() or ""
        # Soften hard line breaks so TTS doesn't pause mid-sentence
        page_text = page_text.replace("-\n", "").replace("\n", " ")
        chunks.append(page_text)

    text = " ".join(chunks).strip()
    if not text:
        sys.exit("No extractable text found. Is this a scanned PDF? Try OCR first.")
    return text


# ---------- 2. TEXT-TO-SPEECH ENGINES ----------------------------------------

def synthesise_gtts(text: str, lang: str, out_path: Path) -> None:
    """Use Google Translate TTS. Free, no API key, requires internet."""
    try:
        from gtts import gTTS
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install gTTS")

    # gTTS chokes on huge strings, so chunk by ~4500 chars on sentence boundaries
    chunks = chunk_text(text, max_chars=4500)
    print(f"Sending {len(chunks)} chunk(s) to Google TTS...")

    # Concatenate by writing each chunk and appending to the same file
    with open(out_path, "wb") as f:
        for idx, chunk in enumerate(chunks, 1):
            tts = gTTS(text=chunk, lang=lang, slow=False)
            tts.write_to_fp(f)
            print(f"  chunk {idx}/{len(chunks)} done")


def synthesise_offline(text: str, out_path: Path, rate: int = 175) -> None:
    """Use the local OS speech engine. Works without internet."""
    try:
        import pyttsx3
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install pyttsx3")

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.save_to_file(text, str(out_path))
    engine.runAndWait()


def chunk_text(text: str, max_chars: int) -> list[str]:
    """Split text on sentence boundaries so chunks stay under max_chars."""
    sentences = text.replace("!", ".").replace("?", ".").split(". ")
    out, current = [], ""
    for s in sentences:
        if len(current) + len(s) + 2 > max_chars:
            if current:
                out.append(current.strip())
            current = s + ". "
        else:
            current += s + ". "
    if current.strip():
        out.append(current.strip())
    return out


# ---------- 3. BUY ME A COFFEE -----------------------------------------------

BMC_URL = "https://www.buymeacoffee.com/yourname"  # ← swap for your handle

def print_bmc_banner() -> None:
    banner = textwrap.dedent(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║   Audiobook ready. If this saved you 10 hours of reading, ║
    ║   buy me a coffee — it keeps the side projects coming.    ║
    ║                                                            ║
    ║   ☕  {BMC_URL:<48}║
    ╚══════════════════════════════════════════════════════════╝
    """)
    print(banner)


# ---------- 4. CLI -----------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PDF file into a free audiobook (MP3)."
    )
    parser.add_argument("pdf", type=Path, help="Path to the input PDF file")
    parser.add_argument(
        "--engine", choices=["gtts", "offline"], default="gtts",
        help="TTS engine: 'gtts' (online, more natural) or 'offline' (no internet)."
    )
    parser.add_argument("--lang", default="en", help="Language code for gTTS (e.g. en, en-uk, es, fr).")
    parser.add_argument("--start", type=int, default=None, help="First page to include (1-indexed).")
    parser.add_argument("--end",   type=int, default=None, help="Last page to include (inclusive).")
    parser.add_argument("--out", type=Path, default=None, help="Output audio file path.")
    parser.add_argument("--rate", type=int, default=175, help="Words-per-minute for offline engine.")
    args = parser.parse_args()

    if not args.pdf.exists():
        sys.exit(f"File not found: {args.pdf}")

    out_path = args.out or args.pdf.with_suffix(".mp3")

    print(f"Extracting text from {args.pdf.name}...")
    text = extract_text(args.pdf, args.start, args.end)
    print(f"Got {len(text):,} characters of text.")

    print(f"Generating audio with engine: {args.engine}")
    if args.engine == "gtts":
        synthesise_gtts(text, args.lang, out_path)
    else:
        synthesise_offline(text, out_path, rate=args.rate)

    print(f"\nSaved → {out_path}  ({os.path.getsize(out_path) / 1024:.1f} KB)")
    print_bmc_banner()


if __name__ == "__main__":
    main()
