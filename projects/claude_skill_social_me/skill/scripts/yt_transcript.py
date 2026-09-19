#!/usr/bin/env python3
"""Pull a YouTube transcript with yt-dlp (auto-subs).

Prints the plaintext transcript on success. Prints `YTDLP_FAILED` (and nothing else on stdout)
if yt-dlp can't get subtitles - the yt-research skill treats that as the signal to fall back to
Apify subtitles, which is the reliable path when YouTube 403s / withholds a PO token.

Usage: python3 yt_transcript.py "<youtube_url_or_id>"
"""
import sys
import os
import re
import glob
import tempfile
import subprocess


def strip_vtt(path):
    out = []
    for raw in open(path, encoding="utf-8", errors="ignore"):
        line = raw.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line or line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line)          # inline timing tags
        line = re.sub(r"\s+", " ", line).strip()
        if line and (not out or out[-1] != line):     # drop the doubled-caption lines
            out.append(line)
    return " ".join(out)


def main():
    if len(sys.argv) < 2:
        print("usage: yt_transcript.py <url>", file=sys.stderr)
        sys.exit(2)
    url = sys.argv[1]
    py = "/usr/bin/python3"  # the interpreter that has yt_dlp installed on this machine
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "sub")
        try:
            subprocess.run(
                [py, "-m", "yt_dlp", "--write-auto-subs", "--sub-lang", "en",
                 "--skip-download", "--sub-format", "vtt", "-o", out + ".%(ext)s", url],
                capture_output=True, text=True, timeout=180,
            )
        except Exception:
            print("YTDLP_FAILED")
            return
        vtts = glob.glob(out + "*.vtt")
        if not vtts:
            print("YTDLP_FAILED")
            return
        text = strip_vtt(vtts[0])
        if len(text) < 80:
            print("YTDLP_FAILED")
            return
        print(text)


if __name__ == "__main__":
    main()
