# CrewAI Listener Flow

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

A poem-writing Flow with a custom event listener (`src/crewai_listener_flow/listeners/my_custom_listener.py`) that prints crew, agent, task and flow events as they happen.

Welcome to the CrewAI Listener Flow project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

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

- Modify `src/crewai_listener_flow/crews/poem_crew/config/agents.yaml` to define your agents (model: `gpt-5.4-mini`)
- Modify `src/crewai_listener_flow/crews/poem_crew/config/tasks.yaml` to define your tasks
- Modify `src/crewai_listener_flow/crews/poem_crew/poem_crew.py` to add your own logic, tools and specific args
- Modify `src/crewai_listener_flow/listeners/my_custom_listener.py` to change which events are printed
- Modify `src/crewai_listener_flow/main.py` to change the flow

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the crewai_listener_flow Flow as defined in your configuration.

This example, unmodified, writes a short poem about CrewAI to `poem.txt` in the root folder.

## Understanding Your Crew

The crewai_listener_flow Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding crewAI:

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
