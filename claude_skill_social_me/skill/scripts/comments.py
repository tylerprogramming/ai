#!/usr/bin/env python3
"""Two comment passes: what resonated, and what people are still stuck on.

They are different signals and the brief must not mix them up:

  REACTION (top-sorted comments) - which promise landed. Title and thumbnail input.
      Measured 2026-08-29: only 3 of 25 top comments on a 219-comment video contained a
      question. The top of a comment section is praise, jokes and the creator's own link.
  DEMAND (newest-sorted comments) - what people cannot do yet. Content input.
      Filtered to question-shaped comments, then clustered by their shared keyword.

Nothing here is invented: every line printed is a verbatim comment with its author and score.
Clustering is mechanical (shared keywords). Naming the clusters is your job, not the script's.

Usage:
  python3 comments.py --top raw-yt-comments-top.json --new raw-yt-comments-new.json
  python3 comments.py --new raw-yt-comments-new.json --tiktok raw-tiktok-comments.json
"""
import argparse
import json
import re
from collections import Counter, defaultdict

STOP = set("""wait okay yeah hey lol bro guys man sir also still even much many way ways thing things
a an the and or but if then than that this these those is are was were be been being am
of to in on at by for with from as into over under about after before between out up down off again
i me my we our you your he she it its they them their what which who whom how when where why all any
both each few more most other some such no nor not only own same so too very can will just don now
do does did doing have has had having would could should may might must shall im ive dont cant thats
one two get got make made use using used like new thanks thank great video please would really need
""".split())

QUESTION = re.compile(
    r"\?|^\s*(how|what|which|why|when|where|can|could|does|do|is|are|any(one|body)|has|would)\b",
    re.I)
LINKISH = re.compile(r"https?://|t\.me/|\bsubscribe\b|\bmy course\b", re.I)


def norm_yt(items, source):
    out = []
    for c in items:
        t = (c.get("comment") or "").strip()
        if not t:
            continue
        out.append({
            "text": t, "author": c.get("author"), "score": c.get("voteCount") or 0,
            "replies": c.get("replyCount") or 0, "owner": bool(c.get("authorIsChannelOwner")),
            "where": c.get("title") or c.get("videoId"), "platform": "youtube",
            "source": source, "cid": c.get("cid"),
        })
    return out


def norm_tt(items, source):
    """TikTok comment rows. Field names vary by actor build, so try the known aliases."""
    out = []
    for c in items:
        t = (c.get("text") or c.get("comment") or "").strip()
        if not t:
            continue
        out.append({
            "text": t,
            "author": (c.get("uniqueId") or c.get("username")
                       or (c.get("user") or {}).get("uniqueId")),
            "score": c.get("diggCount") or c.get("likesCount") or 0,
            "replies": c.get("replyCommentTotal") or c.get("replyCount") or 0,
            "owner": False,
            "where": c.get("videoWebUrl") or c.get("submittedVideoUrl"),
            "platform": "tiktok", "source": source, "cid": c.get("cid"),
        })
    return out


def read(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("items", d) if isinstance(d, dict) else d


def words(t):
    t = re.sub(r"https?://\S+", " ", (t or "").lower())
    t = re.sub(r"'", "", t)                       # that's -> thats, so the stoplist catches it
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return [w for w in t.split() if w not in STOP and len(w) > 2]


def show(c, n=240):
    body = " ".join(c["text"].split())
    body = body if len(body) <= n else body[: n - 1] + "…"
    return f'> "{body}"\n>   - {c["author"] or "unknown"}, {c["score"]} votes, {c["replies"]} replies'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", action="append", default=[], help="top-sorted comment dataset(s)")
    ap.add_argument("--new", action="append", default=[], help="newest-sorted comment dataset(s)")
    ap.add_argument("--tiktok", action="append", default=[], help="TikTok comment dataset(s)")
    ap.add_argument("--show", type=int, default=8)
    ap.add_argument("--min-cluster", type=int, default=2)
    a = ap.parse_args()

    reaction, demand_pool = [], []
    for f in a.top:
        reaction += norm_yt(read(f), "top")
    for f in a.new:
        demand_pool += norm_yt(read(f), "new")
    for f in a.tiktok:
        demand_pool += norm_tt(read(f), "tiktok")
    if not reaction and not demand_pool:
        raise SystemExit("nothing to read - pass --top, --new or --tiktok")

    if reaction:
        clean = [c for c in reaction if not c["owner"] and not LINKISH.search(c["text"])]
        clean.sort(key=lambda c: c["score"], reverse=True)
        print(f"\n## Reaction - what landed ({len(reaction)} top comments, "
              f"{len(reaction) - len(clean)} dropped as creator or promo)\n")
        for c in clean[:a.show]:
            print(show(c) + "\n")

    # Questions hide in the top pass too, so read everything - but the two passes overlap,
    # and the same comment printed twice reads as two people asking.
    pool, seen = [], set()
    for c in demand_pool + reaction:
        k = c.get("cid") or (c["author"], c["text"])
        if k not in seen:
            seen.add(k)
            pool.append(c)
    qs = [c for c in pool if not c["owner"] and QUESTION.search(c["text"])
          and not LINKISH.search(c["text"])]
    print(f"\n## Demand - what people are stuck on\n")
    print(f"{len(qs)} question-shaped of {len(pool)} comments read "
          f"({len(qs)/len(pool)*100:.0f}%).\n")
    if not qs:
        print("No questions found. Say that in the brief; do not infer demand from praise.\n")
        return

    freq = Counter(w for c in qs for w in set(words(c["text"])))
    clusters = defaultdict(list)
    for c in qs:
        ws = [w for w in set(words(c["text"])) if freq[w] >= a.min_cluster]
        key = max(ws, key=lambda w: freq[w]) if ws else "(unclustered)"
        clusters[key].append(c)

    for key, group in sorted(clusters.items(), key=lambda kv: len(kv[1]), reverse=True):
        if len(group) < a.min_cluster:
            continue
        print(f"### \"{key}\" - {len(group)} questions\n")
        for c in sorted(group, key=lambda c: c["score"], reverse=True)[:3]:
            print(show(c) + "\n")
    singles = sum(1 for g in clusters.values() if len(g) < a.min_cluster)
    print(f"_{singles} one-off questions not shown. Keyword clustering is mechanical - "
          f"name the real themes yourself from the quotes above._\n")


if __name__ == "__main__":
    main()
