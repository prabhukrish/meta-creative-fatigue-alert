import os
import requests
import json
from datetime import date, timedelta

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
GRAPH_API_VERSION = "v19.0"


def fetch_campaign_insights(date_preset=None, time_range=None):
    if not AD_ACCOUNT_ID:
        raise RuntimeError("META_AD_ACCOUNT_ID is not set")

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_id,campaign_name,ctr,cpm,frequency,spend",
        "level": "campaign",
        "limit": 100,
        "access_token": META_ACCESS_TOKEN,
    }

    if date_preset:
        params["date_preset"] = date_preset

    if time_range:
        params["time_range"] = json.dumps(time_range)

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


def classify_campaign_status(campaign):
    # WARNING thresholds
    if (
        campaign["ctr_drop_pct"] >= 15
        or campaign["cpm_rise_pct"] >= 15
        or campaign["frequency"] >= 2.2
    ):
        status = "WARNING"
    else:
        status = "HEALTHY"

    # CRITICAL thresholds override
    if (
        campaign["ctr_drop_pct"] >= 25
        or campaign["cpm_rise_pct"] >= 25
        or campaign["frequency"] >= 2.8
    ):
        status = "CRITICAL"

    return status


def get_campaign_audit_data():
    # Recent 7 days
    recent = fetch_campaign_insights(date_preset="last_7d")

    # Previous 7 days
    today = date.today()
    prev_end = today - timedelta(days=7)
    prev_start = today - timedelta(days=14)

    previous = fetch_campaign_insights(
        time_range={
            "since": prev_start.strftime("%Y-%m-%d"),
            "until": prev_end.strftime("%Y-%m-%d"),
        }
    )

    previous_lookup = {c["campaign_id"]: c for c in previous}

    audit_data = []

    for c in recent:
        prev = previous_lookup.get(c["campaign_id"])
        if not prev:
            continue

        ctr_prev = float(prev.get("ctr", 0))
        cpm_prev = float(prev.get("cpm", 0))

        # Skip campaigns without baseline
        if ctr_prev == 0 or cpm_prev == 0:
            continue

        ctr_recent = float(c.get("ctr", 0))
        cpm_recent = float(c.get("cpm", 0))

        campaign = {
            "campaign_id": c["campaign_id"],
            "campaign_name": c["campaign_name"],
            "spend": float(c.get("spend", 0)),
            "frequency": float(c.get("frequency", 0)),
            "ctr_recent": ctr_recent,
            "ctr_prev": ctr_prev,
            "ctr_drop_pct": round((ctr_prev - ctr_recent) / ctr_prev * 100, 1),
            "cpm_recent": cpm_recent,
            "cpm_prev": cpm_prev,
            "cpm_rise_pct": round((cpm_recent - cpm_prev) / cpm_prev * 100, 1),
        }

        campaign["status"] = classify_campaign_status(campaign)
        audit_data.append(campaign)

    return audit_data

def fetch_yesterday_campaign_metrics():
    """
    Fetch yesterday's performance metrics per campaign
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": (
            "campaign_id,"
            "campaign_name,"
            "spend,"
            "impressions,"
            "ctr,"
            "cpm,"
            "actions,"
            "cost_per_action_type"
        ),
        "level": "campaign",
        "date_preset": "yesterday",
        "limit": 100,
        "access_token": META_ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("data", [])

def extract_primary_result(campaign):
    """
    Extract result label + value dynamically
    """
    actions = campaign.get("actions", [])
    cost_actions = campaign.get("cost_per_action_type", [])

    if not actions:
        return {
            "result_label": "Results",
            "result_value": 0,
            "cost_per_result": None,
        }

    primary_action = actions[0]
    action_type = primary_action.get("action_type", "Results")
    value = float(primary_action.get("value", 0))

    cost_lookup = {
        c["action_type"]: float(c["value"])
        for c in cost_actions
    }

    return {
        "result_label": action_type.replace("_", " ").title(),
        "result_value": value,
        "cost_per_result": cost_lookup.get(action_type),
    }

def extract_primary_result(campaign):
    """
    Extract result label + value dynamically
    """
    actions = campaign.get("actions", [])
    cost_actions = campaign.get("cost_per_action_type", [])

    if not actions:
        return {
            "result_label": "Results",
            "result_value": 0,
            "cost_per_result": None,
        }

    primary_action = actions[0]
    action_type = primary_action.get("action_type", "Results")
    value = float(primary_action.get("value", 0))

    cost_lookup = {
        c["action_type"]: float(c["value"])
        for c in cost_actions
    }

    return {
        "result_label": action_type.replace("_", " ").title(),
        "result_value": value,
        "cost_per_result": cost_lookup.get(action_type),
    }

def get_yesterday_campaign_data():
    raw = fetch_yesterday_campaign_metrics()
    budgets = fetch_campaign_budgets()

    output = {}

    for c in raw:
        result_data = extract_primary_result(c)

        output[c["campaign_id"]] = {
            "campaign_name": c["campaign_name"],
            "y_budget": budgets.get(c["campaign_id"]),
            "y_spend": float(c.get("spend", 0)),
            "y_impressions": int(c.get("impressions", 0)),
            "y_ctr": float(c.get("ctr", 0)),
            "y_cpm": float(c.get("cpm", 0)),
            "y_results": result_data["result_value"],
            "y_result_label": result_data["result_label"],
            "y_cost_per_result": result_data["cost_per_result"],
        }

    return output




def fetch_campaign_budgets():
    """
    Fetch daily budgets for campaigns
    """
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{AD_ACCOUNT_ID}/campaigns"

    params = {
        "fields": "id,name,daily_budget",
        "limit": 100,
        "access_token": META_ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    budgets = {}
    for c in response.json().get("data", []):
        budgets[c["id"]] = (
            float(c["daily_budget"]) / 100
            if c.get("daily_budget")
            else None
        )

    return budgets
