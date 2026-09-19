# Smolagents v1.26+ Features

HuggingFace's lightweight agent framework examples.

## Installation

```bash
pip install -U smolagents
```

## Features Covered

1. **Code Agents** - Agents that write and execute Python code
2. **Tool Agents** - Agents that use pre-defined tools
3. **Multi-Agent** - Hierarchical agent systems
4. **Custom Tools** - Creating your own tools
5. **Different LLMs** - Using various model providers

## Examples

- `01_code_agent.py` - Agent that writes code to solve problems
- `02_tool_agent.py` - Agent with specific tools
- `03_custom_tool.py` - Creating custom tools
- `04_multi_agent.py` - Multi-agent coordination

## Running

```bash
export OPENAI_API_KEY="your-key"  # or HF_TOKEN for Hugging Face
python 01_code_agent.py
```
