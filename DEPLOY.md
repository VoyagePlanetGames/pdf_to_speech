# Deploy guide

## 1. Push to GitHub

```bash
cd "/Users/cheny/Documents/Gooloo Doc/Project & Learning/100 Days Programming/D91"

# Initialise a fresh repo here
git init
git add .
git commit -m "Day 91: PDF to audiobook web app"
git branch -M main

# Create an EMPTY repo on github.com first (no README, no .gitignore),
# then copy the URL it gives you and run:
git remote add origin https://github.com/<your-username>/listenly.git
git push -u origin main
```

If you've never set up GitHub auth on this machine, the easiest path is `gh auth login` (GitHub CLI) — it handles credentials in one step.

## 2. Deploy live on Render (free tier)

1. Sign in at [render.com](https://render.com) with your GitHub account.
2. **New → Web Service** → select the `listenly` repo.
3. Render reads `render.yaml` automatically. Confirm:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Plan: Free
4. Click **Create Web Service**. First build takes ~2 minutes.
5. Your live URL: `https://listenly.onrender.com` (or whatever Render assigns).

Free tier sleeps after 15 min of inactivity — first request after that takes ~30s to spin up. Fine for a portfolio piece.

## 3. After deploying

- Update the `BMC_URL` in `pdf_to_speech.py` and the three coffee links in `templates/index.html` to your actual Buy Me a Coffee handle.
- Drop the live URL into your README, your portfolio, and your Obsidian `[[100 Days of Code]]` note.

## 4. Alternative hosts

| Host | Free tier | Sleeps? | Notes |
|---|---|---|---|
| **Render** | ✓ | Yes, 15 min | Easiest, uses `render.yaml` |
| **Railway** | $5/mo credit | No | Faster cold starts |
| **Fly.io** | ✓ | Yes | Needs `fly launch` CLI |
| **PythonAnywhere** | ✓ | No (limited CPU) | Old-school but reliable |
| **GitHub Pages** | ✗ for this | — | Static only — won't run Flask |
