#!/bin/bash
# Two Hermes profiles, same SOUL and skills, different model. Edit the model ids to test any pair.
set -e
A_NAME=${A_NAME:-opus}; A_MODEL=${A_MODEL:-claude-opus-5-5}; A_PROVIDER=${A_PROVIDER:-anthropic}
B_NAME=${B_NAME:-sol};  B_MODEL=${B_MODEL:-gpt-6-sol};       B_PROVIDER=${B_PROVIDER:-openai-codex}
BASE=${BASE:-coder}   # an existing profile to clone SOUL + skills + memories from

for p in "$A_NAME:$A_MODEL:$A_PROVIDER" "$B_NAME:$B_MODEL:$B_PROVIDER"; do
  IFS=: read -r name model provider <<< "$p"
  hermes profile create "$name" 2>/dev/null || true
  cp ~/.hermes/profiles/$BASE/SOUL.md ~/.hermes/profiles/$name/SOUL.md
  mkdir -p ~/.hermes/profiles/$name/skills ~/.hermes/profiles/$name/memories
  cp -R ~/.hermes/profiles/$BASE/skills/. ~/.hermes/profiles/$name/skills/
  cp ~/.hermes/profiles/$BASE/memories/*.md ~/.hermes/profiles/$name/memories/ 2>/dev/null || true
  hermes -p "$name" config set model.default "$model"
  hermes -p "$name" config set model.provider "$provider"
  echo "$name -> $model ($provider)"
done
# Note: Hermes has no bare 'openai' provider id. Subscription = openai-codex. API key = provider custom + model.base_url https://api.openai.com/v1 + model.api_key.

# Optional: put both on the same daily cron so the delivery thread becomes the cold open.
# P='You are Coder. Check <your repos>: commits in the last 24h, failed CI, open PRs. Start your message with your model id in brackets. If everything is green say exactly: All green. Nothing needs you.'
# hermes -p $A_NAME cron create "0 8 * * *" "$P" --name "$A_NAME: morning repo check" --deliver slack
# hermes -p $B_NAME cron create "0 8 * * *" "$P" --name "$B_NAME: morning repo check" --deliver slack
