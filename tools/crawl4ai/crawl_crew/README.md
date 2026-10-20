# CrawlCrew Crew

> **Note:** Updated for CrewAI 1.15 and Crawl4AI 0.9; the code may differ slightly from the video.

Welcome to the CrawlCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

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

Crawl4AI drives a headless Chromium browser. Install it once with:
```bash
uv run crawl4ai-setup
```
### Customizing

**Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`** (`MODEL` picks the LLM; without it CrewAI falls back to `gpt-4.1-mini`)

- Modify `src/crawl_crew/config/agents.yaml` to define your agents
- Modify `src/crawl_crew/config/tasks.yaml` to define your tasks
- Modify `src/crawl_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/crawl_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the crawl_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

The crew's `Crawl Sitemap` tool fetches the sitemap passed in `src/crawl_crew/main.py` (`https://docs.crewai.com/sitemap.xml` by default), crawls every page with Crawl4AI, and the agent prints a summary of what it found.

## Understanding Your Crew

The crawl_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the CrawlCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
