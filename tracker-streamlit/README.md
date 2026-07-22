# Contribution & Impact Tracker — deploy on Streamlit

This puts your tracker online at a permanent URL. To open it, a person just types
their **name** (no password) — and their update notes get signed with that name.

## What's in this folder
- `streamlit_app.py` — the app: name prompt, then your tracker
- `tracker.html` — your tracker (the whole thing)
- `requirements.txt` — one line: streamlit
- `.gitignore`

## Deploy in 5 steps (about 10 minutes)

1. **Get the files onto GitHub.** Sign in at https://github.com (free). Click **New repository**,
   name it e.g. `impact-tracker`, keep it **Private**, click **Create**. On the repo page click
   **“uploading an existing file”** and drag in **all** the files from this folder
   (`streamlit_app.py`, `tracker.html`, `requirements.txt`, `.gitignore`). Commit.

2. **Open Streamlit Cloud.** Go to https://share.streamlit.io and sign in with that same GitHub account.

3. **Create the app.** Click **Create app** → **Deploy a public app from GitHub** →
   pick your `impact-tracker` repo, branch `main`, main file **`streamlit_app.py`** → **Deploy**.
   Wait ~1–2 minutes for it to build.

4. **Choose who can open it.** In the app’s **⋮ menu → Settings → Sharing**:
   - Leave it **public** → anyone with the link can open it and type their name.
   - Or set it **private** and invite people by email → only invited people can open it.

5. **Share the URL.** You’ll get a link like `https://impact-tracker-xxxx.streamlit.app`.
   Send it to your boss and team. Each person types their name and they’re in; whatever they log
   is signed automatically.

## To update the tracker later
Replace `tracker.html` in the GitHub repo (upload the new version over the old one). Streamlit
redeploys automatically in a minute.

## Important — about shared data (please read)
This step gives you a **live, permanent URL** people open with their name. But the tracker’s content
(projects, notes, timesheet, activities, attachments) currently lives in **each person’s browser
session** — so if your boss adds a note, *you* won’t automatically see it, and it resets on refresh.

To make edits **truly shared and saved** for everyone, the tracker needs a small shared datastore.
The clean next step is to connect a **Google Sheet** (or a small database) behind it — then every
update is saved centrally and everyone sees the same live data. Ask and I’ll build that next.
