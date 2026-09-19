#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from lead_crew.crew import LeadCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

SAMPLE_TRANSCRIPT = """
[00:00] AE (Tyler): Hey Jamie, thanks for making the time. Before we dive in—okay to record so I can share notes with our SE?
[00:04] Prospect (Jamie, Director of Operations): Yep, recording's fine.
[00:06] AE: Perfect. Quick agenda: your workflow today, where returns and forecasting hurt, who needs to be involved, timing/budget, and then I’ll show how customers use our platform. Sound good?
[00:15] Jamie: Works for me.

[00:18] AE: Cool. Give me the 60-second on the business.
[00:21] Jamie: We’re Northbeam Outfitters—DTC apparel, mostly outerwear and accessories. 120 employees, about mid-eight figures in revenue. Shopify Plus for ecommerce, Klaviyo for email/SMS, NetSuite for ERP, 3PL is Redline Logistics. We do 35–40k orders/month in Q4, closer to 18–22k off-season.

[00:38] AE: Got it. What brought you to us?
[00:40] Jamie: Returns. They’re killing margin and creating chaos for ops. Our return rate averages 18.7%—peaks at 24% Jan–Feb after holiday gifting. We’re doing too much in spreadsheets. We also need better demand forecasting for replenishment—SKU-level signals are noisy.

[00:56] AE: What does the returns workflow look like today?
[00:58] Jamie: We use Loop Returns for the portal, but the decisioning is basic. If it’s within 30 days and unused, it usually goes through. We don’t triage properly—like first-time vs repeat offender, return reason weighting, or predicted resellability. Warehouse receives, inspects, and updates NetSuite. We reconcile in weekly CSVs—manual VLOOKUPs.

[01:19] AE: How long from return initiation to refund?
[01:21] Jamie: About 9.5 days median. We want <5 days. Slow cycle time triggers WISMO tickets. CS team hates that.

[01:28] AE: Top return reasons?
[01:29] Jamie: Sizing variance is #1. Color mismatch in UGC vs PDP is #2. Damaged packaging is #3—mostly carrier and some 3PL mishandling. About 27% of returned units are resellable with no touch-ups, another ~40% need steaming/retagging, and the rest go to liquidation.

[01:46] AE: What would success look like for you this quarter?
[01:48] Jamie: Reduce return rate by 2–3 points, cut time-to-refund to 5 days, and improve resell rate by 10 points. If we can show a believable path to 6-month ROI, budget is there.

[01:58] AE: Who else besides you needs to sign off?
[02:00] Jamie: I influence. Final sign-off is our COO (Nora) and CFO (Marta). Sometimes there’s a small committee if there’s security or integration risk.

[02:09] AE: On that—any red flags you’re already anticipating?
[02:12] Jamie: Integration with Redline’s WMS. Their API rate-limits and documentation is… not great. Also, security review for PII handling. We’ve got SOC 2 Type II, DPA requirements, the usual.

[02:23] AE: Makes sense. Budget ballpark?
[02:25] Jamie: For SaaS, we can do low-to-mid five figures annually, with flexibility if the ROI case is strong. We also have some services budget for a pilot—up to about $40k this quarter across initiatives, not just this.

[02:36] AE: Timeline?
[02:37] Jamie: If we like the fit, pilot in 45–60 days. We’d need a short security review, legal’s DPA, and procurement. Implementation can run in parallel if we keep scope tight.

[02:47] AE: Great. I’m going to pull in Alex, our Solutions Engineer, just to sanity-check the Redline piece. One sec…

[03:00] SE (Alex): Hey all. I reviewed Redline’s API briefly—auth is token-based, 300 requests/minute. For our ingestion, we’d batch status updates and use webhooks where possible. Worst case we mirror their events via an S3 dump if rate limits bite. We’ve integrated with ShipHero and 3PL Central—patterns are similar.

[03:18] Jamie: We can do S3 exports. We already drop a weekly returns file for finance.

[03:21] SE: Perfect. For near-real-time, we’ll subscribe to return-created/received events. We enrich with PDP metadata and customer history to score resellability and likelihood-to-churn if refund delayed.

[03:31] AE: Speaking of scoring: we use a combination of policy rules you control and ML signals. Example: first return vs third return within 90 days, reason code weight, size adjacency, item markdown risk, and historical QC outcomes. The system decides: auto-approve, exchange suggestion, store credit push, or route to manual review.

[03:48] Jamie: That’s what we’re missing—right now it’s blunt logic.

[03:51] AE: On forecasting: we blend order velocity, return cohorts, PDP traffic, Klaviyo campaign calendar, and seasonal curves. Helps purchasing avoid over/under-buys—especially on sizes.

[04:00] Jamie: Yeah, we stock out on S and M in parkas and are stuck with XXL. Classic problem.

[04:05] AE: If we hit your goals—2–3 point return-rate reduction, refund cycle down to 5 days, +10 points resellability—you’re good to greenlight?
[04:12] Jamie: With a CFO that likes numbers—yes. Show the math.

[04:15] AE: Quick pricing preview so we don’t waste anyone’s time: most brands your size land on our Growth plan at ~$3.5k/month; Pro is ~$5k/month with advanced forecasting and warehouse triage; volume-based overages after 50k returns/year. Implementation ranges $10–25k depending on WMS complexity. Does that scare anyone?

[04:34] Jamie: Not if ROI is clear. Marta will ask about payback and whether we can treat part of this as COGS.

[04:39] AE: Understood. We’ll build a 6‑month ROI model with your real data. Speaking of, can we talk metrics to plug in?

[04:46] Jamie: Sure. AOV is $98. Contribution margin after shipping and pick/pack is ~52% but drops to ~35% on returns due to handling. Return processing costs us ~$6.40/unit in labor and materials. Liquidation recovers ~18% of retail on average.

[05:02] SE: What about exchange rate vs refund?
[05:04] Jamie: Exchanges are only 22% of returns—too low. We want >35%.

[05:08] AE: We can nudge exchanges by showing in-stock alternates and size guidance at the decision point and by offering instant credit. Our customers typically see a 6–12 point lift in exchanges.

[05:18] Jamie: If we get 10 points, Marta will smile.

[05:21] AE: Any objections we haven’t addressed?
[05:23] Jamie: Data privacy. And we can’t disrupt warehouse flow Q4 peak.

[05:28] SE: We deploy read-only listeners first and mirror your current process. The triage UI sits on top of Loop; approvals still sync back. We can feature-flag rules and ramp in waves by SKU category.

[05:40] AE: Mind if Marta joins for 10 minutes? I see her on the invite.
[05:43] Jamie: Yeah, let me ping her.

[05:52] CFO (Marta): Hey team, just joined. I heard my name and ROI in the same sentence.

[05:56] AE: Hi Marta! Super quick: Jamie’s goals are -2–3 pts return rate, refund cycle down to 5 days, +10 pts resell. We think pilot in 45–60 days. Pricing likely $3.5–5k/month plus one-time implementation depending on 3PL complexity. We’ll build a 6‑month ROI model.

[06:13] Marta: What inputs do you need for the model?
[06:15] AE: Historical return rate by category, AOV, contribution margin, resell vs liquidation mix, processing cost/unit, WISMO ticket volume, and any retention impact from faster refunds.

[06:26] Marta: If we reduce refunds by 2 points and lift exchanges by 10 points, what’s your back-of-napkin payback?

[06:32] AE: Rough math: At 30k orders/month and 18.7% returns, that’s ~5,610 returns. 2 points down saves ~600 returns a month. At $98 AOV and 35% contribution on returns avoided, call it ~$20–21k value/month. Exchanges lift of 10 points on those ~5,610 returns shifts ~561 refunds to exchanges; if half of those keep the same AOV/contribution, that’s another ~9–10k in retained margin. Net of $3.5–5k SaaS and say $15k implementation amortized over 12 months, payback looks under 3 months. We’ll refine with real data.

[07:10] Marta: Okay, not committing, but that’s directionally interesting. Two conditions: (1) security review including SOC 2 report and DPA, (2) pilot milestone with claw-back or discount if outcomes miss by a wide margin.

[07:23] AE: Reasonable. We can frame a success plan with specific KPIs and a mid‑pilot checkpoint.

[07:28] Jamie: Also need to confirm Redline can support the webhook volume.

[07:31] SE: If they can’t, we’ll do S3 drops every 15 minutes and a change-data-capture diff. We’ve done that elsewhere.

[07:38] Marta: Procurement timeline?
[07:40] Jamie: Security review 1 week if your docs are ready. Legal 1–2 weeks depending on redlines. We can start data exports right away.

[07:48] AE: Great. Next steps I’m hearing:
  1) We send NDA + security pack (SOC 2, penetration summary, data flow diagram) today.
  2) You drop a 6‑month sample of returns/order data via S3 so we build the ROI model and a sandbox.
  3) Technical working session to map events (Loop, Shopify, Redline, NetSuite).
  4) Success plan draft with KPIs: return rate -2 pts, TTR 5 days, exchanges +10 pts, resellability +10 pts.
  5) Pencil a pilot start in 45–60 days subject to review.

[08:15] Jamie: Add (6) integration test in staging with three SKUs across two warehouses.

[08:19] SE: Done. We’ll also run a dark launch for a week—system scores, but humans still decide—so you can compare outcomes safely.

[08:27] Marta: Pricing—send tiers with a pilot-friendly ramp and an annual option. We prefer annual if the pilot works.

[08:33] AE: Will do. Anything else blocking a yes?

[08:36] Jamie: Just want to see real results with our data and have the warehouse sign off on the triage screen. They hate extra clicks.

[08:42] SE: We can embed approve/deny/exchange directly in the Loop screen and auto-fill notes from the score rationale.

[08:48] AE: Okay—action items on our side: send NDA + security pack today, ROI inputs checklist, proposed architecture, and sample success plan. On your side: S3 access + sample data, intro to Redline contact, and warehouse lead (Luis) for a 30‑min usability review.

[09:05] Jamie: I’ll connect you with Luis and our Redline rep after this call.

[09:08] Marta: Loop me on the ROI model. If numbers hold, we can move fast.

[09:12] AE: Perfect. How does next Wednesday 2:00–2:45pm ET look for the tech working session?

[09:16] Jamie: Works.
[09:17] Marta: I can do 2:15–2:45—join for the last 30.

[09:20] AE: Calendar coming. Anything else you wish I’d asked?

[09:23] Jamie: Maybe just—do you handle fraud on returns?

[09:26] AE: We flag anomalies: address reuse, serial returners, mismatched IMEI for electronics (not your case), and item‑photo similarity for damage claims. We don’t run payments fraud, but we integrate with your risk vendor.

[09:37] Jamie: Good to know.

[09:39] AE: Awesome. Thanks both. We’ll get those docs out within the hour and hold time for next Wednesday.

[09:45] Marta: Thanks.
[09:46] Jamie: Thanks. Talk soon.
"""

def run():
    """
    Run the crew.
    """
    inputs = {
        "transcript": SAMPLE_TRANSCRIPT,
        "company": os.getenv("DEMO_COMPANY", "Acme Brands"),
        "contact_name": os.getenv("DEMO_CONTACT", "Jamie"),
        "product": os.getenv("PRODUCT_BRIEF", "AI-driven returns prediction & analytics platform"),
        "icp_criteria": os.getenv("ICP_CRITERIA", "Mid-market to enterprise ecommerce brands (50-1000 employees) using Shopify/Klaviyo; ops pain around forecasting/returns; data-savvy ops team."),
        "current_year": 2025,
        "scoring_rubric": os.getenv("SCORING_RUBRIC", "Favor strong NEED and ICP fit; penalize high integration risk."),
    }
    
    try:
        response = LeadCrew().crew().kickoff(inputs=inputs)
        print(response.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
if __name__ == "__main__":
    run()