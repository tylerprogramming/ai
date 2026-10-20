# Lead Scoring Crew (CrewAI)

Pipeline: Transcript ➜ Extraction ➜ Insights ➜ Deterministic Score ➜ Report

## Quickstart
1. Create a `.env` file with `OPENAI_API_KEY=...` (optionally `MODEL=gpt-5.4-mini` and `SCORING_WEIGHTS` as JSON, e.g. `{"need": 0.3}`).
2. Install deps: `crewai install` (or `pip install -e .`)
3. The sample call transcript lives in `SAMPLE_TRANSCRIPT` in `src/lead_crew/main.py` — replace it with your own.
4. Run: `crewai run` (or `lead_crew` after `pip install -e .`)
5. Outputs:
   - `lead_report.md` (full report)
   - Console logs (Crew run + final report)

> **Note:** Updated for CrewAI 1.15; the code may differ slightly from the video.

## Inputs you can pass to `kickoff`
- `transcript` (str) – raw transcript text
- `company` (str) – prospect company, optional
- `contact_name` (str) – prospect person, optional
- `product` (str) – your product/service brief
- `icp_criteria` (str) – describe your ICP in plain language
- `current_year` (str) – defaults to the current year
- `scoring_rubric` (str) – freeform description of your scoring philosophy

## Tiers
- **Hot**: total ≥ 70
- **Warm**: 40–69
- **Cold**: < 40

You can tune the deterministic tool in `src/lead_crew/tools/score_tool.py`.