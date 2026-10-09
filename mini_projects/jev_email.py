#!/usr/bin/env python3
"""Jev smoke test: the docs quickstart shape (one support email, three typed questions).
Reads TYPESAFE_API_KEY from ~/.hermes/.env (currently a jev-agent.com gateway key, 5 free decisions/month). Prints the raw response, then the read.
Usage: python3 jev_email.py [path-to-email.txt]   (no arg = the built-in sample)"""
import json, os, sys, time, urllib.request, urllib.error

def key():
    for l in open(os.path.expanduser("~/.hermes/.env")):
        if l.startswith("TYPESAFE_API_KEY="):
            return l.split("=", 1)[1].strip()
    sys.exit("TYPESAFE_API_KEY missing in ~/.hermes/.env")

SAMPLE = """From: dana@northwindcoffee.com
Subject: charged twice this month??

Hi, I just looked at my statement and Attend charged me on the 3rd AND the 5th. This is the second
time this has happened. I need this fixed today or I'm cancelling. Order ids 8812 and 8819.
Dana"""

state = open(sys.argv[1]).read() if len(sys.argv) > 1 else SAMPLE

body = {
    "model": "jev-latest",
    "state": state,
    "questions": {
        "department": {
            "type": "choice",
            "instructions": "Which team should handle this email?",
            "criteria": {"billing": "Payments, invoicing, refunds, double charges",
                         "technical": "Bugs, outages, integrations",
                         "sales": "Pricing, upgrades, new accounts",
                         "spam": "Unsolicited marketing or nonsense"},
        },
        "frustration": {
            "type": "score",
            "instructions": "How frustrated is the sender?",
            "criteria": ["Calm", "Annoyed", "Angry"],
        },
        "is_urgent": {
            "type": "noul",
            "instructions": "Does the sender need a reply today?",
            "criteria": {"true": "Explicitly time-sensitive or threatens to leave",
                         "false": "No urgency expressed"},
        },
    },
}

req = urllib.request.Request(
    "https://jev-agent.com/api/v1/systemone",  # jev-agent.com gateway; swap host + key for api.typesafe.ai when a TypeSafe key arrives
    data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"},
)
t0 = time.perf_counter()
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = json.load(r)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:600]); sys.exit(1)
ms = (time.perf_counter() - t0) * 1000

print("--- raw ---")
print(json.dumps(raw, indent=1)[:1500])
print(f"\n--- read ---  {ms:.0f} ms round trip")
ans = raw.get("answers") or raw.get("results") or raw
for q, a in (ans.items() if isinstance(ans, dict) else []):
    print(f"{q:12s} {json.dumps(a)[:160]}")
u = raw.get("usage")
if u: print("usage:", u)
q = raw.get("quota")
if q: print("quota:", q)
