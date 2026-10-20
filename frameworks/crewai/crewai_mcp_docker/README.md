# CrewAI + MCP Servers in Docker

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

A CrewAI crew (`fastapi_crew/`) that plans, writes and reviews a FastAPI CRUD app using
three MCP servers running in Docker:

- **Context7** (`context7-mcp`, built from the `Dockerfile` here) for up-to-date library docs
- **SQLite** (`mcp/sqlite`)
- **Filesystem** (`mcp/filesystem`), which mounts this `crewai_mcp_docker` folder into the
  container as `/projects/crewai_mcp_docker`, so the generated code lands in this folder

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

`requirements.txt` in this folder lists the dependencies for the generated FastAPI app,
not for the crew.
