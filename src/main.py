from mock_ads_data import ads_data

# Fatigue thresholds
CTR_DROP_THRESHOLD = 0.30
CPM_RISE_THRESHOLD = 0.25
MIN_FREQUENCY = 2.5
MIN_SPEND = 3000

print("\nChecking creative fatigue...\n")

for ad in ads_data:
    ctr_drop = (ad["ctr_prev"] - ad["ctr_recent"]) / ad["ctr_prev"]
    cpm_rise = (ad["cpm_recent"] - ad["cpm_prev"]) / ad["cpm_prev"]

    is_fatigued = (
        ctr_drop >= CTR_DROP_THRESHOLD
        and cpm_rise >= CPM_RISE_THRESHOLD
        and ad["frequency"] >= MIN_FREQUENCY
        and ad["spend_recent"] >= MIN_SPEND
    )

    status = "FATIGUED 🚨" if is_fatigued else "OK ✅"

    print(f"Ad: {ad['ad_name']}")
    print(f"Status: {status}")
    print("-" * 40)
