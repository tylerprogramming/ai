# Lead Scoring Crew (CrewAI)

Pipeline: Transcript ➜ Extraction ➜ Insights ➜ Deterministic Score ➜ Report

## Quickstart
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (and optionally `SCORING_WEIGHTS`).
2. Install deps: `pip install -e .`
3. Put your call transcript into `transcript.txt` (or pass programmatically).
4. Run: `python -m my_project.main`
5. Outputs:
   - `lead_report.md` (full report)
   - Console logs (Crew run + final JSON score)

## Inputs you can pass to `kickoff`
- `transcript` (str) – raw transcript text
- `company` (str) – prospect company, optional
- `contact_name` (str) – prospect person, optional
- `product` (str) – your product/service brief
- `icp_criteria` (str) – describe your ICP in plain language
- `current_year` (int) – e.g., 2025
- `scoring_rubric` (str) – freeform description of your scoring philosophy

## Tiers
- **Hot**: total ≥ 70
- **Warm**: 40–69
- **Cold**: < 40

You can tune the deterministic tool in `tools/score_tool.py`.