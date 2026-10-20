# MCP + CrewAI

A CrewAI agent that gets its tools from four MCP servers through `MCPServerAdapter`: the filesystem server, Brave Search, GitHub, and a small custom image server (`servers/image_server.py`, built with `FastMCP`, which creates images with OpenAI's Images API). The agent researches the Model Context Protocol, creates a diagram, and saves a summary to a text file.

> **Note:** Updated for CrewAI 1.15 (which uses MCP Python SDK 1.x); the code may differ slightly from the video.

## Run it

Needs Python 3.10–3.13 and Node.js (the filesystem, Brave Search and GitHub servers run with `npx`).

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
BRAVE_API_KEY=your-brave-search-api-key
GITHUB_PERSONAL_ACCESS_TOKEN=your-github-token
# OPENAI_ORGANIZATION=optional
```

Then run:

```bash
python main.py
```

The filesystem server may only touch the `downloads/` folder next to `main.py` (change `DOWNLOADS_DIR` to point it somewhere else). Generated images are saved to `images/`.

`requirements.txt` keeps `mcp` below 2.0 because CrewAI 1.15 requires MCP 1.28.x. In MCP 2.x, `FastMCP` was renamed to `MCPServer` (`from mcp.server.mcpserver import MCPServer`).
