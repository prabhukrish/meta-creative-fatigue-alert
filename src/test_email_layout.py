from audit_report import generate_audit_email

mock_campaigns = [
    {
        "campaign_id": "1",
        "campaign_name": "IELTS Leads",
        "ctr_drop_pct": 18,
        "cpm_rise_pct": 22,
        "frequency": 2.6,
        "status": "WARNING",
    }
]

mock_yesterday = {
    "1": {
        "y_results": 42,
        "y_result_label": "Leads",
        "y_cost_per_result": 185,
        "y_spend": 7770,
        "y_ctr": 1.12,
        "y_cpm": 165,
    }
}

html = generate_audit_email(mock_campaigns, mock_yesterday)
print(html)
