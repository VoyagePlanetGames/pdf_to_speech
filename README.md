# 🎧 Listenly — Free PDF to Audiobook

Drop a PDF, get an MP3 audiobook. Built as Day 91 of the 100 Days of Code challenge.

- **CLI:** `python pdf_to_speech.py book.pdf`
- **Web:** Flask app at `/` — upload, choose engine, download MP3
- **Engines:** Google Translate TTS (natural, online) or `pyttsx3` (offline OS voice)

## Quick start (local)

```bash
git clone https://github.com/<your-username>/listenly.git
cd listenly
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

CLI only:

```bash
python pdf_to_speech.py book.pdf --engine gtts --lang en --start 1 --end 20
```

## Deploy free on Render

1. Push this repo to GitHub (see commands below).
2. Go to [render.com](https://render.com) → **New → Web Service** → connect your repo.
3. Render auto-detects `render.yaml` and uses `gunicorn app:app`. Click **Deploy**.
4. Wait ~2 minutes. You get a public `https://listenly.onrender.com` URL.

Other one-click options that work the same way: Railway, Fly.io, PythonAnywhere.

> Note: GitHub Pages won't work for this — it's static only and can't run Python.

## Project structure

```
.
├── app.py              # Flask web app
├── pdf_to_speech.py    # CLI + reusable TTS functions
├── templates/
│   └── index.html      # Landing page
├── static/
│   └── style.css       # Styling
├── requirements.txt
├── Procfile            # Render / Heroku entry point
└── render.yaml         # Render auto-deploy config
```

## How it works

1. **Extract** — `pypdf` pulls text from each page; hyphenated line breaks are stitched back together.
2. **Chunk** — Text is split on sentence boundaries to stay under gTTS's request limit.
3. **Speak** — Each chunk goes to Google Translate TTS and is appended to a single MP3.
4. **Serve** — Flask returns a download link to the finished file.

## Roadmap

- OCR fallback for scanned PDFs (`pytesseract`)
- Streaming generation so the user can start listening before conversion finishes
- ElevenLabs / AWS Polly Neural option for premium voices
- A/B test playback quality against paid audiobooks

## Support

If this saved you a few hours of reading, [buy me a coffee ☕](https://buymeacoffee.com/chenbuilds).

## License

MIT — see [LICENSE](LICENSE).
