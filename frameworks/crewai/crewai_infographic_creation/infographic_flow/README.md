# infographic_flow

The CrewAI Flow package behind the infographic example. See `../README.md` for what it does and the
environment variables it needs.

## Install and run

Requires Python >=3.10 <3.14.

```bash
crewai install            # or: pip install -e .
crewai run                # runs kickoff() with the default topic
```

Or, from the parent folder, `python main.py` (same flow, topic set in `main.py`). Images are written to
`images_infographic_output/` in the folder you run from.

- Research crew: `src/infographic_flow/crews/infographic_research_crew/` (agents and tasks in `config/`)
- Flow steps: `src/infographic_flow/main.py`
