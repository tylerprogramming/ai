# Smolagents intro

Eight short scripts from the smolagents intro video. Most use `InferenceClientModel` (Hugging Face Inference Providers), so you need a Hugging Face token.

| Script | What it shows | Needs |
|---|---|---|
| `01 - first project.py` | `CodeAgent` with DuckDuckGo search | `HF_TOKEN` |
| `02 - e2b.py` | Runs the agent's code in an E2B sandbox (`executor_type="e2b"`) | `HF_TOKEN`, `E2B_API_KEY` |
| `03 - custom tool.py` | A `@tool` that finds the most downloaded Hub model for a task | `HF_TOKEN` |
| `04 - gen image multiple tools.py` | Two tools: Hub model lookup plus a text-to-image `Tool` class. Writes `image.png` | `HF_TOKEN` |
| `05 - gradio image gen.py` | The same image agent behind a Gradio UI | `HF_TOKEN` |
| `06 - any llm.py` | Chat loop with `LiteLLMModel("openai/gpt-5.4-mini")`. Type `exit` to quit | `OPENAI_API_KEY` |
| `07 - import spaces.py` | Wraps a Hugging Face Space as a tool with `Tool.from_space` | network access to the Space |
| `08 - multi-agent framework.py` | A manager `CodeAgent` that calls a web-search `ToolCallingAgent` | `HF_TOKEN` |

## Run

Put your keys in a `.env` file in this folder (`HF_TOKEN=...`, `OPENAI_API_KEY=...`, `E2B_API_KEY=...`), then:

```bash
pip install -r requirements.txt
python "01 - first project.py"
python "05 - gradio image gen.py"   # opens the Gradio app at http://127.0.0.1:7860
```

The file names contain spaces, so keep the quotes.

> **Note:** Updated for smolagents 1.26 (`HfApiModel` is now `InferenceClientModel`, `ManagedAgent` was removed, E2B uses `executor_type="e2b"`) and huggingface_hub 1.x; the code may differ slightly from the video.
