from mock_ads_data import ads_data

# Fatigue thresholds
CTR_DROP_THRESHOLD = 0.30
CPM_RISE_THRESHOLD = 0.25
MIN_FREQUENCY = 2.5
MIN_SPEND = 3000

print("\n🚨 Running Creative Fatigue Check 🚨\n")

fatigued_ads = []

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
        fatigued_ads.append(ad)

# High alert section
if fatigued_ads:
    print("🚨 HIGH ALERT: CREATIVE FATIGUE DETECTED 🚨\n")

    for ad in fatigued_ads:
        print(f"Ad Name: {ad['ad_name']}")
        print("Recommended Action:")
        print("- Refresh creative immediately")
        print("- Test new hook or format")
        print("- Reduce frequency or pause ad")
        print("-" * 50)
else:
    print("✅ All creatives are healthy. No action needed.")
