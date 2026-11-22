# Scherer/Crandall Thanksgiving 2026

Mobile-first event app for the 2026 Thanksgiving Olympics + Scavenger Hunt.

Deploys automatically to Railway on every push to `main` (confirmed working 2026-11-22).

## Run locally

```bash
pip3 install --user -r requirements.txt
python3 -m uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000 on your phone (or resize your browser) to test.

Local data (SQLite + uploaded photos/videos) is stored in `data_volume/`, which is
git-ignored.

## Environment variables

- `ADMIN_PASSWORD` &mdash; shared password for the Judge page. Defaults to `turkey` locally.
- `SESSION_SECRET` &mdash; random string used to sign the admin session cookie.
- `OLYMPICS_UNLOCK_AT` &mdash; ISO timestamp (with timezone) when the Olympics page unlocks.
  Defaults to `2026-11-25T10:00:00-05:00`.
- `SCAVENGER_UNLOCK_AT` &mdash; ISO timestamp when the Scavenger Hunt page unlocks.
  Defaults to `2026-11-25T15:00:00-05:00`.
- `DATA_DIR` &mdash; where the SQLite DB + uploads live. On Railway this should be the
  mounted volume path (e.g. `/data`).

## Deploying to Railway

```bash
railway login
railway init
railway volume add   # mount at /data
railway variables set ADMIN_PASSWORD=... SESSION_SECRET=... \
  OLYMPICS_UNLOCK_AT=2026-11-25T10:00:00-05:00 \
  SCAVENGER_UNLOCK_AT=2026-11-25T15:00:00-05:00 \
  DATA_DIR=/data
railway up
```

Railway will give you a `*.up.railway.app` URL. Re-run `railway up` any time you want
to push a content/copy change before the big day.
