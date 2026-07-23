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

## Turn on saved, shared data + file storage (Supabase) — optional but recommended
Without this, the tracker runs in each person’s browser only (resets on refresh). With it, every
project, note, version, activity and timesheet is **saved in Postgres and synced live** across
everyone, and photos/documents are stored in **Supabase Storage**.

1. **Create a Supabase project** at https://supabase.com (free tier is fine).
2. **Run the schema.** In Supabase → **SQL Editor → New query**, paste the contents of
   **`supabase_setup.sql`** (in this folder) → **Run**. It creates the tables, security policies,
   realtime, and the `attachments` storage bucket.
3. **Get your keys.** Supabase → **Project Settings → API**: copy the **Project URL** and the
   **anon public** key.
4. **Add them to Streamlit.** Your app → **⋮ → Settings → Secrets**, add:
   ```toml
   SUPABASE_URL = "https://YOURPROJECT.supabase.co"
   SUPABASE_ANON_KEY = "your-anon-public-key"
   ```
   Save — Streamlit redeploys. That’s it: data now persists and syncs for everyone.

**Notes.** The sign-in is name-only (no real accounts), so the anon key can read/write the data —
keep the Streamlit app **private (invite-only)** if you want to control who can open it. `projects`
and `activities` are shared; each person’s `timesheet` is their own. Files go to the public
`attachments` bucket. This is great for a team; if you later need per-user permissions or audit,
we can add real Supabase Auth.
