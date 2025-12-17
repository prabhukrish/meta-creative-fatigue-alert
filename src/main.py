from mock_ads_data import ads_data

print("Checking ads performance...\n")

for ad in ads_data:
    print(f"Ad Name: {ad['ad_name']}")
    print(f"Previous CTR: {ad['ctr_prev']}%")
    print(f"Recent CTR: {ad['ctr_recent']}%")
    print(f"Previous CPM: ₹{ad['cpm_prev']}")
    print(f"Recent CPM: ₹{ad['cpm_recent']}")
    print(f"Frequency: {ad['frequency']}")
    print(f"Recent Spend: ₹{ad['spend_recent']}")
    print("-" * 40)
