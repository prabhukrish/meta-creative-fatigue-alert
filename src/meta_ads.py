import os
import requests

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")

GRAPH_API_VERSION = "v19.0"


def fetch_ads_data(days="last_7d"):
    """
    Fetch ad-level metrics from Meta Ads API
    and normalize them into fatigue engine format
    """

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "ad_name,ctr,cpm,frequency,spend",
        "level": "ad",
        "date_preset": days,
        "limit": 100,
        "access_token": META_ACCESS_TOKEN
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    raw_data = response.json().get("data", [])

    ads_data = []

    for ad in raw_data:
        ads_data.append({
            "ad_name": ad.get("ad_name"),
            "ctr_recent": float(ad.get("ctr", 0)),
            "ctr_prev": float(ad.get("ctr", 0)),      # placeholder (Phase 4)
            "cpm_recent": float(ad.get("cpm", 0)),
            "cpm_prev": float(ad.get("cpm", 0)),      # placeholder (Phase 4)
            "frequency": float(ad.get("frequency", 0)),
            "spend_recent": float(ad.get("spend", 0))
        })

    return ads_data
