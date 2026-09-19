# agent-builder: a Claude Code skill for creating AI agents

Give it a task description and a framework preference. It generates a complete, working agent
project with the right structure, dependencies, and best practices for your chosen framework.

📺 **Video:** [Coming soon]

---

## Supported Frameworks

| Framework | Version | Best For |
|-----------|---------|----------|
| AutoGen | v0.7+ | Multi-agent collaboration, code execution |
| CrewAI | v1.15+ | Role-based crews, sequential workflows |
| PydanticAI | v2.x | Type-safe agents, structured outputs |
| Smolagents | v1.26+ | Lightweight code agents, HuggingFace |
| OpenAI Agents | v0.58+ | Simple agents with OpenAI models |

## Quick start

**1. Install the skill**

```bash
git clone https://github.com/tylerprogramming/ai.git
cp -r ai/claude_skill_agent_builder/skill ~/.claude/skills/agent-builder
```

**2. Run it**

```
/agent-builder
```

It asks for:
- What task should the agent perform?
- Which framework (autogen, crewai, pydanticai, smolagents, openai)?
- Any specific requirements?

## What you get

A complete project folder with:

```
my_agent_project/
├── README.md           # How to run the agent
├── requirements.txt    # Dependencies
├── main.py            # Entry point
├── agents/            # Agent definitions
├── tools/             # Custom tools (if needed)
└── config/            # Configuration files
```

## Example

```
/agent-builder

Task: A customer support agent that can search knowledge base and create tickets
Framework: crewai

Generating project...

Created: customer_support_agent/
├── README.md
├── requirements.txt
├── main.py
├── crew.py
├── agents.yaml
├── tasks.yaml
└── tools/
    ├── knowledge_search.py
    └── ticket_creator.py
```

## What's in here

```
README.md                       this file
skill/
  SKILL.md                      the skill definition
  templates/
    autogen_template.md         AutoGen v0.7+ project template
    crewai_template.md          CrewAI v1.15+ project template
    pydanticai_template.md      PydanticAI v2.x project template
    smolagents_template.md      Smolagents v1.26+ project template
    openai_template.md          OpenAI Agents project template
  reference/
    frameworks.md               Framework comparison and best practices
```

## Requirements

- Claude Code with a paid Claude subscription
- Python 3.10+
- The target framework installed for testing

## Credits

Built by Tyler for the AI agents community.
