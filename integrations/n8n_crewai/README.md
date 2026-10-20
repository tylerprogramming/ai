# n8n + CrewAI

A small Flask API that n8n calls with customer feedback (arrival rating, comments, food feedback, overall rating, timestamp). It runs the `deep_fried` CrewAI Flow: one agent writes a funny, light-hearted reply email and a second agent checks it. The reply comes back in the JSON response for n8n to use in the next node.

> **Note:** Updated for CrewAI 1.15 and secured with a shared-secret header; the code may differ slightly from the video.

## Run it

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
# Any long random string; n8n must send the same value in the X-API-Key header.
# e.g. python -c "import secrets; print(secrets.token_urlsafe(32))"
N8N_SHARED_SECRET=your-long-random-secret
```

Start the server from this folder:

```bash
python app.py
```

It listens on `http://127.0.0.1:5003/process`. Every request without the correct `X-API-Key` header gets a `401 Unauthorized`.

Optional environment variables:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Interface to bind. Use `0.0.0.0` if n8n runs in Docker (see below). |
| `PORT` | `5003` | Port to listen on. |
| `FLASK_DEBUG` | off | Set to `1` for Flask debug mode while developing. Never enable it on a reachable host. |

### n8n running in Docker

Inside a container, `127.0.0.1` is the container itself, so n8n can't reach a server bound to your machine's localhost. Start the server with `HOST=0.0.0.0 python app.py` and use `http://host.docker.internal:5003/process` as the URL in n8n (on Linux, add `--add-host=host.docker.internal:host-gateway` to the n8n container). Binding to `0.0.0.0` exposes the port on your network, which is why the shared secret is required.

## n8n HTTP Request node setup

1. **Method:** `POST`
2. **URL:** `http://127.0.0.1:5003/process` (or `http://host.docker.internal:5003/process` from Docker)
3. **Authentication:** `Generic Credential Type` → `Header Auth`, and create a credential with
   - **Name:** `X-API-Key`
   - **Value:** the same value as `N8N_SHARED_SECRET`

   (Alternatively turn on **Send Headers** and add a header `X-API-Key` with that value, but a credential keeps the secret out of the workflow JSON.)
4. **Send Body:** on, **Body Content Type:** `JSON`, with fields such as:

```json
{
  "arrival_rating": 3,
  "comments": "Please...no...",
  "feedback": "It wasn't even fried....",
  "overall": 2,
  "timestamp": "12/12/2024 16:46:12"
}
```

The generated reply is in `sample_result.response` of the response. Each request is also appended to `log.txt`.

## Run the flow without n8n

```bash
cd deep_fried
crewai install
crewai run
```

This runs the flow once with sample feedback.
