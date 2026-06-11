import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Delivery Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inline SVG icons (no emoji) ───────────────────────────────────────────────
ICONS = {
    "truck": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
        <circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>""",
    "clock": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>""",
    "star": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>""",
    "users": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "map": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>
        <line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>""",
    "bar_chart": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
        <line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/></svg>""",
    "alert": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/></svg>""",
    "repeat": """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/>
        <polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>""",
}

def icon_html(key, color="#4F8BF9"):
    svg = ICONS[key].replace('stroke="currentColor"', f'stroke="{color}"')
    return f'<span style="vertical-align:middle;margin-right:6px">{svg}</span>'

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background: #0f1117; }
    .block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

    /* Header */
    .dash-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 1.4rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .dash-header h1 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .dash-header p {
        font-size: 0.82rem;
        color: #718096;
        margin: 2px 0 0 0;
    }

    /* KPI cards */
    .kpi-card {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        min-height: 90px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #e2e8f0;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #68d391;
    }
    .kpi-sub.warn { color: #fc8181; }

    /* Section headers */
    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #a0aec0;
        margin: 0.2rem 0 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 6px;
        border-bottom: 1px solid #2d3748;
        padding-bottom: 0.5rem;
    }

    /* Insight box */
    .insight-box {
        background: #1a1f2e;
        border-left: 3px solid #4F8BF9;
        border-radius: 0 8px 8px 0;
        padding: 0.7rem 1rem;
        font-size: 0.8rem;
        color: #a0aec0;
        margin-top: 0.6rem;
    }

    /* Table */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8rem;
    }
    .styled-table th {
        background: #2d3748;
        color: #a0aec0;
        padding: 7px 10px;
        text-align: left;
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .styled-table td {
        padding: 7px 10px;
        color: #e2e8f0;
        border-bottom: 1px solid #2d3748;
    }
    .styled-table tr:hover td { background: #243044; }

    /* Badge */
    .badge-green  { background:#276749; color:#9ae6b4; padding:2px 7px; border-radius:20px; font-size:0.7rem; font-weight:600; }
    .badge-orange { background:#744210; color:#fbd38d; padding:2px 7px; border-radius:20px; font-size:0.7rem; font-weight:600; }
    .badge-red    { background:#742a2a; color:#feb2b2; padding:2px 7px; border-radius:20px; font-size:0.7rem; font-weight:600; }

    div[data-testid="stMetricValue"] { color: #e2e8f0; }
    [data-testid="stHorizontalBlock"] > div { gap: 1rem; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA  (hard-coded from notebook outputs — no CSVs required)
# ══════════════════════════════════════════════════════════════════════════════

# --- Delivery buffer stats (from In[9]) ---
buffer_stats = {
    "count": 96476, "mean": 10.88, "std": 10.18,
    "min": -189, "25%": 6, "50%": 11, "75%": 16, "max": 146,
}

# --- Punctuality distribution (from In[12]) ---
punctuality_data = pd.DataFrame({
    "Punctuality": ["On Time", "Super Late", "Late"],
    "count":       [88649, 4212, 3615],
    "percentage":  [91.89, 4.37, 3.75],
})

# --- Late delivery rate by state (from In[16]) ---
state_late = pd.DataFrame({
    "state": ["RO","AC","AM","AP","PR","MG","SP","MT","DF","RS","GO","SC","RN","PE","PB","MS","RR","ES","PA","TO","RJ","BA","SE","CE","PI","MA","AL"],
    "late_rate": [3.0, 3.7, 4.1, 4.5, 5.0, 5.8, 5.9, 6.7, 6.9, 7.1, 7.9, 9.6, 10.5, 10.5, 10.8, 11.4, 11.9, 12.0, 12.1, 12.5, 13.3, 13.9, 15.3, 15.6, 16.1, 19.6, 23.9],
}).sort_values("late_rate")

# --- Review score by punctuality (from In[21]) ---
punctuality_review = pd.DataFrame({
    "Punctuality": ["On Time", "Late", "Super Late"],
    "mean":        [4.29, 3.46, 1.78],
    "std":         [1.15, 1.56, 1.31],
    "count":       [88168, 3568, 4094],
})

# --- Customer retention by punctuality (from In[26]) ---
retention = pd.DataFrame({
    "Punctuality":     ["On Time", "Late", "Super Late"],
    "new_customers":   [85751, 3512, 4093],
    "returned":        [10829, 378, 404],
    "retention_pct":   [12.6, 10.8, 9.9],
})

# ══════════════════════════════════════════════════════════════════════════════
# MATPLOTLIB THEME  (dark)
# ══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "figure.facecolor":  "#1a1f2e",
    "axes.facecolor":    "#1a1f2e",
    "axes.edgecolor":    "#2d3748",
    "axes.labelcolor":   "#a0aec0",
    "axes.titlecolor":   "#e2e8f0",
    "xtick.color":       "#718096",
    "ytick.color":       "#718096",
    "grid.color":        "#2d3748",
    "text.color":        "#e2e8f0",
    "axes.titlesize":    11,
    "axes.labelsize":    9,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
})
PALETTE = {"On Time": "#68d391", "Late": "#f6ad55", "Super Late": "#fc8181"}

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="dash-header">
  <div>{ICONS['truck'].replace('stroke="currentColor"','stroke="#4F8BF9"').replace('width="22"','width="32"').replace('height="22"','height="32"')}</div>
  <div>
    <h1>Olist Delivery Performance Dashboard</h1>
    <p>Brazilian e-commerce · 96,476 delivered orders · Olist dataset</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, icon_key, label, value, sub, sub_warn=False):
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">{icon_html(icon_key,'#4F8BF9')}{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub {'warn' if sub_warn else ''}">{sub}</div>
    </div>""", unsafe_allow_html=True)

kpi(k1, "truck",    "Delivered Orders",     "96,476",  "of 99,441 total orders")
kpi(k2, "clock",    "On-Time Rate",          "91.89%",  "+10.88 days avg buffer")
kpi(k3, "alert",    "Late + Super Late",      "8.12%",  "7,827 orders delayed", True)
kpi(k4, "star",     "On-Time Avg Score",      "4.29",    "vs 1.78 for Super Late")
kpi(k5, "repeat",   "Retention (On-Time)",   "12.6%",   "vs 9.9% for Super Late")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1  |  Punctuality distribution  +  Review score by category
# ══════════════════════════════════════════════════════════════════════════════
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown(f'<div class="section-title">{icon_html("bar_chart","#4F8BF9")} Delivery Punctuality Distribution</div>',
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    colors = [PALETTE[p] for p in punctuality_data["Punctuality"]]
    bars = ax.barh(punctuality_data["Punctuality"], punctuality_data["count"],
                   color=colors, height=0.5, edgecolor="none")
    for bar, pct in zip(bars, punctuality_data["percentage"]):
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                f"{pct}%", va="center", fontsize=8.5, color="#e2e8f0", fontweight="600")
    ax.set_xlabel("Number of Orders")
    ax.set_title("Punctuality Breakdown")
    ax.xaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.set_xlim(0, punctuality_data["count"].max() * 1.15)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)
    st.markdown('<div class="insight-box">Over 9 in 10 orders arrive on or before the estimated date. Only 4.4% are "Super Late" (more than 5 days overdue).</div>', unsafe_allow_html=True)

with col_b:
    st.markdown(f'<div class="section-title">{icon_html("star","#4F8BF9")} Avg Review Score by Punctuality</div>',
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    cats  = punctuality_review["Punctuality"]
    means = punctuality_review["mean"]
    stds  = punctuality_review["std"]
    colors2 = [PALETTE[p] for p in cats]
    bars2 = ax.bar(cats, means, color=colors2, width=0.45, edgecolor="none")
    ax.errorbar(cats, means, yerr=stds, fmt="none", color="#a0aec0", capsize=5, linewidth=1.2)
    for bar, m in zip(bars2, means):
        ax.text(bar.get_x() + bar.get_width()/2, m + 0.08, f"{m:.2f}",
                ha="center", va="bottom", fontsize=9, fontweight="600", color="#e2e8f0")
    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Average Review Score (1–5)")
    ax.set_title("Satisfaction vs Delivery Speed")
    ax.yaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)
    st.markdown('<div class="insight-box">Super Late orders score 1.78 on average — a 58% drop vs On-Time (4.29). Delivery speed is a primary driver of customer satisfaction.</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2  |  Late rate by state  +  Retention + summary table
# ══════════════════════════════════════════════════════════════════════════════
col_c, col_d = st.columns([1.4, 1])

with col_c:
    st.markdown(f'<div class="section-title">{icon_html("map","#4F8BF9")} Late Delivery Rate by State (Best to Worst)</div>',
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6.5, 7))
    bar_colors = ["#68d391" if r < 7 else "#f6ad55" if r < 15 else "#fc8181"
                  for r in state_late["late_rate"]]
    ax.barh(state_late["state"], state_late["late_rate"],
            color=bar_colors, height=0.65, edgecolor="none")
    for i, (s, r) in enumerate(zip(state_late["state"], state_late["late_rate"])):
        ax.text(r + 0.2, i, f"{r:.1f}%", va="center", fontsize=7.5, color="#e2e8f0")
    ax.set_xlabel("Late Delivery Rate (%)")
    ax.set_title("All 27 States Ranked")
    ax.xaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.set_xlim(0, state_late["late_rate"].max() * 1.12)
    legend_patches = [
        mpatches.Patch(color="#68d391", label="< 7% (Good)"),
        mpatches.Patch(color="#f6ad55", label="7–15% (Moderate)"),
        mpatches.Patch(color="#fc8181", label="> 15% (Poor)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", framealpha=0.2,
              fontsize=7.5, labelcolor="#e2e8f0")
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)
    st.markdown('<div class="insight-box">RO, AC, and AM are top performers (under 4%). AL, MA, and PI are critical — all above 15% late rate — suggesting logistics bottlenecks in the Northeast region.</div>', unsafe_allow_html=True)

with col_d:
    st.markdown(f'<div class="section-title">{icon_html("repeat","#4F8BF9")} Customer Retention by First Delivery</div>',
                unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5, 3.4))
    ret_colors = [PALETTE[p] for p in retention["Punctuality"]]
    bars3 = ax.bar(retention["Punctuality"], retention["retention_pct"],
                   color=ret_colors, width=0.45, edgecolor="none")
    for bar, pct in zip(bars3, retention["retention_pct"]):
        ax.text(bar.get_x() + bar.get_width()/2, pct + 0.2, f"{pct}%",
                ha="center", va="bottom", fontsize=9.5, fontweight="700", color="#e2e8f0")
    ax.set_ylim(0, 16)
    ax.set_ylabel("Retention Rate (%)")
    ax.set_title("Return Purchase Rate")
    ax.yaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)
    st.markdown('<div class="insight-box">On-Time first delivery yields 12.6% retention vs 9.9% for Super Late — a meaningful 27% relative gap in repeat purchase behaviour.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{icon_html("users","#4F8BF9")} Retention Detail</div>',
                unsafe_allow_html=True)

    badge = {"On Time": "badge-green", "Late": "badge-orange", "Super Late": "badge-red"}
    rows_html = ""
    for _, r in retention.iterrows():
        rows_html += f"""<tr>
            <td><span class="{badge[r['Punctuality']]}">{r['Punctuality']}</span></td>
            <td>{r['new_customers']:,}</td>
            <td>{int(r['returned']):,}</td>
            <td><b>{r['retention_pct']}%</b></td>
        </tr>"""
    st.markdown(f"""
    <table class="styled-table">
      <thead><tr>
        <th>Category</th><th>New Customers</th><th>Returned</th><th>Rate</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3  |  Delivery buffer stats  +  Missing value overview
# ══════════════════════════════════════════════════════════════════════════════
col_e, col_f = st.columns([1, 1])

with col_e:
    st.markdown(f'<div class="section-title">{icon_html("clock","#4F8BF9")} Delivery Buffer Distribution (Days)</div>',
                unsafe_allow_html=True)

    # Approximate distribution from the describe() stats using IQR + normal approx
    np.random.seed(42)
    # Skewed sample to represent the actual distribution shape described in the notebook
    simulated = np.concatenate([
        np.random.normal(loc=10.88, scale=8, size=88000),
        np.random.uniform(-30, -1, size=4000),
        np.random.uniform(-189, -30, size=200),
        np.random.uniform(50, 146, size=500),
    ])
    simulated = np.clip(simulated, -189, 146)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.hist(simulated, bins=80, color="#4F8BF9", edgecolor="none", alpha=0.85)
    ax.axvline(0,  color="#fc8181", linestyle="--", linewidth=1.5, label="On-time threshold")
    ax.axvline(10.88, color="#68d391", linestyle="--", linewidth=1.5, label=f"Mean (+10.88d)")
    ax.set_xlabel("Delivery Buffer (days, positive = early)")
    ax.set_ylabel("Frequency")
    ax.set_title("Buffer Days Distribution (Approximated from describe())")
    ax.legend(fontsize=8, framealpha=0.2, labelcolor="#e2e8f0")
    ax.yaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right"]].set_visible(False)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)

    # Stats table
    stats_df = pd.DataFrame({
        "Stat":  ["Count", "Mean", "Std Dev", "Min", "25th pct", "Median", "75th pct", "Max"],
        "Value": ["96,476", "+10.88 days", "10.18 days", "-189 days", "+6 days", "+11 days", "+16 days", "+146 days"],
    })
    rows2 = "".join(f"<tr><td>{r['Stat']}</td><td><b>{r['Value']}</b></td></tr>" for _, r in stats_df.iterrows())
    st.markdown(f'<table class="styled-table"><thead><tr><th>Statistic</th><th>Value</th></tr></thead><tbody>{rows2}</tbody></table>',
                unsafe_allow_html=True)

with col_f:
    st.markdown(f'<div class="section-title">{icon_html("alert","#4F8BF9")} Data Quality — Missing Values</div>',
                unsafe_allow_html=True)

    missing = pd.DataFrame({
        "Column": [
            "order_approved_at", "order_delivered_carrier_date",
            "order_delivered_customer_date", "review_id",
            "review_score", "review_creation_date",
            "review_answer_timestamp", "review_comment_title",
            "review_comment_message",
        ],
        "Missing": [160, 1783, 2965, 768, 768, 768, 768, 87891, 58666],
        "Pct":     [0.16, 1.79, 2.98, 0.77, 0.77, 0.77, 0.77, 88.39, 59.00],
    }).sort_values("Pct", ascending=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    bar_colors_m = ["#fc8181" if p > 50 else "#f6ad55" if p > 5 else "#68d391"
                    for p in missing["Pct"]]
    ax.barh(missing["Column"], missing["Pct"], color=bar_colors_m, height=0.55, edgecolor="none")
    for i, (col_name, pct) in enumerate(zip(missing["Column"], missing["Pct"])):
        ax.text(pct + 0.4, i, f"{pct}%", va="center", fontsize=7.5, color="#e2e8f0")
    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Rate per Column (Full Dataset, n=99,441)")
    ax.xaxis.grid(True, linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.set_xlim(0, 100)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)

    st.markdown('<div class="insight-box"><b>88.4%</b> of review comment titles are missing — this is expected, as most customers don\'t write a title. Core delivery timestamps (approved_at, carrier_date) are well-populated (&lt;2% missing). The analysis filtered to 96,476 rows with a confirmed delivery date before computing all metrics.</div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:2rem; border-top:1px solid #2d3748; padding-top:1rem;
     font-size:0.72rem; color:#4a5568; text-align:center;">
  Olist Brazilian E-Commerce Dataset &nbsp;|&nbsp;
  Analysis based on 99,441 orders across 27 Brazilian states &nbsp;|&nbsp;
  Punctuality thresholds: On Time ≥ 0d buffer · Late –5 to 0d · Super Late &lt; –5d
</div>
""", unsafe_allow_html=True)
