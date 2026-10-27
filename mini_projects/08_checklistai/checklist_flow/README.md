# checklist_flow

The CrewAI Flow behind ChecklistAI. It takes a checklist, has a crew write an email body from it, has a second crew pick a matching quote, and then makes one OpenAI call to merge the two into a styled HTML email.

You don't run this on its own in normal use. `app.py` and `utils/email_utils.py` in the parent folder import it (`from checklist_flow.src.checklist_flow.main import main`) and call `main(checklist_text)` whenever a scheduled email is due. See the [ChecklistAI README](../README.md) for setup.

## What's inside

- `src/checklist_flow/main.py`: `ChecklistFlow` and its steps.
  1. `generate_email_body_from_checklist` runs `ChecklistCrew` on the checklist.
  2. `generate_quote_from_email_body` runs `QuoteCrew` on that email body.
  3. `final_email_body` merges the two with `gpt-5.4-mini` and returns HTML.
  4. `save_email_body` writes the crew's email body to `email_body.txt`.
- `src/checklist_flow/crews/checklist_crew/`: one agent and one task. Their prompts are in `config/agents.yaml` and `config/tasks.yaml`.
- `src/checklist_flow/crews/quote_crew/`: one agent and one task that pick the quote.
- `src/checklist_flow/tools/custom_tool.py`: an empty example tool from the CrewAI template. Nothing uses it.

## Try the flow by itself

Install the parent folder's requirements and create its `.env` with `OPENAI_API_KEY` (see the [ChecklistAI README](../README.md)). Then, from the `08_checklistai` folder:

```bash
python -m checklist_flow.src.checklist_flow.main
```

That runs the sample checklist in `main()`. It prints the final HTML, writes `email_body.txt`, and saves a diagram of the flow to `email body flow.html` in the current folder.
