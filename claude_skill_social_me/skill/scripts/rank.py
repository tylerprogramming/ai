#!/usr/bin/env python3
"""Normalize + rank raw Apify social data so every number in the brief is computed, not eyeballed.

Takes the raw dataset items you saved from an Apify actor run, maps each platform's field
names onto one shape, computes reach / engagement / outlier metrics, and prints a markdown
leaderboard you can paste straight into the brief.

Missing values stay missing. A field the platform did not return prints as `n/a` and is
excluded from every average - it is never coerced to 0.

Usage:
  python3 rank.py --platform youtube   --in raw-youtube.json   --out norm-youtube.json
  python3 rank.py --platform instagram --in raw-instagram.json --out norm-instagram.json --top 10
  python3 rank.py --platform tiktok    --in raw-tiktok.json
  python3 rank.py --platform x         --in raw-x.json

Input may be a bare JSON array, or an object with an "items" / "data" array.
"""
import argparse
import json
import re
import statistics
import sys
from datetime import datetime, timezone

# field_name -> tuple of candidate paths in the raw item, first hit wins
MAPS = {
    "youtube": {
        "text":      ("title",),
        "url":       ("url", "videoUrl"),
        "author":    ("channelName", "channelUsername"),
        "followers": ("numberOfSubscribers",),
        "reach":     ("viewCount",),
        "likes":     ("likes", "likeCount"),
        "comments":  ("commentsCount", "commentCount"),
        "shares":    (),
        "date":      ("date", "uploadDate"),
        "duration":  ("duration",),
        "kind":      ("type",),
    },
    "instagram": {
        "text":      ("caption",),
        "url":       ("url",),
        "author":    ("ownerUsername",),
        "followers": ("ownerFollowersCount",),
        "reach":     ("videoPlayCount", "videoViewCount"),
        "likes":     ("likesCount",),
        "comments":  ("commentsCount",),
        "shares":    (),
        "date":      ("timestamp",),
        "duration":  ("videoDuration",),
        "kind":      ("productType", "type"),
    },
    "tiktok": {
        "text":      ("text",),
        "url":       ("webVideoUrl", "url"),
        "author":    ("authorMeta.name", "authorMeta.nickName"),
        "followers": ("authorMeta.fans",),
        "reach":     ("playCount",),
        "likes":     ("diggCount",),
        "comments":  ("commentCount",),
        "shares":    ("shareCount",),
        "date":      ("createTimeISO",),
        "duration":  ("videoMeta.duration",),
        "kind":      (),
    },
    "x": {
        "text":      ("text", "fullText"),
        "url":       ("url", "twitterUrl"),
        "author":    ("author.userName", "author.screen_name"),
        "followers": ("author.followers", "author.followersCount"),
        "reach":     ("viewCount",),
        "likes":     ("likeCount",),
        "comments":  ("replyCount",),
        "shares":    ("retweetCount",),
        "date":      ("createdAt",),
        "duration":  (),
        "kind":      (),
    },
}

REACH_LABEL = {"youtube": "views", "instagram": "plays", "tiktok": "plays", "x": "views"}


def dig(item, path):
    # Apify's `fields` projection returns FLATTENED keys ("authorMeta.name"), while a raw
    # dataset dump is nested. Handle both.
    if isinstance(item, dict) and path in item:
        return item[path]
    cur = item
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def pick(item, paths):
    for p in paths:
        v = dig(item, p)
        if v not in (None, "", []):
            return v
    return None


def as_int(v):
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        # Instagram sends -1 for a post with likes hidden. That is "unknown", not a count,
        # and letting it through makes an engagement rate go negative.
        return int(v) if v >= 0 else None
    if isinstance(v, str):
        s = v.replace(",", "").strip()
        m = re.match(r"^([\d.]+)\s*([KMB]?)", s, re.I)
        if not m:
            return None
        try:
            n = float(m.group(1))
        except ValueError:
            return None
        n *= {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2).upper()]
        return int(n)
    return None


def dur_seconds(v):
    """'12:34' / '1:02:03' / 74 -> seconds."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    parts = str(v).strip().split(":")
    if not all(p.strip().isdigit() for p in parts):
        return None
    secs = 0
    for p in parts:
        secs = secs * 60 + int(p)
    return secs


def parse_date(v):
    if not v:
        return None
    s = str(v).strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%d", "%a %b %d %H:%M:%S %z %Y"):
        try:
            d = datetime.strptime(s, fmt)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:  # bare ISO with offset
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def load_profiles(path):
    """Instagram `details` items -> {username: followersCount}.

    Instagram never reports plays on this account tier, so followers are the only way to
    size an account. Without them a 198K-follower post and a 104-follower post look the same.
    """
    out = {}
    for a in load(path):
        u = (a.get("username") or "").lower()
        f = as_int(a.get("followersCount"))
        if u and f:
            out[u] = f
    return out


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for key in ("items", "data", "results"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    if not isinstance(data, list):
        sys.exit("input JSON is not a list of items (or {items:[...]})")
    return data


def normalize(items, platform, profiles=None):
    m = MAPS[platform]
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        if it.get("error") or it.get("noResults"):   # actor status rows, not content
            continue
        rec = {
            "platform": platform,
            "text": (pick(it, m["text"]) or "").strip() if pick(it, m["text"]) else None,
            "url": pick(it, m["url"]),
            "author": pick(it, m["author"]),
            "followers": as_int(pick(it, m["followers"])),
            "reach": as_int(pick(it, m["reach"])),
            "likes": as_int(pick(it, m["likes"])),
            "comments": as_int(pick(it, m["comments"])),
            "shares": as_int(pick(it, m["shares"])),
            "date": pick(it, m["date"]),
            "duration_s": dur_seconds(pick(it, m["duration"])),
            "kind": pick(it, m["kind"]),
        }
        if not rec["url"] and not rec["text"]:
            continue
        parts = [rec[k] for k in ("likes", "comments", "shares") if rec[k] is not None]
        rec["engagement"] = sum(parts) if parts else None
        rec["eng_rate"] = (round(rec["engagement"] / rec["reach"], 4)
                           if rec["engagement"] is not None and rec["reach"] else None)
        rec["reach_per_follower"] = (round(rec["reach"] / rec["followers"], 2)
                                     if rec["reach"] and rec["followers"] else None)
        d = parse_date(rec["date"])
        rec["age_days"] = (datetime.now(timezone.utc) - d).days if d else None
        rec["iso_date"] = d.date().isoformat() if d else None
        out.append(rec)

    if profiles:
        for r in out:
            if r["followers"] is None and r["author"]:
                r["followers"] = profiles.get(r["author"].lower())
                if r["followers"] and r["reach"]:
                    r["reach_per_follower"] = round(r["reach"] / r["followers"], 2)

    for r in out:
        r["eng_per_follower"] = (round(r["engagement"] / r["followers"], 5)
                                 if r["engagement"] is not None and r["followers"] else None)

    # outlier vs the same account's own median inside this pull (needs 3+ items to mean anything)
    by_author = {}
    for r in out:
        if r["author"] and r["reach"]:
            by_author.setdefault(r["author"], []).append(r["reach"])
    for r in out:
        med = by_author.get(r["author"] or "")
        r["vs_own_median"] = (round(r["reach"] / statistics.median(med), 2)
                              if med and len(med) >= 3 and r["reach"] else None)
    return out


def fmt(n):
    if n is None:
        return "n/a"
    if isinstance(n, float):
        return f"{n:g}"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def clip(s, n=68):
    if not s:
        return "n/a"
    s = " ".join(str(s).split())
    s = s.replace("|", "/")
    return s if len(s) <= n else s[: n - 1] + "…"


def report(recs, platform, top):
    label = REACH_LABEL[platform]
    have = [r for r in recs if r["reach"] is not None]
    ranked = sorted(have, key=lambda r: r["reach"], reverse=True)[:top]
    print(f"\n## {platform} - top {len(ranked)} by {label} ({len(recs)} items scanned, "
          f"{len(recs) - len(have)} with no {label} reported)\n")
    print(f"| # | Title/Caption | Author | {label.capitalize()} | Eng. rate | {label.capitalize()}/follower | Date |")
    print("|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked, 1):
        er = f"{r['eng_rate']*100:.1f}%" if r["eng_rate"] is not None else "n/a"
        print(f"| {i} | {clip(r['text'])} | {r['author'] or 'n/a'} | {fmt(r['reach'])} | "
              f"{er} | {fmt(r['reach_per_follower'])} | {r['iso_date'] or 'n/a'} |")

    # Carousels and image posts often report no play count at all. Rank those by raw
    # engagement instead of dropping them - on Instagram they are half the field.
    noreach = [r for r in recs if r["reach"] is None and r["engagement"]]
    if noreach:
        withf = [r for r in noreach if r["eng_per_follower"] is not None]
        if withf:
            # Engagement per follower, NOT reach. Instagram does not report plays here, so this
            # is the only cross-account comparison available - label it as such, always.
            withf.sort(key=lambda r: r["eng_per_follower"], reverse=True)
            print(f"\n### No {label} reported - top {min(top, len(withf))} by ENGAGEMENT per "
                  f"follower (engagement, not reach)\n")
            print("| # | Title/Caption | Author | Followers | Engagement | Eng/follower | Format | Date |")
            print("|---|---|---|---|---|---|---|---|")
            for i, r in enumerate(withf[:top], 1):
                print(f"| {i} | {clip(r['text'], 52)} | {r['author'] or 'n/a'} | {fmt(r['followers'])} | "
                      f"{fmt(r['engagement'])} | {r['eng_per_follower']*100:.2f}% | "
                      f"{r['kind'] or 'n/a'} | {r['iso_date'] or 'n/a'} |")
            med_epf = statistics.median([r["eng_per_follower"] for r in withf])
            print(f"\n**Median engagement per follower:** {med_epf*100:.2f}% "
                  f"({len(withf)} of {len(noreach)} items have a follower count)")
            punch = [r for r in withf if r["eng_per_follower"] >= 3 * med_epf]
            if punch:
                print(f"\n**Punching above their size (>=3x the median rate):**")
                for r in punch[:top]:
                    print(f"- **{clip(r['text'], 70)}** - {r['author']}, {fmt(r['followers'])} followers, "
                          f"{fmt(r['engagement'])} engagements = {r['eng_per_follower']*100:.2f}% - {r['url']}")
        rest = [r for r in noreach if r["eng_per_follower"] is None]
        if rest:
            rest.sort(key=lambda r: r["engagement"], reverse=True)
            print(f"\n### No {label} and no follower count - top {min(top, len(rest))} by raw engagement\n")
            print("| # | Title/Caption | Author | Engagement | Format | Date |")
            print("|---|---|---|---|---|---|")
            for i, r in enumerate(rest[:top], 1):
                print(f"| {i} | {clip(r['text'])} | {r['author'] or 'n/a'} | {fmt(r['engagement'])} | "
                      f"{r['kind'] or 'n/a'} | {r['iso_date'] or 'n/a'} |")

    med = statistics.median([r["reach"] for r in have]) if have else None
    print(f"\n**Median {label} in this pull:** {fmt(int(med)) if med else 'n/a'}"
          f"  |  **items:** {len(recs)}")

    # outliers: punched above the account's own size or its own median
    outs = [r for r in have if (r["reach_per_follower"] or 0) >= 2 or (r["vs_own_median"] or 0) >= 3]
    outs.sort(key=lambda r: (r["reach_per_follower"] or 0, r["vs_own_median"] or 0), reverse=True)
    print(f"\n### Outliers (>=2x their follower count, or >=3x that account's own median here)\n")
    if not outs:
        print("None in this pull.\n")
    else:
        for r in outs[:top]:
            bits = []
            if r["reach_per_follower"]:
                bits.append(f"{r['reach_per_follower']}x followers ({fmt(r['followers'])})")
            if r["vs_own_median"]:
                bits.append(f"{r['vs_own_median']}x own median")
            print(f"- **{clip(r['text'], 80)}** - {r['author'] or 'n/a'}, {fmt(r['reach'])} {label}, "
                  f"{', '.join(bits) or 'n/a'} - {r['url'] or 'n/a'}")

    durs = [r["duration_s"] for r in ranked if r["duration_s"]]
    if durs:
        print(f"\n**Median duration of the top {len(ranked)}:** {int(statistics.median(durs))}s "
              f"(range {min(durs)}-{max(durs)}s)")
    ages = [r["age_days"] for r in ranked if r["age_days"] is not None]
    if ages:
        print(f"**Age of the top {len(ranked)}:** median {int(statistics.median(ages))} days "
              f"(range {min(ages)}-{max(ages)})")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True, choices=sorted(MAPS))
    ap.add_argument("--in", dest="inp", required=True, help="raw Apify dataset items (JSON)")
    ap.add_argument("--out", help="write the normalized records here")
    ap.add_argument("--profiles", help="Instagram `details` dataset, to attach follower counts")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()

    profiles = load_profiles(a.profiles) if a.profiles else None
    recs = normalize(load(a.inp), a.platform, profiles)
    if not recs:
        print(f"\n## {a.platform}\n\nNo usable items in {a.inp}. Say so in the brief; do not guess.\n")
        return
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(recs, f, indent=2, ensure_ascii=False)
    report(recs, a.platform, a.top)


if __name__ == "__main__":
    main()
