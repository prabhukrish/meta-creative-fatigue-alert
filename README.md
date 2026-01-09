# Meta Ads Daily Audit & Creative Fatigue Alert System

A production-ready automation system that audits Meta Ads campaigns daily, detects early performance risks, and sends actionable alerts when creatives show fatigue.

Built for marketers who want **signal, not noise**.

---

## 🚀 What this system does

### Daily (Automated)
- Audits all Meta ad campaigns
- Compares **last 7 days vs previous 7 days**
- Evaluates CTR, CPM, Frequency, and Spend
- Sends a **daily HTML audit email** with:
  - Campaign overview
  - Performance health
  - Red flags
  - Opportunities
  - Suggested actions

### Real-time (Conditional)
- Detects **creative fatigue at ad level**
- Triggers **critical alerts only** (with cooldown)
- Prevents repeated alerts for the same ad within 48 hours

---

## 🧠 Key Design Principles

- **Audit ≠ Alert**
  - Audit is informational (daily)
  - Alerts are actionable (only when critical)

- **Rolling comparison**
  - Uses last 7 days vs previous 7 days
  - Avoids single-day noise

- **Noise control**
  - Cooldown logic prevents alert spam
  - Skips ads/campaigns without baseline data

---

## 📊 Fatigue & Health Logic

### ⚠️ Warning (shown in daily audit)
Triggered if **any one** is true:
- CTR drop ≥ 15%
- CPM rise ≥ 15%
- Frequency ≥ 2.2

### 🚨 Critical (instant alert)
Triggered if **all** are true:
- CTR drop ≥ 25%
- CPM rise ≥ 25%
- Frequency ≥ 2.8
- Spend ≥ ₹2,000 (last 7 days)

### Campaign Escalation
- If 2+ ads in the same campaign are warning/critical
- Or 1 critical ad + high campaign frequency

---

## 🗂 Project Structure

src/
├── main.py # Orchestrator
├── meta_ads.py # Ad-level Meta API data
├── campaign_audit.py # Campaign-level audit logic
├── audit_report.py # HTML audit email generator
├── email_alert.py # Email sending (Brevo)
├── alert_state.py # Alert cooldown & deduplication


---

## ⚙️ Environment Variables

Required secrets:

META_ACCESS_TOKEN
META_AD_ACCOUNT_ID
BREVO_API_KEY
ALERT_EMAIL_FROM
ALERT_EMAIL_TO



Configured via:
- Local shell (for testing)
- GitHub Actions (for automation)

---

## 🤖 Automation

- Runs daily via **GitHub Actions**
- No manual intervention required
- Safe failure if credentials are missing

---

## 💡 Why this system is different

- Not a dashboard — **email-first**
- Not reactive — **trend-based**
- Not noisy — **cooldowns & escalation logic**
- Built like a real **Marketing Ops system**

---

## 📌 Future Enhancements (Optional)

- WhatsApp alerts for critical fatigue
- Google Sheets / CSV audit logs
- Budget pacing alerts
- Campaign scaling recommendations

🏗️ ARCHITECTURE DIAGRAM (SIMPLE & INTERVIEW-FRIENDLY)



                GitHub Actions (Daily Scheduler)
                            |
                            v
                  ┌─────────────────────┐
                  │      main.py         │
                  │  (Orchestrator)      │
                  └─────────────────────┘
                       |          |
        ┌──────────────┘          └──────────────┐
        v                                        v
┌───────────────┐                    ┌──────────────────┐
│ meta_ads.py   │                    │ campaign_audit.py │
│ (Ad-level)    │                    │ (Campaign-level)  │
└───────────────┘                    └──────────────────┘
        |                                        |
        v                                        v
┌───────────────┐                    ┌──────────────────┐
│ alert_state.py│                    │ audit_report.py   │
│ (Cooldowns)   │                    │ (HTML Builder)    │
└───────────────┘                    └──────────────────┘
        |                                        |
        v                                        v
┌────────────────────────────────────────────────────────┐
│                  email_alert.py                         │
│        (Brevo – alerts + daily audit email)             │
└────────────────────────────────────────────────────────┘
