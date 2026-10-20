# Autogen Functions

Examples of giving AutoGen agents Python functions (tools) to call:

- `autogen_function_example.py` – a currency bot with a currency-exchange tool (explicit tool name/description via `FunctionTool`).
- `autogen_function_example_decorators.py` – the same bot, with the tool described by type hints and `Annotated` parameters.
- `autogen_function_planner.py` – an assistant whose tool asks a separate planner agent for a plan, while a code executor runs the code it writes (saved in `planning/`).

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python autogen_function_example.py
```
