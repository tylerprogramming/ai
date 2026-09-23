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

Run 2026-09-23, same prompt file to each profile. Model ids as reported by the agents. Every artifact is in `runs/<profile>/<case>/`.

| # | Case | Opus 5.5 | GPT-6 Sol | Call |
|---|---|---|---|---|
| 1 | Website | 12.6 KB, 6 blocks, 2 CTAs (asked for one). Least-sure line: "Your first brief arrives the next morning," with the reason (no public Skool API) and a safer rewrite. | 8.2 KB, 5 blocks, 1 CTA as asked. Opened Chrome at phone width to check the layout. | judge by eye |
| 2 | Code review | Led with a logic bug: a deleting run logged as idle because the result dict lacks a `wrote` key. Fix given. Read the diff only. | Led with a UX limit (`.limit(20)`), then found a read-then-delete race that removes a row the owner just ticked. **Ran the test suite** and reported the gap. | Sol |
| 3 | Ad | Hook: "Your most active member hasn't posted in two weeks. Did you notice?" 87 words by `wc`, 0 em dashes. Flagged that the 14% proof number comes from a mockup screen. | Hook: "Your member count won't tell you who stopped showing up." Proof line is a feature list. 1 em dash after being told none. | Opus |
| 4 | Game | 14.4 KB. Browser tool timed out twice, so it wrote a Node script to drive headless Chrome with real keypresses. Played to level 8, 3,200 pts, then found the speed cap (emails can't arrive faster than 0.9s) and asked whether that's intended. | 21.1 KB. Played one round in headless Chrome, 1,000 pts, deliberately mislabelled 3 to verify game over. Fixed long subjects overflowing cards. | judge by playing |
| 5 | Analytics | "10 to 20 min holds, over 20 dies, viewers stop at the same point regardless of length." 72 of 81 subs from that band. Named "Full Course" as the losing pattern with 5 examples. 0 em dashes. | "Under 5 minutes holds best" (highest %, but those videos earned 0 subs). Recommended a CS-basics video for a Claude Code channel. 4 em dashes. | Opus |
| 6 | Reel | 1080x1920, 45.0s, 13.6 MB, `check --strict` pass. Caught the broken SRT (one line repeated), re-transcribed 3 cuts. Pulled 5 reference frames and a face crop before designing. "Give the caption sync one pass." | 1080x1920, 45.0s, 5.5 MB, `check --strict` zero findings, 31.6s render. Caught the broken SRT, repaired captions from audio. Stayed on 0.8.17 when the upgrade failed verification. | tie (both fixed an input bug I didn't know was there) |
| 7 | Brief | Picked the newest idea, flagged the analytics as stale, 6 notes on what it could not verify and why it didn't run yt-search. | Picked the oldest idea in the file (a dead lane this week), dated the brief to the stale data. | Opus |
| 8 | Bill | pending: both profiles fire the 8am repo check from 2026-09-24; invoices compared after 3 days | | |

Tally on the judged rows: Opus 3, Sol 1, tie 1. Website and game are for the viewer.

What held across all 7: Opus questions its own output and the inputs more; Sol follows the literal instruction more closely and verifies by running things. Sol used em dashes in 3 of 7 outputs after being told not to; Opus in 0.

## Two bugs in the harness, fixed

- `hermes chat` writes relative to the profile workdir, not the shell's cwd. Both models wrote `~/landing.html` and `~/game.html`, and the second overwrote the first. `run-all.sh` now puts the absolute case folder in the prompt. Sol's game was re-run after the fix.
- The reel prompt pointed both models at a stretch of transcript that was corrupted (a whisper repeat loop from an earlier run). Neither model was told. Both found it. Left in on purpose; it is the best beat.

## Notes that cost me time

- Hermes has no bare `openai` provider. Subscription login is `openai-codex`. An API key is
  `provider: custom` + `model.base_url: https://api.openai.com/v1` + `model.api_key`.
- A cron created before a provider change keeps the old provider (`provider_snapshot`). Pin it:
  `hermes -p <p> cron edit <id> --provider openai-codex --model gpt-6-sol`.
- `hermes profile create` copies the template's `model.base_url`; a new profile can inherit an
  Ollama endpoint. Check `config.yaml` before the first call.
- Both profiles need the same skills installed or the comparison is unfair. `setup.sh` copies
  the whole `skills/` tree from the base profile.
