# social-me: a Claude Code skill that tells you what to make next

Give it a topic. It pulls the real top content on YouTube, Instagram, TikTok and
X through the Apify MCP server, reads the winning YouTube transcripts and their
comment sections, computes every number with a script instead of by eye, and
writes a brief that ends in a decision: which video, short, carousel or post gets
made next.

Built live in the video in five steps. The prompt that builds it is in
[PROMPT.md](PROMPT.md) — it is five lines.

📺 **Video:** [UPDATE with link]

---

## The five steps

| Step | What happens |
|---|---|
| 1 | Choose where to build it — Claude on the web, the desktop app, or Claude Code in the terminal (this build uses Claude Code) |
| 2 | Describe the agent in plain English. Claude writes the skill, the scripts and the brief template |
| 3 | Give it tools — connect the Apify MCP server so it can reach the platforms |
| 4 | Harden it with Matt Pocock's `grilling` skill, which asks adversarial questions until the weak parts show |
| 5 | Schedule it as a cloud routine so it runs without you |

## Quick start

**1. Install the skill**

```bash
git clone https://github.com/tylerprogramming/ai.git
cp -r ai/claude_skill_social_me/skill ~/.claude/skills/social-me
```

Or skip the copy and build your own from [PROMPT.md](PROMPT.md) — that is what
the video does, and you will understand it better.

**2. Connect Apify**

Sign up at [apify.com](https://apify.com/) (free tier includes $5 of credit),
then go to [mcp.apify.com](https://mcp.apify.com/), turn on **Add Apify token**,
and copy the command it gives you:

```bash
claude mcp add apify "https://mcp.apify.com/" -t http --header "Authorization: Bearer YOUR_TOKEN_HERE"
```

Verify with `/mcp` inside Claude Code. It will ask you to authenticate once.

**3. Reload skills**

A new skill will not show up in an already-running session. Exit Claude Code and
resume — it prints the resume command on the way out. This trips everyone up.

**4. Run it**

```
/social-me
```

It asks for a topic and which platforms. First run takes a few minutes.

## What you get back

A brief, grounded in the pulled data. From the run in the video:

```
104 items pulled, 26 per platform, 3 transcripts read

- The topic is barely covered: only 3 of 26 videos in the pool
  have "skill" in the title
- Sub-agent content is underperforming, not unwanted
- Usage limits are the loudest complaint on all four platforms
```

Every number there was computed by `scripts/rank.py` from the raw JSON on disk.
None of it was written by the model into prose. That distinction is the whole
design.

## What's in here

```
PROMPT.md              the five-line prompt that builds the skill
skill/
  SKILL.md             the skill itself
  scripts/
    rank.py            normalizes and ranks the pulled records
    yt_transcript.py   pulls transcripts for the top videos
    comments.py        pulls and summarizes comment sections
    subtopics.py       clusters the pool into subtopics
  templates/brief.md   the brief format
  reference/actors.md  verified Apify actor calls, fields and gotchas
```

## The gotchas, up front

These cost real time. `reference/actors.md` has the full list.

- **YouTube has no 3-month window.** The actor's `dateFilter` maxes out at
  `month`, and setting `oldestPostDate` forces sorting to newest, which destroys
  the view ranking. So "last 3 months" becomes 30 days on YouTube. Say so in the
  brief rather than pretending otherwise.
- **Instagram's hashtag route returns the recency feed**, not the top posts. Pull
  by hashtag for patterns, but keep a handle watchlist and scrape those directly
  for anything you plan to rank.
- **Actor tool names shift between sessions.** Some sessions expose dedicated
  tools, others only `call-actor`. Use the actor full name through `call-actor`
  and it always works.
- **Apify is not free.** The free tier gives you $5 of credit, which is enough to
  try this several times over.

## Requirements

- Claude Code with a paid Claude subscription
- An Apify account (free tier is fine to start)
- Node.js, for the MCP server

## Credits

The hardening step uses [Matt Pocock's skills](https://github.com/mattpocock),
now available as an official Claude Code plugin.
