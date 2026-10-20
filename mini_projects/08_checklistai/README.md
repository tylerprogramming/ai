# ChecklistAI

A Flask app for checklists that email themselves. Create a checklist by hand, from an example, or let OpenAI generate one from a short prompt. Give it a time and recipients, and every day at that time a CrewAI Flow (`checklist_flow/`) turns the checklist into a styled HTML email with a matching quote and sends it over SMTP.

> **Note:** Updated for Flask 3 and CrewAI 1.15; the code may differ slightly from the video.

## Run it

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
FLASK_SECRET_KEY=any-long-random-string
# Gmail: use an App Password, not your normal password
MAIL_USERNAME=you@gmail.com
MAIL_PASSWORD=your-app-password
# Optional
# CHECKLIST_AI_FLASK_PORT=5000
# FLASK_DEBUG=1
```

Then run:

```bash
python app.py
```

Open http://127.0.0.1:5000. The SQLite database is created at `instance/checklists.db` on first run. Scheduled emails only go out while the app is running.
