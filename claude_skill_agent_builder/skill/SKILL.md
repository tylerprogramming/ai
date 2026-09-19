---
name: agent-builder
description: Create complete AI agent projects from a task description. Supports AutoGen, CrewAI, PydanticAI, Smolagents, and OpenAI Agents. Generates working code with proper structure, dependencies, and best practices. Triggers on - create an agent, build an agent, new agent project, scaffold agent, agent template, generate agent code.
---

# agent-builder

Give it a task and a framework. It generates a complete, working agent project with the right
structure, dependencies, and best practices.

## Inputs

| input | default | notes |
|---|---|---|
| task | required | What the agent should do (e.g., "research assistant that searches the web") |
| framework | ask user | `autogen`, `crewai`, `pydanticai`, `smolagents`, or `openai` |
| project_name | derived | Snake_case name derived from task |
| model | gpt-5.4-mini | Default LLM to use |
| include_tools | true | Generate custom tools if the task needs them |

## Framework Selection Guide

When the user doesn't specify a framework, recommend based on their task:

| Task Type | Recommended Framework | Why |
|-----------|----------------------|-----|
| Multi-agent collaboration | AutoGen | Best for complex agent-to-agent workflows |
| Role-based teams | CrewAI | Built for crew metaphor with roles/tasks |
| Type-safe, structured output | PydanticAI | Pydantic integration, strong typing |
| Lightweight, code execution | Smolagents | Minimal overhead, code agents |
| Simple single agent | OpenAI Agents | Straightforward, OpenAI native |

## Process

### 1. Gather requirements

Ask the user:
1. "What task should the agent perform?" (required)
2. "Which framework? (autogen/crewai/pydanticai/smolagents/openai)" - if not specified, recommend
3. "Any specific requirements? (tools, APIs, output format)"

### 2. Validate the framework choice

Check `reference/frameworks.md` for the framework's current API patterns. Each framework has
different conventions - follow them exactly.

### 3. Design the agent architecture

Based on the task:
- Single agent: Simple tasks, one responsibility
- Multi-agent: Complex tasks needing collaboration
- Crew/Team: Tasks with distinct roles (research, write, review)

Identify required tools:
- Web search: DuckDuckGo, Tavily, Serper
- Code execution: Docker sandbox, local executor
- File operations: Read/write files
- API calls: Custom integrations
- Database: Vector stores, SQL

### 4. Generate the project

Use the appropriate template from `templates/`. Generate:

1. **README.md** - How to set up and run
2. **requirements.txt** - All dependencies with versions
3. **main.py** - Entry point
4. **Agent files** - Framework-specific agent definitions
5. **Tools** - Custom tools if needed
6. **Config** - Any configuration files

### 5. Validate the code

Before presenting to user:
- Check imports are correct for the framework version
- Ensure all tools are properly defined
- Verify the entry point runs without syntax errors

## Templates

Each template in `templates/` contains:
- Current import patterns for that framework
- Project structure conventions
- Example agent and tool definitions
- Common gotchas to avoid

## Rules

- **Use current API patterns.** AutoGen v0.7+ uses async/await and `autogen_agentchat`. CrewAI uses
  decorators and YAML config. Check `reference/frameworks.md` for current patterns.
- **Pin dependency versions.** Always include version pins in requirements.txt.
- **Generate working code.** Every file should be syntactically correct and runnable.
- **Follow framework conventions.** CrewAI uses YAML for agents/tasks, AutoGen uses Python classes,
  PydanticAI uses decorators. Match the framework's idioms.
- **Include error handling.** Wrap API calls in try/except, handle missing API keys gracefully.
- **Document everything.** README should explain setup, configuration, and usage.
- **No placeholders.** Generate complete, working code. If something needs user input, use
  environment variables with clear documentation.
