# Airtable

An AutoGen "Engineer" agent with Airtable tools (create a record, get a table's record structure, list all records). You give it instructions in the terminal and it calls the Airtable API for you.

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=your-openai-key
API_KEY=your-airtable-personal-access-token
BASE_ID=your-airtable-base-id
```

Then run:

```bash
python airtable.py
```

Type your instructions when prompted (e.g. "Create a record in the Contacts table for Jane"). Type `exit` to stop.
