from datetime import date


def generate_audit_email(campaigns, yesterday_data):
    today = date.today().strftime("%d %b %Y")

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>📊 Meta Ads Daily Audit – {today}</h2>
        <p>Yesterday’s performance and current campaign health.</p>

        <h3>Yesterday Performance</h3>
        <table border="1" cellpadding="6" cellspacing="0" width="100%">
            <tr>
                <th>Campaign</th>
                <th>Daily Budget</th>
                <th>Spend</th>
                <th>Impressions</th>
                <th>Results</th>
                <th>Cost / Result</th>
                <th>CTR</th>
                <th>CPM</th>
            </tr>
    """

    for c in campaigns:
        y = yesterday_data.get(c["campaign_id"], {})

        html += f"""
        <tr>
            <td>{c['campaign_name']}</td>
            <td>{y.get('y_budget', '-')}</td>
            <td>₹{y.get('y_spend', 0)}</td>
            <td>{y.get('y_impressions', 0)}</td>
            <td>{y.get('y_result_label', 'Results')}: {y.get('y_results', 0)}</td>
            <td>{y.get('y_cost_per_result', '-')}</td>
            <td>{y.get('y_ctr', 0)}%</td>
            <td>₹{y.get('y_cpm', 0)}</td>
        </tr>
        """

    html += """
        </table>

        <h3>Campaign Health & Fatigue</h3>
        <table border="1" cellpadding="6" cellspacing="0" width="100%">
            <tr>
                <th>Campaign</th>
                <th>CTR Δ % (7d)</th>
                <th>CPM Δ % (7d)</th>
                <th>Frequency</th>
                <th>Status</th>
            </tr>
    """

    for c in campaigns:
        color = {
            "HEALTHY": "#e6fffa",
            "WARNING": "#fff5e6",
            "CRITICAL": "#ffe6e6",
        }.get(c["status"], "#ffffff")

        html += f"""
        <tr style="background-color:{color}">
            <td>{c['campaign_name']}</td>
            <td>{c['ctr_drop_pct']}%</td>
            <td>{c['cpm_rise_pct']}%</td>
            <td>{c['frequency']}</td>
            <td><b>{c['status']}</b></td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html
