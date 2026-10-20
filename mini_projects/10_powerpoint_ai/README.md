# PowerPoint AI

Generate PowerPoint slides with OpenAI (`gpt-5.4-mini`) and `python-pptx`.

| Script | What it does | Output |
|---|---|---|
| `powerpoint.py` | Asks the model for a JSON outline (title + 5 sections) about a topic and builds a styled deck. | `presentation.pptx` |
| `pp_test.py` | Uses structured output (`chat.completions.parse` with a Pydantic model) to get three sections with colors, then builds one 16:9 slide with shapes. Falls back to built-in text if the API call fails. | `python_introduction.pptx` |

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...    # or put it in a .env file
python powerpoint.py
python pp_test.py
```

The `.pptx` files are written to the current folder.
