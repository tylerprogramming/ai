# n8n with external task runners (Python packages in Code nodes)

Runs n8n plus a custom `n8nio/runners` image so Code nodes can use Python packages
(`yt-dlp`, `numpy`, `pandas`, `pydub`). The runner image extends the official one and
allowlists those packages in `n8n-task-runners.json`.

> **Note:** Updated to n8n 2.44.4. The runner auth token now comes from `.env` instead of
> being hardcoded, and the runner broker port is no longer published to the host.

## Run it

```bash
cp .env.example .env
# set N8N_RUNNERS_AUTH_TOKEN, e.g. openssl rand -hex 32
docker compose up --build
```

Open http://localhost:5678. Files for the Code nodes go in `../videos` (mounted at `/videos`).

## Changing the n8n version

The `n8nio/runners` image must be the same version as `n8nio/n8n`. Set `N8N_VERSION` in
`.env`; docker compose uses it for both. `n8n-task-runners.json` is based on the default
config shipped with that runners version (`docker/images/runners/n8n-task-runners.json` in
the n8n repo). If you change versions, compare it with the new default and keep only the
allowlist changes.
