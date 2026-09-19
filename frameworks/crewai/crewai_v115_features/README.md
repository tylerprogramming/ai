# CrewAI v1.15+ New Features

Examples showcasing the latest CrewAI features as of v1.15+.

## Installation

```bash
pip install -U crewai crewai-tools
```

## New Features Covered

1. **Conversational Flows** - Interactive chat-style agent workflows
2. **LLM Overlay** - Route different agent roles to different models
3. **Human Feedback** - Pause execution for human input
4. **Platform Tools** - Use CrewAI platform integrations
5. **Checkpoints** - Save and resume crew execution state

## Examples

- `01_conversational_flow.py` - Interactive conversational agent flow
- `02_llm_overlay.py` - Route agents to different models
- `03_human_feedback.py` - Pause for human approval
- `04_streaming_output.py` - Real-time streaming responses

## Running

```bash
export OPENAI_API_KEY="your-key"
python 01_conversational_flow.py
```
