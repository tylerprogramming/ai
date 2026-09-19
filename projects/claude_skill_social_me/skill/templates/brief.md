# Social Brief - {topic}
**Date:** {YYYY-MM-DD} | **Scope:** {platforms} | **Window:** {window}
**Pulled:** {n} items ({per-platform counts}) | **Transcripts:** {n} | **Comments read:** {n}
**Failed / skipped / limited:** {stage + reason, or "none"}

> Standing caveats to restate every run: YouTube's window is **30 days**, not the requested window.
> Instagram has **no reach data** at all, so its column is **engagement per follower**.

## What to make first
{One line. The idea, the platform, the format.}
{Two or three lines on why, each pointing at a number or a quote below.}

---

## Per platform

### {Platform}
{rank.py leaderboard, pasted as printed, including the medians and the outlier block}

**Working:**
- {pattern} - "{verbatim title or caption}" ({handle}, {reach}, {Nx} their follower count) {url}
- {pattern} - {second real example}

**Hook read** (top {depth}, first 60s, verbatim):
> "{hook}"
> - {handle}, {reach} {url}
> Structure: {segments, where the demo starts, where the CTA lands}

{Repeat per platform. If a platform returned nothing usable, say exactly that and why.}

---

## Subtopics - frequency vs performance
{subtopics.py score table, pasted as printed}

{One or two lines naming what the table actually shows. The labels are yours; every number
under them is computed.}

## What the comments say

### Reaction - which promise landed ({n} top comments)
> "{verbatim}"
> - {author}, {votes} votes, on {video title}

### Demand - what people are stuck on ({n} question-shaped of {m} read, {x}%)
**"{theme you named}" - {n} people asked this:**
> "{verbatim question}"
> - {author}, on {video title}
> "{second verbatim question}"
> - {author}

{Demand quotes replace inferred demand. If the comment passes found nothing on a theme, that
theme is a hunch, not a gap.}

## Outliers worth studying
- {title} - {handle}, {reach}, {Nx} their follower count - {what it did differently} {url}

## Gaps (make these)
- **{angle}** - Demand: {a quoted question, or a subtopic index with its share}.
  Coverage: {a count you can point at}. Platform: {x}.

## Saturated (skip or differentiate)
- **{angle}** - {n} of {total} items run it, index {x} on {platform}. To differentiate: {angle}.

## Hunches (not proven by this data)
- {idea} - would be confirmed by {the specific pull that would settle it}

## Content ideas
| # | Idea | Platform / format | Grounded in |
|---|---|---|---|
| 1 | {title or hook} | {long-form / short / carousel / build post} | {the gap + the proven pattern it borrows} |

{One line: which idea first, and why it beats the others.}

## Sources
Raw data in this folder: `raw-*.json` ({n} items each, exactly as Apify returned them).
Computed metrics in `norm-*.json`. Subtopic labels in `labels.json`.
Transcripts in `transcripts/`. Comment datasets: `raw-yt-comments-top.json`,
`raw-yt-comments-new.json`{, `raw-tiktok-comments.json`}.
