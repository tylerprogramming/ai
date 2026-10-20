# CrewAI 0.83 Features: Knowledge and Mem0 Memory

Examples from the CrewAI 0.83 update video:

- `sample_knowledge.py` – gives a crew a `StringKnowledgeSource` so the agent can answer questions about the user from that knowledge.
- `crewai_mem0.py` + `search_mem0_tool.py` – an interactive loop where the agent searches a [Mem0](https://mem0.ai) memory store with a custom `SearchMem0Tool`, and each question is saved back to Mem0.

> **Note:** Updated for CrewAI 1.15 and mem0ai 2.x; the code may differ slightly from the video. Crew knowledge is now passed as `knowledge_sources=[...]` (0.83 used `knowledge={"sources": [...]}`), Mem0 `search()` takes `filters={"user_id": ...}`, and `add()` no longer takes `output_format`.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in this folder:

```
OPENAI_API_KEY=sk-...
MEM0_API_KEY=m0-...   # only needed for crewai_mem0.py
```

The agents use `gpt-5.4-mini`. Knowledge sources are embedded with OpenAI embeddings, so `OPENAI_API_KEY` is needed for both scripts.

## Run

```bash
python sample_knowledge.py   # one question answered from the knowledge source
python crewai_mem0.py        # ask questions in a loop; Ctrl+C to quit
```
