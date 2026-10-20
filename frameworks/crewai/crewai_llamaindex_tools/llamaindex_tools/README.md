# LlamaIndex Tools with CrewAI

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

A CrewAI Flow whose agents use LlamaIndex tools through `crewai_tools.LlamaIndexTool`: a math crew (LlamaIndex `FunctionTool`s for add/subtract/multiply/divide) and a Yahoo Finance crew (`YahooFinanceToolSpec`). The flow runs the math crew; the Yahoo Finance and Wikipedia steps are left commented out in `main.py`.

Welcome to the llamaindex_tools project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/llamaindex_tools/crews/<crew>/config/agents.yaml` to define your agents (model: `gpt-5.4-mini`)
- Modify `src/llamaindex_tools/crews/<crew>/config/tasks.yaml` to define your tasks
- Modify `src/llamaindex_tools/tools/math_function_tool.py` to add your own LlamaIndex tools
- Modify `src/llamaindex_tools/main.py` to change the flow and its inputs

## Running the Project

To kickstart the flow, run this from the root folder of your project (the folder containing `pyproject.toml`):

```bash
crewai run
```

This command runs the llamaindex_tools Flow (`kickoff` in `src/llamaindex_tools/main.py`). Run `uv run plot` to render the flow diagram.

This example, unmodified, asks the math agent to multiply 5 and 2 with the LlamaIndex multiply tool and prints the flow state.

## Understanding Your Crew

The llamaindex_tools Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding crewAI:

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
