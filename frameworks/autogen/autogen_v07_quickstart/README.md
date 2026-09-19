# AutoGen v0.7+ Quickstart Examples

This folder contains examples using the **new AutoGen v0.7+ API**, which is a complete rewrite with an async, event-driven architecture.

## Installation

```bash
pip install -U "autogen-agentchat" "autogen-ext[openai]"
```

## What Changed from v0.2?

The v0.7+ version is a complete rewrite. Key differences:

| v0.2 (Old) | v0.7+ (New) |
|------------|-------------|
| `import autogen` | `from autogen_agentchat import ...` |
| `autogen.AssistantAgent` | `AssistantAgent` from `autogen_agentchat.agents` |
| `autogen.UserProxyAgent` | `UserProxyAgent` from `autogen_agentchat.agents` |
| Synchronous execution | Async/await pattern |
| `config_list` pattern | `OpenAIChatCompletionClient` model client |
| `initiate_chat()` | `agent.run()` or `agent.run_stream()` |

## Examples

1. **01_simple_agent.py** - Basic single agent with a tool
2. **02_two_agent_chat.py** - Two agents collaborating
3. **03_group_chat.py** - Multiple agents in a group chat
4. **04_code_execution.py** - Agent that writes and executes code

## Running Examples

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run any example
python 01_simple_agent.py
```

## Migration Guide

See the official migration guide: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/migration-guide.html
