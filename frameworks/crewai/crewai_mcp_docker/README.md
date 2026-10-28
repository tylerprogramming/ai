# CrewAI + MCP Servers in Docker

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

A CrewAI crew (`fastapi_crew/`) that plans, writes and reviews a FastAPI CRUD app using
three MCP servers running in Docker:

- **Context7** (`context7-mcp`, built from the `Dockerfile` here) for up-to-date library docs
- **SQLite** (`mcp/sqlite`)
- **Filesystem** (`mcp/filesystem`), which mounts only the `app/` subfolder of this project
  into the container as `/projects/app`, so the generated code lands in `crewai_mcp_docker/app/`
  (created on first run). The rest of the project, including `fastapi_crew/.env` with your
  API key, is not visible to the MCP server.

The crew connects to the servers through `mcp_server_params` / `self.get_mcp_tools()` in
`fastapi_crew/src/fastapi_crew/crew.py`.

## Setup

1. Build the Context7 image and pull the other two:
   ```bash
   docker build -t context7-mcp .
   docker pull mcp/sqlite
   docker pull mcp/filesystem
   ```
2. Copy `.env.example` to `fastapi_crew/.env` and add your `OPENAI_API_KEY`.
3. Install and run the crew (agents use `gpt-5.4-mini`, set in `config/agents.yaml`):
   ```bash
   cd fastapi_crew
   crewai install
   crewai run
   ```

The code reviewer reviews the generated files in `/projects/app` (the `file_path` input in
`main.py`). To run the generated app, `cd app` and follow the README the crew writes there.
`requirements.txt` in this folder lists baseline dependencies for the generated FastAPI app
(the crew usually writes its own `app/requirements.txt` too), not for the crew. It uses
`psycopg2-binary`, so `pip install -r requirements.txt` works without a local PostgreSQL
build toolchain; for production builds against your own libpq, swap it for `psycopg2`.
