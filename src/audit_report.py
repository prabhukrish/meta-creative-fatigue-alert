from datetime import date


def generate_audit_email(campaigns):
    today = date.today().strftime("%d %b %Y")

    total_spend = round(sum(c["spend"] for c in campaigns), 2)

    healthy = sum(1 for c in campaigns if c["status"] == "HEALTHY")
    warning = sum(1 for c in campaigns if c["status"] == "WARNING")
    critical = sum(1 for c in campaigns if c["status"] == "CRITICAL")

    rows = ""
    for c in campaigns:
        color = {
            "HEALTHY": "#e6fffa",
            "WARNING": "#fff5e6",
            "CRITICAL": "#ffe6e6"
        }[c["status"]]

        rows += f"""
        <tr style="background-color:{color}">
            <td>{c['campaign_name']}</td>
            <td>₹{c['spend']}</td>
            <td>{c['ctr_drop_pct']}%</td>
            <td>{c['cpm_rise_pct']}%</td>
            <td>{c['frequency']}</td>
            <td><b>{c['status']}</b></td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>Daily Meta Ads Audit – {today}</h2>

        <p>
            Campaigns audited: <b>{len(campaigns)}</b><br>
            🟢 Healthy: <b>{healthy}</b> |
            ⚠️ Warning: <b>{warning}</b> |
            🚨 Critical: <b>{critical}</b><br>
            Total Spend (7d): <b>₹{total_spend}</b>
        </p>

        <table border="1" cellpadding="8" cellspacing="0" width="100%">
            <tr style="background-color:#f0f0f0">
                <th align="left">Campaign</th>
                <th align="left">Spend (₹)</th>
                <th align="left">CTR Δ %</th>
                <th align="left">CPM Δ %</th>
                <th align="left">Frequency</th>
                <th align="left">Status</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

    return html
