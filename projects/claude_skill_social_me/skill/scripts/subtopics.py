#!/usr/bin/env python3
"""Subtopic frequency vs performance, across every platform in a run.

Two passes, because the machine is better at counting and you are better at naming:

  1. `candidates` dumps the most frequent 2 and 3 word phrases across all normalized items.
     Mechanical, reproducible, noisy. You read it and write the labels file.
  2. `score` takes that labels file and, for each subtopic, counts how many items run it and
     how those items performed against their own platform's median.

The number that matters is the **index**: median reach of the items matching a subtopic, over
the median reach of every item on that platform. Index 2.0 means the subtopic doubles the
platform median. Share tells you how crowded it is. High index + low share is a gap; high
share + index at or below 1.0 is a saturated angle.

Usage:
  python3 subtopics.py candidates --dir .            # then hand-write labels.json
  python3 subtopics.py score --dir . --labels labels.json

labels.json:
  { "usage limits": ["usage limit", "token limit", "rate limit", "hit the cap", "\\\\blimits?\\\\b"],
    "subagents":    ["subagent", "sub-agent", "agent team", "multiple agents"] }
Patterns are case-insensitive regexes matched against title/caption text.
"""
import argparse
import glob
import json
import os
import re
import statistics
from collections import Counter, defaultdict

STOP = set("""a an the and or but if then than that this these those is are was were be been being am
of to in on at by for with from as into over under about after before between out up down off again
i me my we our you your he she it its they them their what which who whom how when where why all any
both each few more most other some such no nor not only own same so too very can will just don now
s t d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn
wasn weren won wouldn get got make makes made use using used like new best top via let lets go going
com https http www vs amp """.split())

REACH_LABEL = {"youtube": "views", "instagram": "engagement", "tiktok": "plays", "x": "views"}


def clean(t):
    t = (t or "").lower()
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[#@]\w+", " ", t)
    t = re.sub(r"[^a-z0-9\s']", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def load_run(d):
    """{platform: [normalized records]} from norm-<platform>.json."""
    out = {}
    for f in sorted(glob.glob(os.path.join(d, "norm-*.json"))):
        p = os.path.basename(f)[len("norm-"):-len(".json")]
        with open(f, encoding="utf-8") as fh:
            out[p] = json.load(fh)
    if not out:
        raise SystemExit(f"no norm-*.json in {d} - run rank.py first")
    return out


def metric(rec):
    """Reach where a platform reports it, engagement where it does not (Instagram)."""
    return rec.get("reach") if rec.get("reach") is not None else rec.get("engagement")


def candidates(args):
    runs = load_run(args.dir)
    grams = Counter()
    seen_on = defaultdict(set)
    for plat, recs in runs.items():
        for r in recs:
            words = [w for w in clean(r.get("text")).split() if w not in STOP and len(w) > 2]
            for n in (2, 3):
                for i in range(len(words) - n + 1):
                    g = " ".join(words[i:i + n])
                    grams[g] += 1
                    seen_on[g].add(plat)
    print(f"\n## Phrase candidates ({sum(len(v) for v in runs.values())} items, "
          f"{len(runs)} platforms)\n")
    print("| phrase | count | platforms |")
    print("|---|---|---|")
    rows = [(g, c) for g, c in grams.items() if c >= args.min_count]
    rows.sort(key=lambda gc: (len(seen_on[gc[0]]), gc[1]), reverse=True)
    for g, c in rows[:args.limit]:
        print(f"| {g} | {c} | {', '.join(sorted(seen_on[g]))} |")
    print("\nWrite labels.json from these. Merge synonyms into one label - "
          "'usage limit', 'token limit' and 'hit the cap' are one demand signal, not three.\n")


def score(args):
    runs = load_run(args.dir)
    with open(args.labels, encoding="utf-8") as fh:
        labels = json.load(fh)
    compiled = {k: [re.compile(p, re.I) for p in v] for k, v in labels.items()}

    baseline, total = {}, 0
    for plat, recs in runs.items():
        vals = [metric(r) for r in recs if metric(r) is not None]
        baseline[plat] = statistics.median(vals) if vals else None
        total += len(recs)

    plats = sorted(runs)
    print(f"\n## Subtopics - frequency vs performance ({total} items)\n")
    print("Index = median reach of matching items / that platform's median. "
          "n/a means no matches or no baseline.\n")
    header = "| subtopic | items | share |" + "".join(f" {p} n | {p} index |" for p in plats)
    print(header)
    print("|---|---|---|" + "---|---|" * len(plats))

    rows = []
    for name, pats in compiled.items():
        cells, n_all, best_index, best_plat = [], 0, 0.0, None
        for plat in plats:
            hits = [r for r in runs[plat]
                    if any(p.search(r.get("text") or "") for p in pats)]
            n_all += len(hits)
            vals = [metric(r) for r in hits if metric(r) is not None]
            if vals and baseline.get(plat):
                idx = statistics.median(vals) / baseline[plat]
                cells.append(f" {len(hits)} | {idx:.2f}x |")
                if len(hits) >= args.min_hits and idx > best_index:
                    best_index, best_plat = idx, plat
            else:
                cells.append(f" {len(hits)} | n/a |")
        share = n_all / total if total else 0
        print(f"| {name} | {n_all} | {share*100:.0f}% |" + "".join(cells))
        rows.append((name, n_all, share, best_index, best_plat))

    gaps = [r for r in rows if r[3] >= args.gap_index and r[2] <= args.gap_share]
    sat = [r for r in rows if r[2] >= args.sat_share and r[3] <= 1.0]
    print(f"\n**Gap candidates** (index >= {args.gap_index} on a platform with >= {args.min_hits} "
          f"items, and share <= {args.gap_share*100:.0f}%):")
    print("\n".join(f"- {n}: {s*100:.0f}% of items, {bi:.2f}x on {bp}"
                    for n, c, s, bi, bp in gaps) or "- none")
    print(f"\n**Saturated** (share >= {args.sat_share*100:.0f}% and no platform above 1.0x):")
    print("\n".join(f"- {n}: {c} items, {s*100:.0f}% of the pull"
                    for n, c, s, bi, bp in sat) or "- none")
    print("\nThese two lists are candidates, not conclusions. Confirm each against the actual "
          "items before it goes in the brief.\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("candidates")
    c.add_argument("--dir", default=".")
    c.add_argument("--min-count", type=int, default=3)
    c.add_argument("--limit", type=int, default=45)
    c.set_defaults(fn=candidates)
    s = sub.add_parser("score")
    s.add_argument("--dir", default=".")
    s.add_argument("--labels", required=True)
    s.add_argument("--min-hits", type=int, default=2)
    s.add_argument("--gap-index", type=float, default=1.3)
    s.add_argument("--gap-share", type=float, default=0.15)
    s.add_argument("--sat-share", type=float, default=0.25)
    s.set_defaults(fn=score)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
