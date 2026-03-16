# 📦 AI Inventory Intelligence System

An AI-powered retail inventory management system built during my role as Product Management Supervisor at Canada's Wonderland. Automated weekly reporting with Microsoft Copilot, built a GPT-4 SKU analysis agent for reorder decisions, and connected fragmented data across 8+ locations through a Python pipeline — cutting report time 83% and reducing stockout incidents by 80%.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Plotly](https://img.shields.io/badge/Plotly-5.20-purple)
![GPT-4](https://img.shields.io/badge/OpenAI-GPT--4-green)
![Copilot](https://img.shields.io/badge/Microsoft-Copilot-blue)

---

## 🎯 The Problem

At Canada's Wonderland, merchandise operations spanned 8+ retail locations with no unified inventory view. Weekly operational reports required 4+ hours of manual data pulling from DataWorks, Excel files, and POS systems. Stockout decisions were made reactively — by the time an issue was visible, the damage was done.

---

## 💡 The Solution

I designed and deployed a two-agent AI system:

**Agent 1 — Microsoft Copilot (Reporting)**
- Connected to DataWorks and multi-location Excel files
- Automated KPI calculation across 15+ metrics
- Generated formatted weekly report in 45 minutes vs. 4 hours
- Distributed via Outlook automation — zero manual steps

**Agent 2 — GPT-4 SKU Analysis**
- Ingested Python-processed inventory data per SKU
- Scored each SKU: days remaining, velocity, margin, reorder urgency
- Generated natural-language action recommendations
- Synced recommendations to Asana as actionable tasks
- Triggered Slack alerts for critical threshold breaches

---

## 📊 Results

| Metric | Before | After | Change |
|---|---|---|---|
| Report Generation Time | 4 hours | 45 min | **−83%** |
| Stockout Incidents / Season | 15+ | 3 | **−80%** |
| Inventory Accuracy | 91% | 99.1% | **+8.1pp** |
| SKUs Analyzed / Hour | ~10 (manual) | All 50+ | **Automated** |
| Locations with Live KPIs | 0 | 8 | **8/8** |
| Annual Labour Savings | — | $5,000+ | **Process efficiency** |

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| Python 3.11 + pandas | Data pipeline — merge, clean, normalize across all sources |
| OpenAI GPT-4 | SKU analysis agent — scoring, flagging, action recommendations |
| Microsoft Copilot | Reporting agent — automated KPI report generation |
| DataWorks | Primary inventory data source (8+ locations) |
| Excel (Office 365) | Dashboard layer — 15+ KPIs with conditional formatting |
| n8n | Workflow orchestration — connects all agents and outputs |
| Asana API | Task creation from GPT-4 reorder recommendations |
| Slack | Threshold breach alerts |
| Streamlit + Plotly | This interactive demo dashboard |

---

## 🖥️ Dashboard Views

| View | What It Shows |
|---|---|
| **Operations Overview** | KPI cards, weekly sales by location, stockout trend, revenue by location |
| **AI SKU Agent** | Per-SKU gauge charts, behavioral signals, GPT-4 action recommendations |
| **KPI Dashboard** | 15+ metrics — turnover, accuracy, revenue, SKU status distribution |
| **Reporting Automation** | Before/after report time, Copilot workflow steps, time saved charts |
| **Transaction Audit** | 10,000+ transactions, accuracy improvement, discrepancy analysis |
| **System Architecture** | Full pipeline diagram, tech stack, before/after comparison table |

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/ai-inventory-intelligence.git
cd ai-inventory-intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

Runs at `http://localhost:8501`

---

## 📁 Project Structure

```
ai-inventory-intelligence/
├── app.py               # Streamlit dashboard (all 6 views)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore
```

> **Note:** Dashboard runs on synthetic data modeled after real Wonderland operations. No proprietary data included.

---

## 🔄 How the Pipeline Works

```
POS Systems (8 locations) + DataWorks + Excel
               │
               ▼
    Python Pipeline (pandas)
    Merge → Clean → Normalize → KPIs
               │
       ┌───────┴────────┐
       ▼                ▼
  GPT-4 SKU Agent   Copilot Reporting
  Score + Recommend  Auto-format + Send
       │                ▼
  Asana Tasks     Excel KPI Dashboard
  Slack Alerts
```

---

## 📌 Connection to Professional Work

- **Canada's Wonderland (Feb 2025–present):** Product Management Supervisor managing merchandise across 8+ locations. This system was built and deployed in-role.
- **10,000+ transactions audited** to identify shrink, reconciliation errors, and discrepancies.
- **15+ KPIs tracked** across all locations weekly — sell-through, turnover, stockout rate, margin, availability.

---

## 📬 Let's Connect

- [LinkedIn](https://linkedin.com/in/mahindudhiya)
- [GitHub](https://github.com/yourusername)
