# Opus 5.5 vs GPT-6 Sol, on real agents

The harness behind the video. Two Hermes Agent profiles with the same SOUL, skills, and memory,
one on `claude-opus-5-5`, one on `gpt-6-sol`. Same prompt file to each. Outputs judged by
looking, playing, or against a known answer.

This is not a benchmark. It is 8 jobs I actually run, with the model swapped underneath.

## Why this shape

Every model comparison I found tests the models as assistants: "build me a website," "make me a
game," judged by eye. Fair, and 3 of these 8 are that. The other 5 are jobs my agents already do
every day (a code review, a morning brief, a channel analysis, an ad, a reel). Those have ground
truth: I know the answer, so one model is visibly right.

Nate Herk's "I Tested Opus 5.5 vs GPT-6 Sol on 10 Real Use Cases" (2026-09-22) is the reference.
Three of these cases are his shapes on my data; five he could not run.

## The 8

| # | Case | Prompt | Judged by |
|---|---|---|---|
| 1 | Website design | `prompts/1-website.md` | looking, split screen |
| 2 | Code review on a real commit | `prompts/2-review.md` | catches a known stale line or not |
| 3 | Write an ad from a swipe file | `prompts/3-ad.md` | reading; closest existing script named |
| 4 | Build a game | `prompts/4-game.md` | playing |
| 5 | Channel analytics, what to make next | `prompts/5-videos.md` | finds the retention pattern the owner already knows |
| 6 | Cut a vertical reel with HyperFrames | `prompts/6-reel.md` | watching both; `hyperframes check --strict` |
| 7 | Morning content brief (a skill both profiles have) | `prompts/7-brief.md` | same 3 picks? numbers from the files only? |
| 8 | The bill, then model-per-bot routing | not a prompt | two invoices, one `config.yaml` |

## Run it

```bash
bash setup.sh                       # two profiles from an existing one; edit model ids at the top
# drop your files in inputs/ (see inputs/README.md)
bash run-all.sh                     # every case, both models, in parallel
CASES="5-videos 7-brief" bash run-all.sh   # a subset
```

Outputs land in `runs/<profile>/<case>/`: `out.txt` (full agent transcript), `time.txt`, and the
artifact (`landing.html`, `game.html`, the rendered reel). `runs/` and `inputs/` are gitignored;
this repo is the harness, not the results.

## Results

Filled in after the run. Model ids as reported by each agent.

| # | Case | Opus 5.5 | GPT-6 Sol | Call |
|---|---|---|---|---|
| 5 | Analytics | Found "10 to 20 min holds, courses die, viewers stop at the same point regardless of length"; 72 of 81 subs from that band; 0 em dashes | Recommended under 5 minutes (highest %, but those videos earned 0 subs); 4 em dashes after being told none | Opus |
| 7 | Brief | Newest idea, flagged stale data, 6 notes on what it could not verify | Oldest idea in the file (a dead lane), dated the brief to the stale data | Opus |
| 1 | Website | | | |
| 2 | Review | | | |
| 3 | Ad | | | |
| 4 | Game | | | |
| 6 | Reel | | | |
| 8 | Bill | | | |

## Notes that cost me time

- Hermes has no bare `openai` provider. Subscription login is `openai-codex`. An API key is
  `provider: custom` + `model.base_url: https://api.openai.com/v1` + `model.api_key`.
- A cron created before a provider change keeps the old provider (`provider_snapshot`). Pin it:
  `hermes -p <p> cron edit <id> --provider openai-codex --model gpt-6-sol`.
- `hermes profile create` copies the template's `model.base_url`; a new profile can inherit an
  Ollama endpoint. Check `config.yaml` before the first call.
- Both profiles need the same skills installed or the comparison is unfair. `setup.sh` copies
  the whole `skills/` tree from the base profile.
