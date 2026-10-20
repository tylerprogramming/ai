# Agentic prompt patterns

Five workflow patterns built from plain OpenAI chat calls (`gpt-5.4-mini`). Shared helpers live in `helpers/` (`run_llm`, `run_llm_parallel`, and `JSON_llm` for structured JSON output).

| Script | Pattern |
|---|---|
| `prompt_chaining.py` | Each step's output feeds the next prompt (speech, then action items, then a Dutch translation). |
| `router.py` | An LLM picks a route (model) for each prompt, then that route answers it. |
| `parallelization.py` | Several proposer calls run concurrently, an aggregator call merges them. |
| `orchestrator_workers.py` | An orchestrator splits a task into styles, workers write each one in parallel. |
| `evaluate_optimizer.py` | Generate, evaluate as JSON, and regenerate with feedback until the evaluator says PASS. |

## Run

Run from this folder so `helpers` imports resolve:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...    # or put it in a .env file
python prompt_chaining.py
```
