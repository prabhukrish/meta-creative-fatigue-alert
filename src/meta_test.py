import requests

import os
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = "act_2038695363582581"

url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/insights"

params = {
    "fields": "ad_name,ctr,cpm,frequency,spend",
    "level": "ad",
    "date_preset": "last_7d",
    "limit": 5,
    "access_token": ACCESS_TOKEN
}


response = requests.get(url, params=params)

print("Status code:", response.status_code)
print("Response:", response.json())
