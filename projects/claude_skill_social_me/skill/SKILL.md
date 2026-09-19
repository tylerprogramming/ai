---
name: social-me
description: Research a topic across YouTube, Instagram, X and TikTok with Apify, read the top YouTube videos' transcripts and comments, and return a brief of what is working, where the gaps are, and what to make next. Every number is pulled or computed from real data, never invented. Triggers on - social me, research this topic across platforms, what is working on social, cross-platform research, find the content gaps, topic brief, scout a niche, what should I make about.
---

# social-me

Give it a topic. It pulls the real top content on four platforms, reads the winners' transcripts and
their comment sections, computes every number with a script instead of by eye, and writes a brief
that ends in a decision: which video, short, carousel or post gets made next.

## Inputs

| input | default | notes |
|---|---|---|
| topic | required | e.g. "claude code skills", "AI agents for solopreneurs" |
| platforms | all four | `youtube` `instagram` `x` `tiktok` |
| window | last 3 months | **YouTube is fixed at 30 days** - the actor has no 3-month filter that survives view sorting. Say so in the brief. |
| per_platform | 25 | items pulled per platform |
| depth | 3 | YouTube videos read in full (transcript + comments) |

Everything runs every time. There is no quick mode: the expensive stages are priced per item, not
per run, so `depth` and `per_platform` are the cost dials.

## Where it writes

`~/content/research/social/YYYY-MM-DD-<topic-slug>/`

```
brief.md                    the deliverable
raw-<platform>.json         exactly what Apify returned (the audit trail)
raw-instagram-profiles.json follower counts for the IG accounts in the pull
raw-yt-comments-top.json    reaction pass
raw-yt-comments-new.json    demand pass
raw-tiktok-comments.json    demand pass (optional)
norm-<platform>.json        normalized records from rank.py
labels.json                 the subtopic labels you wrote for this run
transcripts/                <videoid>.txt
```

Instagram handles discovered along the way get appended to a watchlist file
(`watchlist.md`, path is yours to choose) with their follower count, their engagement rate at
discovery, and a `[found YYYY-MM-DD via <topic>]` stamp, so the next run scrapes them directly
instead of rediscovering them.

## Process

### 0. Load context first
Read whatever notes you keep on your own voice, your channel's history, and your platform
watchlists, then check your existing research and idea files for prior work on this topic. A gap
you have already covered is not a gap.

If you have no such files yet, skip this step - the skill works without them, it is just less
opinionated about what counts as new.

### 1. Pull, and get the raw data onto disk
`reference/actors.md` has the verified call for every actor and every gotcha that has bitten this
skill. Follow it. Seven runs: YouTube search, TikTok search, X search, Instagram hashtag, Instagram
profiles, YouTube subtitles, YouTube comments.

Then curl each dataset straight to a file. No token needed, full fidelity, nothing retyped:
```bash
curl -s "https://api.apify.com/v2/datasets/<datasetId>/items?format=json&clean=true" -o raw-<platform>.json
```
Do that before you look at anything.

If a stage returns nothing or errors, write that line into the brief and keep going. A brief that
says "Instagram returned no usable items" is worth more than a brief with a plausible Instagram
section in it.

### 2. Rank with the script, not by eye
```bash
python3 scripts/rank.py --platform youtube   --in raw-youtube.json   --out norm-youtube.json --top 10
python3 scripts/rank.py --platform instagram --in raw-instagram.json --profiles raw-instagram-profiles.json \
                        --out norm-instagram.json --top 10
```
Paste its tables into the brief as printed. Missing values print `n/a` and stay `n/a`.

The signal to chase is **reach per follower**. A 768-follower account at 44K views is a stronger read
than a 149K-follower account at 367K. On Instagram there is no reach at all, so the equivalent is
**engagement per follower** - call it that, every time, and never call it reach.

### 3. Read the winners
**Transcripts.** yt-dlp is blocked (`YTDLP_FAILED` on every video, 2026-08-29), so go straight to
Apify with all `depth` videos as `startUrls` in ONE run, and save `subtitles[].plaintext` to
`transcripts/<videoid>.txt`. `scripts/yt_transcript.py` stays as the cheap fallback for the day
YouTube relents.

From each transcript pull the **first 60 seconds verbatim** (that is the hook, quote it), what the
video actually delivers in one line, and the structure - segments, demo, where the CTA lands.

**Comments, two passes, never mixed:**
```bash
python3 scripts/comments.py --top raw-yt-comments-top.json --new raw-yt-comments-new.json \
                            --tiktok raw-tiktok-comments.json
```
- **Reaction** (`TOP_COMMENTS`, 25/video): which promise landed. Title and thumbnail input.
- **Demand** (`NEWEST_FIRST`, 100/video): what people are stuck on. Content input.

The top of a comment section is praise, jokes and the creator's own pinned link. Measured on a
219-comment video: 3 of 25 top comments contained a question, against 31% of the newest ones.
**Never quote a reaction comment as evidence of demand.**

For TikTok, Instagram and X posts, read the top items' opening line, the format, the length and the
CTA. Comment-gates especially: they are the Instagram norm and the TikTok exception.

### 4. Find the patterns and the gaps
**Subtopics, mechanically, then labelled by you:**
```bash
python3 scripts/subtopics.py candidates --dir .                      # n-grams, noisy on purpose
# read them, merge synonyms, write labels.json
python3 scripts/subtopics.py score --dir . --labels labels.json
```
The index is median reach of matching items over that platform's median. High index + low share is a
gap candidate. High share + index at or below 1.0 is saturated. Both lists are candidates: confirm
each against the actual items before it reaches the brief.

A **gap** needs both halves from the data: demand (a repeated question from the comment pass, or a
subtopic index above 1.3 on thin share) and thin coverage (a count you can point at). Anything with
only one half goes under "hunches", not gaps.

### 5. Write the brief
Use `templates/brief.md`. The new evidence **replaces inference, it does not stack on top of it** -
quote a real question instead of arguing from an adjacent video's performance, and cite the subtopic
table instead of hand-counting title shapes. Every number carries its source. Every claim points at
a real item.

### 6. Hand off
Close with the single thing to make first and the skill that makes it: `/yt-package` for long-form,
`/yt-shorts` for shorts, `/instagram-writer` for a carousel, `/linkedin-writer` for the build post.

## Rules

- **Never invent a number, a title, a handle, or a quote.** If it is not in the raw JSON, a
  transcript, or a comment file, it does not go in the brief.
- Numbers come from the scripts. Do not do the arithmetic in your head.
- Quote hooks and comments verbatim, in quotation marks, with the author and the URL.
- Engagement is not reach. Label the Instagram column honestly or do not print it.
- Say what failed. Partial and honest beats complete and made up.
- Follow `BRAIN/tyler-voice.md`. No em dashes. No money amounts in proposed titles. The subject is
  Claude Code automation, never platform or growth strategy - if an idea could headline a YouTube
  growth channel, rewrite it as an automation insight that transfers to anyone's repetitive work.
- Tyler is a software engineer. Ideas should show the build, not pitch beginners.
- Report the ideas, do not schedule or publish anything.
