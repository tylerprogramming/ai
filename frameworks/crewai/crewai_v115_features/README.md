# CrewAI v1.15+ New Features

Examples showcasing the latest CrewAI features as of v1.15+.

> **Note:** Updated for CrewAI 1.15.28; the code may differ slightly from the video.

## Installation

```bash
pip install -r requirements.txt
```

## New Features Covered

1. **Conversational Flows** - Interactive chat-style agent workflows (`@ConversationConfig`, `flow.chat()`, `flow.handle_turn()`)
2. **LLM Overlay** - Route different agent roles to different models at run time (`crewai.llm_overlay.llm_overlay`)
3. **Streaming Output** - Real-time streamed chunks from a crew (`Crew(stream=True)`)
4. **JSON Crews** - Build a crew from a JSON definition (`load_crew_from_definition`, `crewai.project.load_crew`)

## Examples

- `01_conversational_flow.py` - Interactive conversational agent flow (type `exit` to quit)
- `02_llm_overlay.py` - Route agents to different models
- `03_streaming_output.py` - Real-time streaming responses
- `04_json_crew.py` - Define a crew in JSON and load it

## Running

```bash
export OPENAI_API_KEY="your-key"
python 01_conversational_flow.py
```
