from email_alert import send_email_alert
from mock_ads_data import ads_data

# Fatigue thresholds
CTR_DROP_THRESHOLD = 0.30
CPM_RISE_THRESHOLD = 0.25
MIN_FREQUENCY = 2.5
MIN_SPEND = 3000


def send_alert(ad):
    print("\n🚨🚨🚨 HIGH PRIORITY ALERT 🚨🚨🚨")
    print(f"Ad Name: {ad['ad_name']}")
    print("Issue: Creative Fatigue Detected")
    print("Recommended Actions:")
    print("1. Refresh creative immediately")
    print("2. Test new hook or format")
    print("3. Reduce frequency or pause ad")
    print("🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨\n")


print("\nRunning Creative Fatigue Monitoring...\n")

for ad in ads_data:
    ctr_drop = (ad["ctr_prev"] - ad["ctr_recent"]) / ad["ctr_prev"]
    cpm_rise = (ad["cpm_recent"] - ad["cpm_prev"]) / ad["cpm_prev"]

    is_fatigued = (
        ctr_drop >= CTR_DROP_THRESHOLD
        and cpm_rise >= CPM_RISE_THRESHOLD
        and ad["frequency"] >= MIN_FREQUENCY
        and ad["spend_recent"] >= MIN_SPEND
    )

    if is_fatigued:
        send_alert(ad)
print("🔍 Starting fatigue evaluation")

for ad in ads_data:
    print(f"Checking ad: {ad['ad_name']}")
    
    ctr_drop = (ad["ctr_prev"] - ad["ctr_recent"]) / ad["ctr_prev"]
    cpm_rise = (ad["cpm_recent"] - ad["cpm_prev"]) / ad["cpm_prev"]

    print(f"CTR drop: {ctr_drop:.2f}, CPM rise: {cpm_rise:.2f}")

    if is_fatigued:
        print("🚨 Fatigued ad detected")
        send_email_alert(ad)
    else:
        print("✅ Ad is healthy")


from email_alert import send_email_alert

print("🧪 FORCED EMAIL TEST STARTED")

test_ad = {
    "ad_name": "FORCED TEST AD – GITHUB ACTIONS"
}

send_email_alert(test_ad)

print("🧪 FORCED EMAIL TEST COMPLETED")

print("FORCE TEST")
send_email_alert({"ad_name": "LOCAL TERMINAL TEST"})

