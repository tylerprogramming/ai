# CrewAI Supabase Agent

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

An interactive CrewAI agent that reads and writes a Supabase database in plain English.
It uses five custom tools in `supabase_tools/` (get row, get all rows, insert, update, delete),
plus a `FileWriterTool` that can update the table description in `knowledge/table_info.txt`.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
```

`knowledge/table_info.txt` describes the example `leads` table; edit it to match your tables.

## Run

Run from this folder (the agent model is `gpt-5.4-mini`):

```bash
python main.py
```

Ask questions like `list all leads` or `add a lead for Jane Doe, jane@example.com`.
Type `exit` to quit.

`python get_the_connection.py` is a quick check that your Supabase credentials work
(it selects all rows from the `leads` table).
