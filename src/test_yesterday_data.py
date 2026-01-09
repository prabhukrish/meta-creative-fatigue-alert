from campaign_audit import get_yesterday_campaign_data

data = get_yesterday_campaign_data()

for k, v in data.items():
    print(v)
