# First Flow – Guide Creator

A CrewAI Flow that asks for a topic and an audience level, has the LLM produce a structured outline
(`GuideOutline`), writes each section in order (feeding previous sections back as context), and
compiles everything into a Markdown guide.

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video. With
> `response_format=<PydanticModel>`, `LLM.call()` now returns the model instance instead of a JSON string.

## Setup

Requires Python >=3.10 <3.14 and [uv](https://docs.astral.sh/uv/).

```bash
pip install uv
crewai install
```

Add your `OPENAI_API_KEY` to a `.env` file in this folder. The flow uses `openai/gpt-5.4-mini`.

## Run

```bash
crewai run        # or: crewai flow kickoff
```

Answer the two prompts (topic and `beginner`/`intermediate`/`advanced`). Output is written to
`output/guide_outline.json` and `output/complete_guide.md` (relative to where you run it).

`plot` (`uv run plot`) saves a visualization of the flow.
