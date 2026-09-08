# The prompt

This is the prompt from the video, verbatim. Paste it into Claude Code and it
builds the skill. Nothing else is needed to start.

```
Create a Claude Code skill called social-me.

It takes a topic and researches it across multiple platforms using Apify:
YouTube, Instagram, TikTok and X.

It reads the top YouTube videos' transcripts to find what is working and where
the content gaps are.

It gives me a brief with content ideas.

Ground everything in real data. Never invent numbers.
```

That is the whole thing. Claude writes the skill file, the scripts and the brief
template from those five lines.

## Why it is so short

The instruction that does the most work is the last one: **never invent
numbers.** Without it the model will happily write "this video got 340K views"
because it reads plausible. With it, Claude builds a `rank.py` that computes
every figure from the pulled data instead of writing figures into prose. The
constraint is what forces the scripts to exist.

The second most useful line is naming the tool (`using Apify`). Say the platform
and the model picks the actors, the auth flow and the field names. Leave it out
and it invents an API.

## Step 4: hardening it

Once the skill exists, run it through a round of adversarial questions. In the
video this is Matt Pocock's `grilling` skill, now an official Claude Code plugin:

```
/grilling

I want to harden social-me.
```

It asks a round of questions, you answer, it asks another round. On this build it
caught three real defects:

1. **The Instagram hashtag route returns the recency feed**, so all 26 items came
   back hours old with almost no engagement. Fix: two-stage pull, hashtags for
   patterns plus a handle watch list scraped every time.
2. **The YouTube actor has no 3-month window** and setting post dates forces
   sorting by newest, which destroys view ranking. Fix: fix YouTube at 30 days
   and say so in the brief.
3. **Transcript path was wrong.** Fix: try Apify first, fall back to YouTube.

None of those are visible until something runs against live data. That is the
whole point of the step.

## Step 5: scheduling it

```
/schedule social-me every two days at 7am
```

`/schedule` creates a cloud routine that runs whether or not your machine is on.
`/loop` does the same thing locally, which is fine but needs the computer awake
and gets reset on restart. A VPS is the third option and the most durable.

Note the routine is created in **UTC**, so set the hour accordingly.
