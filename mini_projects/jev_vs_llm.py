#!/usr/bin/env python3
"""Same email, same three questions, two models. Prints both answers, both latencies, both bills.

  python3 jev_vs_llm.py                 # built-in sample email
  python3 jev_vs_llm.py email.txt       # any text file
  python3 jev_vs_llm.py email.txt --llm-only   # skip Jev (saves quota while iterating)

Requires: pip install "openai>=3.35,<4"   (the Jev side is standard library only)
Keys: OPENAI_API_KEY and TYPESAFE_API_KEY, from the environment, else ~/.hermes/.env then ~/.claude/.env.
Jev side goes through the jev-agent.com gateway (field-for-field the TypeSafe API; swap host
and key when a TypeSafe key arrives). LLM side uses OpenAI structured outputs so the answer
shape matches Jev's and the comparison is fair: one call, JSON out, no retries.
"""
import json, os, sys, time, urllib.request, urllib.error

# ---- keys -------------------------------------------------------------------
def load_env():
    for p in ("~/.hermes/.env", "~/.claude/.env"):
        p = os.path.expanduser(p)
        if os.path.exists(p):
            for l in open(p):
                if "=" in l and not l.startswith("#"):
                    k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
load_env()

# ---- the decision, defined once ---------------------------------------------
DEPARTMENTS = {"billing": "Payments, invoicing, refunds, double charges",
               "technical": "Bugs, outages, integrations",
               "sales": "Pricing, upgrades, new accounts",
               "spam": "Unsolicited marketing or nonsense"}
FRUSTRATION = ["Calm", "Annoyed", "Angry"]
URGENT = {"true": "Explicitly time-sensitive or threatens to leave", "false": "No urgency expressed"}

SAMPLE = """From: dana@northwindcoffee.com
Subject: charged twice this month??

Hi, I just looked at my statement and Attend charged me on the 3rd AND the 5th. This is the second
time this has happened. I need this fixed today or I'm cancelling. Order ids 8812 and 8819.
Dana"""

# ---- Jev --------------------------------------------------------------------
JEV_URL = "https://jev-agent.com/api/v1/systemone"
JEV_PRICE_PER_MTOK_IN = 0.042  # TypeSafe list price; output free

def ask_jev(state):
    body = {"model": "jev-latest", "state": state, "questions": {
        "department": {"type": "choice", "instructions": "Which team should handle this email?", "criteria": DEPARTMENTS},
        "frustration": {"type": "score", "instructions": "How frustrated is the sender?", "criteria": FRUSTRATION},
        "is_urgent": {"type": "noul", "instructions": "Does the sender need a reply today?", "criteria": URGENT},
    }}
    req = urllib.request.Request(JEV_URL, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}", "Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as r: raw = json.load(r)
    ms = (time.perf_counter() - t0) * 1000
    a = raw["answers"]; u = raw["usage"]
    fr = a["frustration"]
    return {
        "department": a["department"]["choice"],
        "frustration": fr["legend"][str(round(fr["score"]))],
        "is_urgent": a["is_urgent"]["noul"] >= 0.5,
        "detail": {"department_p": a["department"]["probabilities"], "frustration_score": fr["score"], "urgent_p": a["is_urgent"]["noul"]},
        "ms": ms, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"],
        "usd": u["input_tokens"] / 1e6 * JEV_PRICE_PER_MTOK_IN,
        "model": raw["model"], "quota": raw.get("quota"),
    }

# ---- LLM --------------------------------------------------------------------
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-6-astra")
LLM_PRICE = {"gpt-6-astra": (10.00, 50.00), "gpt-5.4-mini": (0.20, 1.60)}  # per Mtok (in, out); update from the pricing page

def ask_llm(state):
    from openai import OpenAI
    client = OpenAI()
    schema = {"type": "object", "additionalProperties": False, "required": ["department", "frustration", "is_urgent"],
              "properties": {"department": {"type": "string", "enum": list(DEPARTMENTS)},
                             "frustration": {"type": "string", "enum": FRUSTRATION},
                             "is_urgent": {"type": "boolean"}}}
    prompt = ("Classify this email. department: " + "; ".join(f"{k} = {v}" for k, v in DEPARTMENTS.items()) +
              ". frustration: one of " + ", ".join(FRUSTRATION) +
              ". is_urgent: true if " + URGENT["true"] + ", false if " + URGENT["false"] + ".\n\nEmail:\n" + state)
    t0 = time.perf_counter()
    r = client.responses.create(model=LLM_MODEL, input=prompt,
                                text={"format": {"type": "json_schema", "name": "triage", "schema": schema, "strict": True}})
    ms = (time.perf_counter() - t0) * 1000
    out = json.loads(r.output_text); u = r.usage
    pin, pout = LLM_PRICE.get(LLM_MODEL, (0, 0))
    return {**out, "ms": ms, "tokens_in": u.input_tokens, "tokens_out": u.output_tokens,
            "usd": u.input_tokens / 1e6 * pin + u.output_tokens / 1e6 * pout, "model": LLM_MODEL}

# ---- run --------------------------------------------------------------------
def show(name, r):
    print(f"\n{name}  ({r['model']})")
    print(f"  department  {r['department']}")
    print(f"  frustration {r['frustration']}")
    print(f"  urgent      {r['is_urgent']}")
    print(f"  {r['ms']:.0f} ms   {r['tokens_in']} in / {r['tokens_out']} out   ${r['usd']:.6f}")
    if r.get("quota"): print(f"  quota: {r['quota'].get('remaining')} left this month")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    state = open(args[0]).read() if args else SAMPLE
    llm = ask_llm(state); show("LLM", llm)
    if "--llm-only" not in sys.argv:
        jev = ask_jev(state); show("Jev", jev)
        print(f"\nJev vs LLM: {llm['ms']/jev['ms']:.1f}x faster, {llm['usd']/jev['usd']:.0f}x cheaper, "
              f"same answer: {all(llm[k]==jev[k] for k in ('department','frustration','is_urgent'))}")
