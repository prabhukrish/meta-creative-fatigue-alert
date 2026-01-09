📊 Automated Meta Ads Audit & Creative Fatigue Detection (Side Project)
Overview

This project is an automated Meta Ads monitoring system that delivers a daily, decision-ready campaign audit via email.

It combines yesterday’s business performance with trend-based health diagnostics to help performance marketers act early—before creative fatigue or inefficiencies impact spend.

The system runs fully automatically using the Meta Marketing API and GitHub Actions.

What Problem This Solves

Manually checking Meta Ads performance is:

Reactive

Time-consuming

Easy to misread without context (budget, trends, fatigue)

This system answers two critical daily questions in one email:

What did each campaign deliver yesterday?

Is the campaign healthy or drifting toward fatigue?

Key Features
📧 Daily Campaign Audit Email

Delivered automatically every day with two clear sections:

1️⃣ Yesterday Performance (Business View)

One table showing, per campaign:

Daily Budget

Spend (Yesterday)

Impressions

Results (dynamic label: Leads / Purchases / etc.)

Cost per Result

CTR

CPM

2️⃣ Campaign Health & Fatigue (Diagnostic View)

One table showing, per campaign:

CTR % change (last 7 days vs previous 7 days)

CPM % change (last 7 days vs previous 7 days)

Frequency

Status: HEALTHY / WARNING / CRITICAL

🚨 Creative Fatigue Alerts

Separate critical alert emails for CRITICAL campaigns

Triggered only when multiple degradation signals align

Cooldown logic prevents alert spam

🤖 Full Automation

Scheduled via GitHub Actions

Secure credentials using repository secrets

No manual intervention required

Tech Stack

Python

Meta Marketing API

GitHub Actions (cron automation)

Brevo (email delivery)

Streamlit (optional dashboard for visibility)

Design Philosophy

Trend-based analysis over single-day noise

Business metrics first, diagnostics second

High-signal, low-noise alerts

Built for how marketers actually make decisions

Why This Project Matters

This is not a reporting script or dashboard clone.

It’s a monitoring system that:

Reduces manual checks

Surfaces risk early

Improves decision speed

Bridges performance data and action

Status

✅ Production-ready
✅ Running daily
✅ Actively used for monitoring Meta Ads performance

### Future Enhancements
- Budget utilisation alerts
- Creative-level drilldowns
- Slack / WhatsApp alerts
- Historical trend dashboards
