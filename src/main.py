"""
Main Orchestrator
-----------------
1. Runs creative fatigue detection (ad level)
2. Sends critical fatigue alerts (with cooldown)
3. Sends daily campaign audit email
"""

# ===== Imports =====
from meta_ads import fetch_ads_data
from campaign_audit import get_campaign_audit_data
from audit_report import generate_audit_email
from email_alert import send_email_alert, send_daily_audit_email
from alert_state import should_alert, record_alert


# ===== Fatigue Thresholds (CRITICAL) =====
CTR_DROP_THRESHOLD = 0.25
CPM_RISE_THRESHOLD = 0.25
MIN_FREQUENCY = 2.8
MIN_SPEND = 2000


def run_creative_fatigue_check():
    print("\n🔍 Running Creative Fatigue Monitoring...\n")

    ads_data = fetch_ads_data()

    for ad in ads_data:
        # Skip ads with no baseline data
        if ad["ctr_prev"] == 0 or ad["cpm_prev"] == 0:
            print(f"⏭ Skipping ad (no baseline): {ad['ad_name']}")
            continue

        ctr_drop = (ad["ctr_prev"] - ad["ctr_recent"]) / ad["ctr_prev"]
        cpm_rise = (ad["cpm_recent"] - ad["cpm_prev"]) / ad["cpm_prev"]

        is_fatigued = (
            ctr_drop >= CTR_DROP_THRESHOLD
            and cpm_rise >= CPM_RISE_THRESHOLD
            and ad["frequency"] >= MIN_FREQUENCY
            and ad["spend_recent"] >= MIN_SPEND
        )

        if is_fatigued:
            ad_id = ad.get("ad_id")

            if should_alert(ad_id):
                print(f"🚨 CRITICAL fatigue detected: {ad['ad_name']}")
                send_email_alert(ad)
                record_alert(ad_id)
            else:
                print(f"⏸ Alert skipped (cooldown active): {ad['ad_name']}")
        else:
            print(f"✅ Ad healthy: {ad['ad_name']}")


def run_daily_campaign_audit():
    print("\n📊 Generating daily campaign audit...\n")

    campaigns = get_campaign_audit_data()
    audit_html = generate_audit_email(campaigns)

    send_daily_audit_email(audit_html)

    print("✅ Daily audit email sent")


# ===== Entry Point =====
if __name__ == "__main__":
    run_creative_fatigue_check()
    run_daily_campaign_audit()
