# inputs/ (gitignored)

Put your own files here. The prompts reference them by name:

| File | Used by | What it is |
|---|---|---|
| `analytics-50-videos.json` | 5-videos, 7-brief | Your channel's per-video analytics. Shape: `{"month": {"perVideo": [{"title","views","avgViewPct","avgViewDuration","durationSeconds","isShort"}, ...]}}`. The `yt-analytics` skill writes this. |
| `status.md`, `video-ideas.md` | 7-brief | Your pipeline state and idea list, any markdown. |
| `attend-ad-swipe.md` | 3-ad | A swipe file of ad scripts that worked for your product. |
| `<video>.mp4` + `<video>.srt` | 6-reel | A long video and its transcript. Edit the timestamps in `prompts/6-reel.md`. |

Nothing in this folder is committed. The `.gitignore` covers it.
