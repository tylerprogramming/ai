import json
import os
from typing import Dict, Any
from crewai.tools import tool

DEFAULT_WEIGHTS = {
    "budget": 0.15,
    "authority": 0.15,
    "need": 0.25,
    "timing": 0.15,
    "icp_fit": 0.20,
    "engagement": 0.10,
    "risk": -0.10,  # risk subtracts
}

LEVELS = {
    "budget": {
        "none": 0,
        "unknown": 0.25,
        "low": 0.5,
        "adequate": 0.8,
        "committed": 1.0,
    },
    "authority": {
        "user": 0.25,
        "influencer": 0.6,
        "committee": 0.8,
        "decision_maker": 1.0,
    },
    "need": {
        "weak": 0.25,
        "moderate": 0.6,
        "strong": 0.85,
        "urgent": 1.0,
    },
    "timing": {
        "no_timeline": 0.2,
        ">6mo": 0.4,
        "3-6mo": 0.7,
        "<3mo": 0.9,
        "immediate": 1.0,
    },
    "icp_fit": {
        "poor": 0.2,
        "fair": 0.5,
        "good": 0.8,
        "excellent": 1.0,
    },
    "engagement": {
        "low": 0.3,
        "medium": 0.6,
        "high": 1.0,
    },
    "risk": {
        "low": 0.0,      # subtract 0
        "medium": 0.5,   # subtract some
        "high": 1.0,     # subtract most
    },
}


def _load_weights() -> Dict[str, float]:
    raw = os.getenv("SCORING_WEIGHTS")
    if not raw:
        return DEFAULT_WEIGHTS
    try:
        custom = json.loads(raw)
        merged = DEFAULT_WEIGHTS.copy()
        merged.update({k: float(v) for k, v in custom.items() if k in DEFAULT_WEIGHTS})
        return merged
    except Exception:
        return DEFAULT_WEIGHTS


def _to_unit(feature: str, value: str) -> float:
    if value is None:
        return 0.0
    v = str(value).strip().lower()
    mapping = LEVELS.get(feature, {})
    return float(mapping.get(v, 0.0))


@tool("calculate_lead_score")
def calculate_lead_score(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic lead scoring.

    Expected inputs (categorical strings):
      - budget:        none|unknown|low|adequate|committed
      - authority:     user|influencer|committee|decision_maker
      - need:          weak|moderate|strong|urgent
      - timing:        no_timeline|>6mo|3-6mo|<3mo|immediate
      - icp_fit:       poor|fair|good|excellent
      - engagement:    low|medium|high
      - risk:          low|medium|high  (subtracts per weights)

    Optional:
      - weights: { str: float }  # overrides defaults for this call only

    Returns: {
      "subscores": {<feature>: {"unit": 0..1, "weighted": -/+..}},
      "total": 0..100,
      "tier": "Hot"|"Warm"|"Cold"
    }
    """
    weights = _load_weights()
    if isinstance(inputs, dict) and isinstance(inputs.get("weights"), dict):
        # one-off overrides
        for k, v in inputs["weights"].items():
            if k in weights:
                try:
                    weights[k] = float(v)
                except Exception:
                    pass

    # normalize to 0..1
    unit = {
        k: _to_unit(k, inputs.get(k))
        for k in ["budget", "authority", "need", "timing", "icp_fit", "engagement", "risk"]
    }

    # weighted sum (risk subtracts)
    weighted = {
        "budget": unit["budget"] * weights["budget"],
        "authority": unit["authority"] * weights["authority"],
        "need": unit["need"] * weights["need"],
        "timing": unit["timing"] * weights["timing"],
        "icp_fit": unit["icp_fit"] * weights["icp_fit"],
        "engagement": unit["engagement"] * weights["engagement"],
        "risk": - unit["risk"] * abs(weights["risk"])  # subtract
    }

    # Convert to 0..100 by treating positive-weight sum as baseline
    raw = sum(weighted.values())
    max_pos = sum([weights["budget"], weights["authority"], weights["need"], weights["timing"], weights["icp_fit"], weights["engagement"]])
    min_total = -abs(weights["risk"])  # worst-case high risk
    max_total = max_pos  # best case, zero risk

    # map raw from [min_total, max_total] -> [0, 100]
    if max_total == min_total:
        pct = 0.0
    else:
        pct = (raw - min_total) / (max_total - min_total)
    score = max(0.0, min(100.0, pct * 100.0))

    if score >= 70:
        tier = "Hot"
    elif score >= 40:
        tier = "Warm"
    else:
        tier = "Cold"

    return {
        "subscores": {
            k: {"unit": round(unit[k], 3), "weighted": round(v, 3)} for k, v in weighted.items()
        },
        "total": round(score, 1),
        "tier": tier,
    }