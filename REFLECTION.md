# Day 91 — Reflection: PDF → Speech Audiobook

🔗 **Live site:** https://pdf-to-speech-hkpk.onrender.com
*(Free tier — the first visit after a quiet spell takes ~50s to wake up.)*

## How I approached it
Broke the problem into three clean stages: (1) pull text out of the PDF, (2) hand text to a TTS engine, (3) wrap it in a CLI. Picked `pypdf` for extraction and offered two TTS paths — `gTTS` for natural-sounding online output and `pyttsx3` as an offline fallback. Added a Buy Me a Coffee prompt that fires once the MP3 is written. Then went further than a CLI: built a Flask web app (`app.py`) that reuses the same `extract_text`/`synthesise_*` functions, and deployed it live on Render's free tier at `pdf-to-speech-hkpk.onrender.com`.

## What was easy
- The actual PDF text extraction. `pypdf` is one line per page.
- Wiring `argparse` for the CLI — by Day 91 this is muscle memory.
- gTTS API surface is tiny: `gTTS(text).write_to_fp(file)`.

## What was hard
- gTTS silently fails on huge inputs, so I had to chunk text on sentence boundaries and append to the same MP3 file. Took some trial to land on ~4500 chars per chunk.
- Hyphenated line breaks in PDFs ("inter-\nesting") read out as two words. Fixed with a small preprocessing pass.
- Scanned PDFs return empty strings — I now exit early with a clear OCR hint instead of producing a silent file.
- Deploying revealed the free-tier reality: Render spins the instance down after 15 min idle, so the first visitor gets a bare `Not Found` (`x-render-routing: no-server`) until the cold start finishes ~50s later. Looked broken; wasn't.

## Biggest learning
APIs and offline libraries solve the same problem with very different tradeoffs. gTTS sounds great but needs internet and rate-limits you; pyttsx3 is instant and offline but sounds robotic. Designing the script to swap engines via a `--engine` flag is the real lesson — pick the right tool per use case instead of religiously sticking to one.

## What I'd do differently next time
- Add real OCR (tesseract) fallback for scanned PDFs so the script never gives up.
- Stream chunks straight to disk while generating, so a 500-page book doesn't sit in memory.
- Show conversion progress in the web UI — right now a long PDF just looks frozen until the MP3 is done.
- Try a paid TTS (ElevenLabs / Polly Neural) for one chapter and A/B the listening experience. As a VP-of-Product instinct, the quality delta is probably what determines whether anyone uses this twice.
- Decide if the free-tier cold start is acceptable for a portfolio demo, or pay for an always-on instance so first impressions aren't a 50s blank wait.

## Filed under
[[100 Days of Code]] · [[Python]] · [[APIs]] · [[Audiobooks]]
