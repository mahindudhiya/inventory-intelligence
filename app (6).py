import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Inventory Intelligence System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .metric-card {
        background: #fff; border: 1px solid #e5e7eb;
        border-radius: 12px; padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-label { font-size: 11px; color: #6b7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }
    .metric-value { font-size: 30px; font-weight: 700; color: #111827; margin: 4px 0 2px; }
    .metric-delta { font-size: 12px; font-weight: 500; }
    .metric-delta.pos { color: #10b981; }
    .metric-delta.neg { color: #ef4444; }
    .metric-delta.neutral { color: #6366f1; }

    .sku-card {
        background: #fff; border: 1px solid #e5e7eb;
        border-left: 4px solid; border-radius: 8px;
        padding: 14px 16px; margin-bottom: 10px;
    }
    .sku-card.reorder  { border-left-color: #ef4444; }
    .sku-card.watch    { border-left-color: #f59e0b; }
    .sku-card.healthy  { border-left-color: #10b981; }
    .sku-card.overstock{ border-left-color: #6366f1; }

    .ai-box {
        background: #f0f9ff; border: 1px solid #bae6fd;
        border-radius: 8px; padding: 12px 14px;
        font-size: 13px; color: #0c4a6e; line-height: 1.6;
    }
    .ai-label { font-size: 10px; font-weight: 700; color: #0369a1; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }

    .copilot-box {
        background: #f5f3ff; border: 1px solid #ddd6fe;
        border-radius: 8px; padding: 12px 14px;
        font-size: 13px; color: #4c1d95; line-height: 1.6;
    }

    .tag {
        display: inline-block; padding: 2px 9px; border-radius: 99px;
        font-size: 11px; font-weight: 600; margin-right: 4px;
    }
    .tag-reorder   { background: #fee2e2; color: #991b1b; }
    .tag-watch     { background: #fef3c7; color: #92400e; }
    .tag-healthy   { background: #d1fae5; color: #065f46; }
    .tag-overstock { background: #ede9fe; color: #5b21b6; }

    div[data-testid="stSidebarContent"] { background: #f9fafb; }
</style>
""", unsafe_allow_html=True)


# ─── Data ───────────────────────────────────────────────────────────────────────
random.seed(7)
np.random.seed(7)

LOCATIONS = ["Thrills & Chills", "Alpine Outfitters", "Main Gate Gifts", "Splash Zone", "Wild Zone", "Cedar Junction", "Gold Mine", "Park Ave Market"]

SKUS = [
    {"sku":"WL-1042","name":"Wonderland Logo Tee","location":"Main Gate Gifts","category":"Apparel","current_stock":12,"reorder_point":25,"velocity":8.4,"days_remaining":1,"status":"reorder","revenue_weekly":840,"margin":0.62,"ai_rec":"Stock critically low. Velocity 8.4 units/day means stockout within 1–2 days. Reorder 200 units immediately. Peak weekend ahead — do not delay."},
    {"sku":"WL-2018","name":"Roller Coaster Plush (Large)","location":"Thrills & Chills","category":"Toys","current_stock":8,"reorder_point":20,"velocity":3.2,"days_remaining":2,"status":"reorder","revenue_weekly":480,"margin":0.71,"ai_rec":"Near stockout. High-margin item (71%). Reorder 150 units — lead time is 4 days, act now to avoid gap. Upsell opportunity at checkout."},
    {"sku":"WL-3301","name":"Cedar Crest Hoodie","location":"Alpine Outfitters","category":"Apparel","current_stock":47,"reorder_point":30,"velocity":4.1,"days_remaining":11,"status":"watch","revenue_weekly":1120,"margin":0.58,"ai_rec":"11 days of stock remaining. Weekend traffic expected to spike velocity. Recommend placing a reorder in the next 3 days to avoid stockout during peak period."},
    {"sku":"WL-4455","name":"Splash Zone Keychain Set","location":"Splash Zone","category":"Accessories","current_stock":310,"reorder_point":80,"velocity":5.2,"days_remaining":59,"status":"overstock","revenue_weekly":260,"margin":0.44,"ai_rec":"Overstocked at 59-day supply. Velocity declining. Recommend promotional bundling with high-velocity Splash Zone items or cross-display at Main Gate to move units."},
    {"sku":"WL-5120","name":"Park Map & Guide Booklet","location":"All Locations","category":"Stationery","current_stock":189,"reorder_point":100,"velocity":9.8,"days_remaining":19,"status":"healthy","revenue_weekly":490,"margin":0.38,"ai_rec":"Healthy stock level. High velocity (9.8/day). Monitor weekly — approaching reorder point if velocity holds. No action needed this cycle."},
    {"sku":"WL-6080","name":"Wild Zone Water Bottle","location":"Wild Zone","category":"Accessories","current_stock":23,"reorder_point":40,"velocity":5.8,"days_remaining":3,"status":"reorder","revenue_weekly":580,"margin":0.52,"ai_rec":"Below reorder point. 3-day supply. High correlation with hot weather forecast this weekend. Reorder 120 units — request expedited delivery from supplier."},
    {"sku":"WL-7211","name":"Canada's Wonderland Snapback","location":"Cedar Junction","category":"Apparel","current_stock":88,"reorder_point":35,"velocity":2.9,"days_remaining":30,"status":"healthy","revenue_weekly":580,"margin":0.64,"ai_rec":"30-day supply. Healthy margin (64%). No action needed. Flag for seasonal review — demand tends to drop post-August."},
    {"sku":"WL-8003","name":"Gold Rush Plush Assortment","location":"Gold Mine","category":"Toys","current_stock":64,"reorder_point":45,"velocity":3.7,"days_remaining":17,"status":"watch","revenue_weekly":740,"margin":0.68,"ai_rec":"Watch status — stock will hit reorder point in ~17 days. High-margin assortment (68%). Recommend pre-emptive reorder this week to avoid stockout during school holiday week."},
]

WEEKLY_SALES = pd.DataFrame({
    "week": ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10","W11","W12"],
    "Thrills & Chills":   [18400,19200,17800,21000,22400,23100,21800,24000,25200,26100,24800,27300],
    "Alpine Outfitters":  [14200,15100,14800,16200,17400,18200,17100,19000,20100,21200,19800,22100],
    "Main Gate Gifts":    [22100,23400,21800,24200,25800,27100,26200,28400,29800,31200,30100,33400],
    "Splash Zone":        [9800,10200,9400,11200,12800,13400,12100,14200,15800,16200,14800,17100],
    "Wild Zone":          [11200,12100,11400,12800,14200,15100,13800,15800,16900,18100,16800,19200],
})

STOCKOUT_TREND = pd.DataFrame({
    "week": ["W1","W2","W3","W4","W5","W6","W7","W8","W9","W10","W11","W12"],
    "before_ai": [14,16,13,18,15,17,14,None,None,None,None,None],
    "after_ai":  [None,None,None,None,None,None,14,9,7,5,4,3],
})

REPORT_TIME = pd.DataFrame({
    "week": ["W1","W2","W3","W4","W5","W6","W7","W8"],
    "manual_mins": [240,255,240,260,240,250,240,255],
    "copilot_mins": [55,48,42,40,38,36,35,34],
})

LOCATION_KPI = pd.DataFrame({
    "location": LOCATIONS,
    "revenue":    [142000, 118000, 198000, 87000, 102000, 94000, 76000, 61000],
    "stockouts":  [3, 2, 4, 1, 2, 2, 1, 0],
    "turnover":   [4.2, 3.8, 5.1, 3.4, 4.0, 3.6, 3.2, 2.9],
    "accuracy":   [94, 97, 91, 98, 96, 95, 97, 99],
})

AUDIT_DATA = pd.DataFrame({
    "month": ["May","Jun","Jul","Aug","Sep","Oct"],
    "transactions": [1420,1980,2240,2810,1640,920],
    "discrepancies": [38,29,22,18,12,8],
    "accuracy_pct": [97.3,98.5,99.0,99.4,99.3,99.1],
})


# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📦 AI Inventory Intelligence")
    st.markdown("---")
    view = st.radio("View", [
        "📊 Operations Overview",
        "🤖 AI SKU Agent",
        "📈 KPI Dashboard",
        "🧾 Reporting Automation",
        "🔍 Transaction Audit",
        "🔌 System Architecture",
    ])
    st.markdown("---")
    st.markdown("**Context:** Canada's Wonderland")
    st.markdown("**Role:** Product Mgmt Supervisor")
    st.markdown("**Stack:** Python · GPT-4 · Copilot")
    st.markdown("**Tools:** DataWorks · Excel · Asana")
    st.markdown("**Impact:** 83% report time ↓ · $5K saved")


# ─── Views ───────────────────────────────────────────────────────────────────────

# ── Operations Overview ───────────────────────────────────────────────────────────
if view == "📊 Operations Overview":
    st.markdown("## Operations Overview")

    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        ("Locations Managed","8+","merchandise ops","neutral"),
        ("Transactions Audited","10,000+","across all locations","neutral"),
        ("Report Time","45 min","↓ from 4 hours (83%)","pos"),
        ("Stockout Incidents","3","↓ from 15 per season","pos"),
        ("Annual Savings","$5,000+","process efficiency","pos"),
    ]
    for col,(label,val,delta,cls) in zip([c1,c2,c3,c4,c5],kpis):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div><div class="metric-delta {cls}">{delta}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Weekly Sales by Location (Top 5)")
        fig = go.Figure()
        colors = ["#6366f1","#10b981","#f59e0b","#ef4444","#8b5cf6"]
        for i, loc in enumerate(["Thrills & Chills","Alpine Outfitters","Main Gate Gifts","Splash Zone","Wild Zone"]):
            fig.add_trace(go.Scatter(
                x=WEEKLY_SALES["week"], y=WEEKLY_SALES[loc],
                name=loc, mode="lines", line=dict(color=colors[i], width=2),
            ))
        fig.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#fafafa", paper_bgcolor="white",
                          legend=dict(orientation="h", y=-0.3, font=dict(size=10)),
                          yaxis=dict(tickprefix="$", tickformat=",.0f"),)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Stockout Incidents: Before vs. After AI")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=STOCKOUT_TREND["week"], y=STOCKOUT_TREND["before_ai"],
            name="Before AI", mode="lines+markers",
            line=dict(color="#ef4444", width=2, dash="dash"), marker=dict(size=7), connectgaps=False
        ))
        fig2.add_trace(go.Scatter(
            x=STOCKOUT_TREND["week"], y=STOCKOUT_TREND["after_ai"],
            name="After AI", mode="lines+markers",
            line=dict(color="#10b981", width=2.5), marker=dict(size=7),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.07)", connectgaps=False
        ))
        fig2.add_vline(x="W7", line_dash="dot", line_color="#6366f1",
                       annotation_text="AI Deployed", annotation_position="top left")
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#fafafa", paper_bgcolor="white",
                           yaxis_title="Stockout Incidents",
                           legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Revenue by Location")
    fig3 = px.bar(LOCATION_KPI, x="location", y="revenue",
                  color="revenue", color_continuous_scale=["#ddd6fe","#6366f1"],
                  labels={"revenue":"Revenue ($)","location":"Location"})
    fig3.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="#fafafa", paper_bgcolor="white",
                       showlegend=False, coloraxis_showscale=False,
                       yaxis=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig3, use_container_width=True)


# ── AI SKU Agent ───────────────────────────────────────────────────────────────
elif view == "🤖 AI SKU Agent":
    st.markdown("## AI SKU Analysis Agent")
    st.markdown("Each SKU is processed through a Python + GPT-4 pipeline that calculates days-remaining, flags status, and generates a natural-language action recommendation synced to Asana.")

    status_filter = st.multiselect("Filter by Status", ["reorder","watch","healthy","overstock"], default=["reorder","watch","healthy","overstock"])
    filtered = [s for s in SKUS if s["status"] in status_filter]

    for sku in sorted(filtered, key=lambda x: x["days_remaining"]):
        with st.expander(f"**{sku['sku']}** — {sku['name']} · {sku['location']} · {sku['days_remaining']}d remaining"):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown(f"**Category:** {sku['category']}")
                st.markdown(f"**Current Stock:** {sku['current_stock']} units")
                st.markdown(f"**Reorder Point:** {sku['reorder_point']} units")
                st.markdown(f"**Daily Velocity:** {sku['velocity']} units/day")
                st.markdown(f"**Days Remaining:** {sku['days_remaining']}")
                st.markdown(f"**Weekly Revenue:** ${sku['revenue_weekly']:,}")
                st.markdown(f"**Gross Margin:** {int(sku['margin']*100)}%")

                status_colors = {"reorder":"🔴","watch":"🟡","healthy":"🟢","overstock":"🟣"}
                st.markdown(f"**Status:** {status_colors[sku['status']]} `{sku['status'].upper()}`")

            with col2:
                # Stock gauge
                stock_pct = min(sku["current_stock"] / (sku["reorder_point"] * 3) * 100, 100)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=sku["current_stock"],
                    title={"text": "Current Stock (units)", "font": {"size": 13}},
                    gauge={
                        "axis": {"range": [0, sku["reorder_point"]*3]},
                        "bar": {"color": "#ef4444" if sku["status"]=="reorder" else "#f59e0b" if sku["status"]=="watch" else "#10b981"},
                        "steps": [
                            {"range": [0, sku["reorder_point"]], "color": "#fee2e2"},
                            {"range": [sku["reorder_point"], sku["reorder_point"]*2], "color": "#fef3c7"},
                        ],
                        "threshold": {"line": {"color": "#ef4444", "width": 3}, "thickness": 0.8, "value": sku["reorder_point"]}
                    }
                ))
                fig.update_layout(height=220, margin=dict(t=30,b=10,l=20,r=20))
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="ai-label">🤖 GPT-4 SKU Recommendation</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ai-box">{sku["ai_rec"]}</div>', unsafe_allow_html=True)


# ── KPI Dashboard ──────────────────────────────────────────────────────────────
elif view == "📈 KPI Dashboard":
    st.markdown("## KPI Dashboard — 15+ Metrics Tracked")
    st.markdown("Automated KPI tracking built in Excel + DataWorks, replacing manual multi-location reporting.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Inventory Turnover by Location")
        fig = px.bar(LOCATION_KPI, x="turnover", y="location", orientation="h",
                     color="turnover", color_continuous_scale=["#ddd6fe","#6366f1"],
                     labels={"turnover":"Turnover Rate","location":""})
        fig.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#fafafa", paper_bgcolor="white",
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Inventory Accuracy by Location")
        fig2 = px.bar(LOCATION_KPI, x="location", y="accuracy",
                      color="accuracy", color_continuous_scale=["#fef3c7","#10b981"],
                      labels={"accuracy":"Accuracy (%)","location":""},
                      range_y=[85,100])
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#fafafa", paper_bgcolor="white",
                           coloraxis_showscale=False,
                           xaxis=dict(tickangle=-30, tickfont=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### SKU Status Distribution (All Locations)")
        status_counts = {"Reorder Now":3,"Watch":2,"Healthy":2,"Overstock":1}
        fig3 = px.pie(names=list(status_counts.keys()), values=list(status_counts.values()),
                      hole=0.55, color_discrete_sequence=["#ef4444","#f59e0b","#10b981","#6366f1"])
        fig3.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                           legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### Weekly Revenue — All Locations")
        total_weekly = WEEKLY_SALES.set_index("week").sum(axis=1).reset_index()
        total_weekly.columns = ["week","total"]
        fig4 = px.area(total_weekly, x="week", y="total",
                       color_discrete_sequence=["#6366f1"],
                       labels={"total":"Total Revenue ($)","week":"Week"})
        fig4.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#fafafa", paper_bgcolor="white",
                           yaxis=dict(tickprefix="$",tickformat=",.0f"))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Full Location KPI Table")
    display_df = LOCATION_KPI.copy()
    display_df["revenue"] = display_df["revenue"].apply(lambda x: f"${x:,}")
    display_df["accuracy"] = display_df["accuracy"].apply(lambda x: f"{x}%")
    display_df.columns = ["Location","Revenue","Stockouts","Turnover Rate","Inventory Accuracy"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ── Reporting Automation ──────────────────────────────────────────────────────
elif view == "🧾 Reporting Automation":
    st.markdown("## Reporting Automation — Microsoft Copilot")
    st.markdown("Weekly operational reporting was reduced from **4 hours to 45 minutes** using Microsoft Copilot + Excel automation, saving $5,000+ annually in labour time.")

    col1, col2, col3, col4 = st.columns(4)
    for col,(label,val,delta,cls) in zip([col1,col2,col3,col4],[
        ("Before: Report Time","4 hours","manual pull & format","neg"),
        ("After: Report Time","45 min","with Copilot","pos"),
        ("Time Saved","83%","per weekly cycle","pos"),
        ("Annual Labour Saving","$5,000+","fully automated","pos"),
    ]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div><div class="metric-delta {cls}">{delta}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Weekly Report Generation Time (Minutes)")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=REPORT_TIME["week"], y=REPORT_TIME["manual_mins"],
            name="Manual Process", marker_color="#e5e7eb", marker_line_width=0))
        fig.add_trace(go.Bar(x=REPORT_TIME["week"], y=REPORT_TIME["copilot_mins"],
            name="Copilot Assisted", marker_color="#6366f1", marker_line_width=0))
        fig.update_layout(height=300, barmode="group", margin=dict(t=10,b=10,l=10,r=10),
                          yaxis_title="Minutes", plot_bgcolor="#fafafa", paper_bgcolor="white",
                          legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Time Saved Per Week (Minutes)")
        REPORT_TIME["saved"] = REPORT_TIME["manual_mins"] - REPORT_TIME["copilot_mins"]
        fig2 = px.area(REPORT_TIME, x="week", y="saved",
                       color_discrete_sequence=["#10b981"],
                       labels={"saved":"Minutes Saved","week":"Week"})
        fig2.update_traces(fill="tozeroy", fillcolor="rgba(16,185,129,0.1)")
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="#fafafa", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### What Copilot Automated")
    steps = [
        ("1. Data Pull", "Copilot connected to DataWorks and Excel files across all 8 locations, pulling last 7 days of sales, stock, and transaction data automatically."),
        ("2. Cross-Location Merge", "Python script merged multi-source data into a single normalized dataset — eliminating manual copy-paste across spreadsheets."),
        ("3. KPI Calculation", "15+ KPIs calculated automatically: sell-through rate, turnover, stockout rate, margin by SKU, revenue by location."),
        ("4. Report Generation", "Copilot formatted the final report in the standard Excel template with conditional formatting, charts, and location tabs — ready to send."),
        ("5. Distribution", "Automated email distribution via Outlook + Power Automate — no manual sending required."),
    ]
    for title, desc in steps:
        with st.expander(f"**{title}**"):
            st.markdown(f'<div class="copilot-box">{desc}</div>', unsafe_allow_html=True)


# ── Transaction Audit ──────────────────────────────────────────────────────────
elif view == "🔍 Transaction Audit":
    st.markdown("## Transaction Audit & Shrink Analysis")
    st.markdown("Audited 10,000+ transactions to identify shrink, reconciliation errors, and inventory discrepancies across 8+ locations. Improved accuracy from 91% to 99%+.")

    col1,col2,col3,col4 = st.columns(4)
    for col,(label,val,delta,cls) in zip([col1,col2,col3,col4],[
        ("Transactions Audited","10,000+","May–Oct 2025","neutral"),
        ("Initial Accuracy","91%","before reconciliation","neg"),
        ("Post-Audit Accuracy","99.1%","after process fix","pos"),
        ("Discrepancies Found","127","resolved via workflow redesign","neutral"),
    ]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div><div class="metric-delta {cls}">{delta}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Monthly Transaction Volume")
        fig = px.bar(AUDIT_DATA, x="month", y="transactions",
                     color_discrete_sequence=["#6366f1"],
                     labels={"transactions":"Transactions","month":"Month"})
        fig.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                          plot_bgcolor="#fafafa", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### Inventory Accuracy Over Time")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=AUDIT_DATA["month"], y=AUDIT_DATA["accuracy_pct"],
            mode="lines+markers", name="Accuracy %",
            line=dict(color="#10b981", width=2.5),
            marker=dict(size=8, color="#10b981"),
            fill="tozeroy", fillcolor="rgba(16,185,129,0.07)"))
        fig2.add_hline(y=99, line_dash="dot", line_color="#6366f1",
                       annotation_text="Target: 99%", annotation_position="bottom right")
        fig2.update_layout(height=280, margin=dict(t=10,b=10,l=10,r=10),
                           yaxis=dict(range=[89,100], title="Accuracy (%)"),
                           plot_bgcolor="#fafafa", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Discrepancies Found & Resolved by Month")
    fig3 = px.bar(AUDIT_DATA, x="month", y="discrepancies",
                  color="discrepancies", color_continuous_scale=["#10b981","#ef4444"],
                  labels={"discrepancies":"Discrepancies","month":"Month"})
    fig3.update_layout(height=260, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="#fafafa", paper_bgcolor="white",
                       coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Workflow Redesign — Root Causes Fixed")
    causes = {
        "Double-entry across POS and DataWorks": "Eliminated via automated sync script",
        "Manual stock counts not reconciled": "Replaced with cycle count schedule + audit trail",
        "Shrink not categorized (damage vs theft)": "New shrink tagging taxonomy implemented",
        "Transfer records not logged in real-time": "Mandatory transfer log at point of move",
        "Seasonal hire data entry errors": "Validation rules added to POS entry screens",
    }
    for cause, fix in causes.items():
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(f"🔴 **{cause}**")
        with col_r:
            st.markdown(f"✅ {fix}")
        st.markdown("---")


# ── System Architecture ────────────────────────────────────────────────────────
elif view == "🔌 System Architecture":
    st.markdown("## System Architecture & Tech Stack")
    st.markdown("How the data sources, AI agents, and automation tools connect end-to-end.")

    st.markdown("""
    ```
    ┌────────────────────────────────────────────────────────────┐
    │                     DATA SOURCES                           │
    │   POS Systems (8 locations) → DataWorks → Excel Files     │
    └───────────────────────┬────────────────────────────────────┘
                            │
                            ▼
    ┌────────────────────────────────────────────────────────────┐
    │              PYTHON DATA PIPELINE                          │
    │   pandas merge → clean → normalize → compute KPIs         │
    │   10,000+ transactions · 15+ KPI calculations             │
    └───────────────────────┬────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              ▼                            ▼
    ┌─────────────────┐          ┌─────────────────────┐
    │  GPT-4 SKU      │          │  Microsoft Copilot  │
    │  Analysis Agent │          │  Reporting Agent    │
    │                 │          │                     │
    │ • Score SKUs    │          │ • Auto-format Excel │
    │ • Flag status   │          │ • Generate KPI      │
    │ • Recommend     │          │   summary report    │
    │   action        │          │ • 4hr → 45min       │
    └────────┬────────┘          └──────────┬──────────┘
             │                              │
             ▼                              ▼
    ┌─────────────────┐          ┌─────────────────────┐
    │  Asana Tasks    │          │  Excel Dashboard    │
    │  (Reorder       │          │  (15+ KPIs,         │
    │   actions)      │          │   8 locations)      │
    └─────────────────┘          └─────────────────────┘
             │                              │
             └──────────────┬───────────────┘
                            ▼
                    Slack Alerts (threshold breaches)
    ```
    """)

    st.markdown("#### Tech Stack")
    stack = {
        "Data Layer": ["Python 3.11","pandas","DataWorks API","Excel (Office 365)"],
        "AI Agents": ["OpenAI GPT-4","Microsoft Copilot","Prompt Engineering","Structured JSON output"],
        "Automation": ["n8n (workflow orchestration)","Power Automate","Outlook (report dist.)","Asana API"],
        "Visualization": ["Excel Dashboards","Streamlit (this demo)","Plotly","Conditional Formatting"],
        "Process Tools": ["Asana (task management)","Slack (alerts)","GitHub (version control)","Notion (docs)"],
    }
    col1, col2 = st.columns(2)
    for i, (category, tools) in enumerate(stack.items()):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"**{category}**")
            for tool in tools:
                st.markdown(f"- {tool}")
            st.markdown("")

    st.markdown("#### Before vs. After — System Impact")
    comparison = pd.DataFrame({
        "Metric": ["Report Generation Time","Stockout Incidents / Season","Inventory Accuracy","SKUs Analyzed / Hour","Manual Data Entry","Locations with Live KPIs"],
        "Before": ["4 hours","15+","91%","~10 (manual)","High","0"],
        "After":  ["45 minutes","3","99.1%","All 50+ (automated)","Eliminated","8"],
        "Improvement": ["−83%","−80%","+8.1pp","5× faster","Automated","8/8 live"],
    })
    st.dataframe(comparison, use_container_width=True, hide_index=True)
