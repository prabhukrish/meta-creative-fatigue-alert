import streamlit as st
from src.campaign_audit import get_campaign_audit_data
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Meta Ads Audit Dashboard", layout="wide")

st.title("📊 Meta Ads Daily Audit Dashboard")
st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

st.divider()

campaigns = get_campaign_audit_data()
df = pd.DataFrame(campaigns)

# KPI counts
total = len(df)
healthy = len(df[df["status"] == "HEALTHY"])
warning = len(df[df["status"] == "WARNING"])
critical = len(df[df["status"] == "CRITICAL"])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Campaigns", total)
c2.metric("🟢 Healthy", healthy)
c3.metric("⚠️ Warning", warning)
c4.metric("🚨 Critical", critical)

st.divider()

st.subheader("Campaign Health Table")

status_filter = st.multiselect(
    "Filter by status",
    options=["HEALTHY", "WARNING", "CRITICAL"],
    default=["WARNING", "CRITICAL"],
)

filtered_df = df[df["status"].isin(status_filter)]

def highlight_status(row):
    if row["status"] == "CRITICAL":
        return ["background-color: #ffe6e6"] * len(row)
    elif row["status"] == "WARNING":
        return ["background-color: #fff5e6"] * len(row)
    else:
        return ["background-color: #e6fffa"] * len(row)


st.dataframe(
    filtered_df.style.apply(highlight_status, axis=1),
    use_container_width=True,
)
