# PydanticAI v2.x Features

Advanced examples showcasing PydanticAI v2.x features.

## Installation

```bash
pip install -r requirements.txt
```

## Features Covered

1. **Structured Outputs** - Type-safe responses with Pydantic models
2. **Tool Use** - Custom tools with full type hints
3. **Streaming** - Real-time streaming responses
4. **Multi-Model** - Support for various LLM providers
5. **Dependencies** - Dependency injection for tools

## Examples

- `01_structured_output.py` - Type-safe agent responses
- `02_tools_with_context.py` - Tools with dependency injection
- `03_streaming_agent.py` - Streaming responses
- `04_multi_agent.py` - Multi-agent coordination

## Running

```bash
export OPENAI_API_KEY="your-key"
python 01_structured_output.py
```

> **Note:** Updated for pydantic-ai 2.58 (`output_type=` and `result.output` replace `result_type=` and `result.data`); the code may differ slightly from the video.
