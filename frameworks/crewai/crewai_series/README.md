# CrewAI Series

This repository contains a series of projects demonstrating the capabilities and evolution of CrewAI, a framework for orchestrating role-playing AI agents. Each day's project builds upon the previous, showcasing different aspects and features of CrewAI.

## Overview of Daily Projects



### Day 01: Introduction to CrewAI
- Basic setup of CrewAI
- Creating simple agents and tasks
- Understanding the fundamental concepts of CrewAI

### Day 02: Multi-Agent Collaboration
- Implementing multiple agents with distinct roles
- Designing tasks that require agent collaboration
- Exploring basic inter-agent communication

### Day 03: Advanced Task Management
- Introducing more complex task structures
- Implementing task dependencies and sequences
- Enhancing agent decision-making capabilities

### Day 04: Automated News Analysis
- Creating a system for news gathering and analysis
- Implementing agents for research, analysis, and report writing
- Generating comprehensive news reports automatically

### Day 05: Content Marketing Strategy
- Developing an automated content marketing workflow
- Creating specialized agents for content strategy, writing, editing, and SEO
- Producing a complete content marketing strategy with AI assistance

### Day 06: CrewAI Flow System
- Introduction to the new Flow system in CrewAI
- Implementing multiple crews with different configurations
- Using YAML files for agent and task definitions
- Visualizing workflows with the `flow.plot()` method

## Getting Started

Each day's project is contained in its own directory (e.g., `day_01`, `day_02`, etc.). To get started with a specific day:

1. Navigate to the day's directory
2. Follow the README instructions in that directory for setup and execution

## Prerequisites

- Python >=3.10 <=3.13
- Poetry (for dependency management)

## General Setup

1. Clone this repository
2. Install Poetry if you haven't already:
   ```
   pip install poetry
   ```
3. Navigate to the specific day's directory
4. Install dependencies:
   ```
   poetry install
   ```
5. Set up your OpenAI API key in the `.env` file

## Running a Project

Typically, you can run a day's project with:

```
poetry run python src/day_XX/main.py
```

Replace `XX` with the day number (e.g., `01`, `02`, etc.)


## Jupyter Notebooks

This series also includes Jupyter notebooks for interactive exploration and execution of CrewAI concepts. Here's a list of the available notebooks:

1. `day_01.ipynb`: Introduction to CrewAI
   - This notebook demonstrates the basic setup and usage of CrewAI, introducing simple agents and tasks.

2. `day_02.ipynb`: Local LLM Agents
   - shows how to use Ollama for creating agents and tasks

3. `day_03.ipynb`: News Aggregator start
   - Starts the news aggregator project with Tools

4. `day_04.ipynb`: Custom Tooling
   - Shows how to create custom tools for the agents using a more refined SerperDev tool

5. `day_05.ipynb`: New Feature in CrewAI
   - Introduces the new Flow system in CrewAI, implementing multiple crews and using YAML files for configurations.

### Running the Notebooks

To run the Jupyter notebooks:

1. Ensure you have Jupyter installed. If not, you can install it using:
   ```
   pip install jupyter
   ```

2. Navigate to the project directory and start Jupyter:
   ```
   jupyter notebook
   ```

3. In the Jupyter interface, navigate to the desired notebook (e.g., `day_01.ipynb`) and open it.

4. You can run the cells individually by clicking on them and pressing Shift+Enter, or you can run all cells from the "Cell" menu by selecting "Run All".

5. Make sure you have set up your environment variables (like OPENAI_API_KEY) before running the notebooks.

Each notebook corresponds to its respective day's project, allowing for an interactive exploration of the concepts covered in that day's lesson.
