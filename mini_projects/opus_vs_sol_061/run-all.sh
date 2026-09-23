#!/bin/bash
# Pre-run every remaining 061 use case on both profiles. One folder per model per case.
# Runs cases sequentially per model, both models in parallel. Logs to runs/<model>/<case>/out.txt.
set -u
R="$(cd "$(dirname "$0")" && pwd)"
cd "$R/inputs"
run_model() {
  m=$1
  for c in ${CASES:-1-website 2-review 3-ad 4-game 5-videos 7-brief}; do
    d="$R/runs/$m/$c"; mkdir -p "$d"
    [ "$c" = "3-ad" ] && cp "$R/inputs/attend-ad-swipe.md" "$d/"
    ( cd "$d" && /usr/bin/time -p hermes -p "$m" chat -q "$(cat "$R/prompts/$c.md")" > out.txt 2>&1 ) 2> "$d/time.txt"
    echo "$m $c done $(grep real "$d/time.txt")"
  done
}
run_model opus &
run_model sol &
wait
echo ALL DONE
