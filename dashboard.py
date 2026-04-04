"""
E-commerce Business Analytics Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import warnings

from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="E-commerce Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F0F2F6;
}

.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1400px;
}

/* ── Header ── */
.dash-header {
    background: white;
    border-radius: 16px;
    padding: 1.75rem 2.5rem;
    margin-bottom: 1.75rem;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #2563EB;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.dash-header h1 {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.02em;
    color: #0F172A;
}
.dash-header p {
    font-size: 0.875rem;
    margin: 0;
    color: #64748B;
}
.dash-badge {
    display: inline-block;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    margin-top: 0.75rem;
    color: #2563EB;
}

/* ── Section labels ── */
.section-title {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748B;
    border-left: 3px solid #2563EB;
    padding-left: 0.6rem;
    margin: 0 0 1rem 0;
}

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    position: relative;
    overflow: hidden;
    height: 138px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.kpi-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.c-blue::before   { background: linear-gradient(90deg, #1E40AF, #3B82F6); }
.kpi-card.c-amber::before  { background: linear-gradient(90deg, #D97706, #F59E0B); }
.kpi-card.c-green::before  { background: linear-gradient(90deg, #059669, #10B981); }
.kpi-card.c-purple::before { background: linear-gradient(90deg, #6D28D9, #8B5CF6); }

.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94A3B8;
    margin: 0 0 0.45rem 0;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 0.45rem 0;
    letter-spacing: -0.02em;
    line-height: 1;
}
.kpi-trend {
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0;
    color: #64748B;
}
.up   { color: #059669; }
.down { color: #DC2626; }

/* ── Chart wrapper ── */
.chart-wrap {
    background: white;
    border-radius: 14px;
    padding: 1.25rem 1.25rem 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    transition: box-shadow 0.2s ease;
}
.chart-wrap:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.09);
}
.chart-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #334155;
    letter-spacing: 0.02em;
    margin: 0 0 0.75rem 0.25rem;
}

/* ── Bottom experience cards ── */
.exp-card {
    background: white;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
    border: 1px solid #E2E8F0;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.exp-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.09);
    transform: translateY(-2px);
}
.exp-card .kpi-value { font-size: 2.6rem; text-align: center; }

/* ── Stars ── */
.stars-row {
    display: flex;
    justify-content: center;
    gap: 3px;
    margin-top: 0.4rem;
}
.star-on  { color: #F59E0B; font-size: 1.3rem; }
.star-off { color: #CBD5E1; font-size: 1.3rem; }

/* ── Selectbox style ── */
div[data-testid="stSelectbox"] > label {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #64748B !important;
}

/* ── Summary strip ── */
.summary-strip {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.25rem 1.75rem;
    display: flex;
    gap: 0;
    align-items: stretch;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-top: 0.5rem;
}
.summary-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    padding: 0 1.5rem;
    border-right: 1px solid #F1F5F9;
}
.summary-item:first-child { padding-left: 0; }
.summary-item:last-child  { border-right: none; }
.summary-icon {
    font-size: 1.1rem;
    margin-bottom: 0.15rem;
}
.summary-key {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94A3B8;
    margin: 0;
}
.summary-val {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.01em;
}
.summary-sub {
    font-size: 0.72rem;
    color: #94A3B8;
    margin: 0;
}

/* ── Footer ── */
.dash-footer {
    text-align: center;
    font-size: 0.68rem;
    color: #CBD5E1;
    letter-spacing: 0.08em;
    padding: 1.25rem 0 0.25rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

@st.cache_data
def load_dashboard_data():
    try:
        loader, processed_data = load_and_process_data('ecommerce_data/')
        return loader, processed_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


def fmt_currency(v):
    if abs(v) >= 1e6:
        return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:.0f}K"
    return f"${v:.0f}"


def fmt_trend(current, previous, invert=False):
    if previous == 0:
        return '<span style="color:#94A3B8">— N/A</span>'
    pct = ((current - previous) / previous) * 100
    up = pct > 0
    if invert:
        up = not up          # for metrics where lower = better
    arrow = "▲" if pct > 0 else "▼"
    cls = "up" if up else "down"
    return f'<span class="{cls}">{arrow} {abs(pct):.1f}%</span> <span style="color:#94A3B8;font-size:0.7rem">vs prior year</span>'


def stars_html(score):
    filled = round(score)
    html = '<div class="stars-row">'
    for i in range(1, 6):
        html += f'<span class="{"star-on" if i <= filled else "star-off"}">&#9733;</span>'
    html += '</div>'
    return html


# ─── Plot helpers ─────────────────────────────────────────────────────────────

PLOT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="white",
    font=dict(family="Inter, sans-serif", color="#64748B", size=12),
    margin=dict(t=10, b=50, l=60, r=20),
    height=340,
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font=dict(color="#0F172A", size=12, family="Inter"),
    ),
)

AXIS_STYLE = dict(
    showgrid=True,
    gridcolor="#F1F5F9",
    gridwidth=1,
    zeroline=False,
    linecolor="#E2E8F0",
    tickfont=dict(color="#94A3B8", size=11),
    title_font=dict(color="#64748B", size=11),
)


def chart_layout(**overrides):
    d = dict(**PLOT_DEFAULTS)
    d.update(overrides)
    return d


def empty_chart(msg):
    fig = go.Figure()
    fig.add_annotation(text=msg, xref="paper", yref="paper",
                       x=0.5, y=0.5, showarrow=False,
                       font=dict(color="#94A3B8", size=13))
    fig.update_layout(**PLOT_DEFAULTS)
    return fig


# ─── Charts ───────────────────────────────────────────────────────────────────

def revenue_trend_chart(cur, prev, cy, py):
    fig = go.Figure()
    months = cur['purchase_month'].nunique()

    if months > 1:
        cm = cur.groupby('purchase_month')['price'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=cm['purchase_month'], y=cm['price'],
            mode='lines+markers', name=str(cy),
            line=dict(color='#2563EB', width=3),
            marker=dict(size=7, color='#2563EB',
                        line=dict(color='white', width=2)),
            fill='tozeroy', fillcolor='rgba(37,99,235,0.07)',
            hovertemplate='Month %{x}<br>Revenue: %{y:$,.0f}<extra></extra>',
        ))
        if prev is not None and not prev.empty:
            pm = prev.groupby('purchase_month')['price'].sum().reset_index()
            fig.add_trace(go.Scatter(
                x=pm['purchase_month'], y=pm['price'],
                mode='lines+markers', name=str(py),
                line=dict(color='#F59E0B', width=2, dash='dot'),
                marker=dict(size=5, color='#F59E0B',
                            line=dict(color='white', width=2)),
                hovertemplate='Month %{x}<br>Revenue: %{y:$,.0f}<extra></extra>',
            ))
        fig.update_layout(
            **chart_layout(),
            legend=dict(orientation='h', y=1.08, x=0, bgcolor='rgba(0,0,0,0)',
                        font=dict(size=11, color='#64748B')),
            yaxis={**AXIS_STYLE, 'tickformat': '$,.0f'},
            xaxis_title="Month", yaxis_title="Revenue",
        )
    else:
        cr = cur['price'].sum()
        pr = prev['price'].sum() if prev is not None and not prev.empty else 0
        fig.add_trace(go.Bar(
            x=[str(cy), str(py)], y=[cr, pr],
            marker_color=['#2563EB', '#F59E0B'],
            marker_line_width=0,
            text=[fmt_currency(cr), fmt_currency(pr)],
            textposition='outside',
            textfont=dict(color='#0F172A', size=13),
        ))
        fig.update_layout(
            **chart_layout(),
            yaxis={**AXIS_STYLE, 'tickformat': '$,.0f'},
            xaxis_title="Year", yaxis_title="Revenue",
        )
    return fig


def category_chart(sales_data):
    if 'product_category_name' not in sales_data.columns:
        return empty_chart("Product category data not available")

    cat = (sales_data.groupby('product_category_name')['price']
                     .sum().sort_values(ascending=True).tail(10))
    n = len(cat)
    blues = [f"rgba(37,99,235,{0.28 + 0.072 * i:.2f})" for i in range(n)]
    blues[-1] = '#2563EB'

    fig = go.Figure(go.Bar(
        y=cat.index, x=cat.values,
        orientation='h',
        marker=dict(color=blues, line=dict(width=0)),
        text=[fmt_currency(v) for v in cat.values],
        textposition='outside',
        textfont=dict(color='#64748B', size=11),
        hovertemplate='<b>%{y}</b><br>%{x:$,.0f}<extra></extra>',
    ))
    fig.update_layout(
        **chart_layout(margin=dict(t=10, b=50, l=160, r=80)),
        xaxis={**AXIS_STYLE, 'tickformat': '$,.0f'},
        yaxis={**AXIS_STYLE, 'showgrid': False},
        xaxis_title="Revenue",
    )
    return fig


def state_map(sales_data):
    if 'customer_state' not in sales_data.columns:
        return empty_chart("Geographic data not available")

    sr = sales_data.groupby('customer_state')['price'].sum().reset_index()
    sr.columns = ['state', 'revenue']

    fig = go.Figure(go.Choropleth(
        locations=sr['state'], z=sr['revenue'],
        locationmode='USA-states',
        colorscale=[
            [0.0, '#EFF6FF'],
            [0.3, '#BFDBFE'],
            [0.6, '#60A5FA'],
            [1.0, '#1D4ED8'],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Revenue", font=dict(color='#64748B', size=11)),
            tickformat='$,.0f',
            tickfont=dict(color='#94A3B8', size=10),
            bgcolor='rgba(0,0,0,0)',
            outlinewidth=0,
            thickness=14,
        ),
        hovertemplate='<b>%{location}</b><br>%{z:$,.0f}<extra></extra>',
    ))
    fig.update_layout(
        geo=dict(
            scope='usa',
            bgcolor='rgba(0,0,0,0)',
            lakecolor='#EFF6FF',
            landcolor='#F8FAFC',
            showlakes=True,
            subunitcolor='#E2E8F0',
            coastlinecolor='#CBD5E1',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#64748B'),
        margin=dict(t=0, b=0, l=0, r=0),
        height=340,
        hoverlabel=dict(bgcolor='white', bordercolor='#E2E8F0',
                        font=dict(color='#0F172A', size=12, family='Inter')),
    )
    return fig


def satisfaction_chart(sales_data):
    if 'delivery_days' not in sales_data.columns or 'review_score' not in sales_data.columns:
        return empty_chart("Delivery or review data not available")

    def cat_d(d):
        if pd.isna(d):
            return 'Unknown'
        if d <= 3:
            return '1-3 days'
        if d <= 7:
            return '4-7 days'
        return '8+ days'

    tmp = sales_data.copy()
    tmp['dcat'] = tmp['delivery_days'].apply(cat_d)
    agg = (tmp[tmp['dcat'] != 'Unknown']
           .groupby('dcat')['review_score'].mean().reset_index())
    order = ['1-3 days', '4-7 days', '8+ days']
    agg['dcat'] = pd.Categorical(agg['dcat'], order, ordered=True)
    agg = agg.sort_values('dcat')

    color_map = {'1-3 days': '#10B981',
                 '4-7 days': '#F59E0B', '8+ days': '#EF4444'}
    colors = [color_map.get(c, '#2563EB') for c in agg['dcat'].astype(str)]

    fig = go.Figure(go.Bar(
        x=agg['dcat'].astype(str), y=agg['review_score'],
        marker=dict(color=colors, line=dict(width=0), opacity=0.85),
        text=[f"{v:.2f}" for v in agg['review_score']],
        textposition='outside',
        textfont=dict(color='#0F172A', size=12),
        hovertemplate='<b>%{x}</b><br>Avg Score: %{y:.2f} / 5.0<extra></extra>',
    ))
    fig.update_layout(
        **chart_layout(bargap=0.45),
        xaxis={**AXIS_STYLE, 'showgrid': False},
        yaxis={**AXIS_STYLE, 'range': [0, 5.5]},
        xaxis_title="Delivery Window", yaxis_title="Avg Review Score",
    )
    return fig


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    loader, processed_data = load_dashboard_data()
    if loader is None:
        st.error("Failed to load data. Please check your data files.")
        return

    orders_data = processed_data['orders']
    available_years = sorted(
        orders_data['purchase_year'].unique(), reverse=True)
    default_idx = available_years.index(2023) if 2023 in available_years else 0

    # ── Header + Filters ──────────────────────────────────────────────────────
    hdr, fcol1, fcol2 = st.columns([3, 1, 1])

    with hdr:
        st.markdown("""
        <div class="dash-header">
            <h1>E-commerce Analytics</h1>
            <p>Business performance intelligence &mdash; delivered &amp; processed orders</p>
            <span class="dash-badge">LIVE REPORT</span>
        </div>
        """, unsafe_allow_html=True)

    with fcol1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        selected_year = st.selectbox(
            "Fiscal Year", options=available_years,
            index=default_idx, key="year_filter"
        )

    with fcol2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        from datetime import datetime as dt
        month_opts = ['All Months'] + \
            [dt(2000, i, 1).strftime('%B') for i in range(1, 13)]
        sel_month_label = st.selectbox(
            "Period", options=month_opts, index=0, key="month_filter")
        selected_month = None if sel_month_label == 'All Months' else month_opts.index(
            sel_month_label)

    # ── Data ──────────────────────────────────────────────────────────────────
    cur = loader.create_sales_dataset(
        year_filter=selected_year, month_filter=selected_month, status_filter='delivered'
    )
    prev_year = selected_year - 1
    prev = (loader.create_sales_dataset(
        year_filter=prev_year, month_filter=selected_month, status_filter='delivered'
    ) if prev_year in available_years else None)

    # ── KPI Calculations ──────────────────────────────────────────────────────
    total_rev = cur['price'].sum()
    total_orders = cur['order_id'].nunique()
    aov = cur.groupby('order_id')['price'].sum().mean()

    pr_rev = prev['price'].sum() if prev is not None else 0
    pr_orders = prev['order_id'].nunique() if prev is not None else 0
    pr_aov = prev.groupby('order_id')['price'].sum(
    ).mean() if prev is not None else 0

    monthly = cur.groupby('purchase_month')['price'].sum()
    mom_growth = monthly.pct_change().mean() * 100 if len(monthly) > 1 else 0

    # ── KPI Row ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Key Performance Indicators</div>',
                unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card c-blue">
            <p class="kpi-label">Total Revenue</p>
            <p class="kpi-value">{fmt_currency(total_rev)}</p>
            <p class="kpi-trend">{fmt_trend(total_rev, pr_rev)}</p>
        </div>""", unsafe_allow_html=True)

    with k2:
        arr = "▲" if mom_growth > 0 else "▼"
        cls = "up" if mom_growth > 0 else "down"
        st.markdown(f"""
        <div class="kpi-card c-amber">
            <p class="kpi-label">Monthly Growth Rate</p>
            <p class="kpi-value">{mom_growth:.1f}%</p>
            <p class="kpi-trend"><span class="{cls}">{arr} avg mom</span></p>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card c-green">
            <p class="kpi-label">Avg Order Value</p>
            <p class="kpi-value">{fmt_currency(aov)}</p>
            <p class="kpi-trend">{fmt_trend(aov, pr_aov)}</p>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card c-purple">
            <p class="kpi-label">Total Orders</p>
            <p class="kpi-value">{total_orders:,}</p>
            <p class="kpi-trend">{fmt_trend(total_orders, pr_orders)}</p>
        </div>""", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Performance Analytics</div>',
                unsafe_allow_html=True)

    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)

    def render_chart(col, title, fig):
        with col:
            st.markdown(
                f'<div class="chart-wrap"><p class="chart-title">{title}</p>', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    render_chart(r1c1, "Revenue Trend", revenue_trend_chart(
        cur, prev, selected_year, prev_year))
    render_chart(r1c2, "Top 10 Product Categories", category_chart(cur))
    render_chart(r2c1, "Revenue by State", state_map(cur))
    render_chart(r2c2, "Customer Satisfaction vs Delivery Time",
                 satisfaction_chart(cur))

    # ── Customer Experience ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Customer Experience</div>',
                unsafe_allow_html=True)

    e1, e2 = st.columns(2)

    with e1:
        if 'delivery_days' in cur.columns:
            avg_del = cur['delivery_days'].mean()
            pr_del = prev['delivery_days'].mean() if prev is not None else 0
            trend = fmt_trend(avg_del, pr_del, invert=True)
            st.markdown(f"""
            <div class="exp-card">
                <p class="kpi-label">Average Delivery Time</p>
                <p class="kpi-value">{avg_del:.1f} <span style="font-size:1.1rem;font-weight:400;color:#94A3B8">days</span></p>
                <p class="kpi-trend" style="text-align:center;margin-top:0.4rem">{trend}</p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="exp-card"><p class="kpi-label">Average Delivery Time</p><p class="kpi-value">N/A</p></div>', unsafe_allow_html=True)

    with e2:
        if 'review_score' in cur.columns:
            avg_score = cur['review_score'].mean()
            st.markdown(f"""
            <div class="exp-card">
                <p class="kpi-label">Customer Satisfaction</p>
                <p class="kpi-value">{avg_score:.1f} <span style="font-size:1.1rem;font-weight:400;color:#94A3B8">/ 5.0</span></p>
                {stars_html(avg_score)}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="exp-card"><p class="kpi-label">Customer Satisfaction</p><p class="kpi-value">N/A</p></div>', unsafe_allow_html=True)

    # ── Summary strip ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Snapshot</div>',
                unsafe_allow_html=True)

    # Derived values for summary
    top_cat = "N/A"
    if 'product_category_name' in cur.columns:
        top_cat = cur.groupby('product_category_name')['price'].sum().idxmax()
        top_cat = top_cat.replace('_', ' ').title()

    top_state = "N/A"
    if 'customer_state' in cur.columns:
        top_state = cur.groupby('customer_state')['price'].sum().idxmax()

    fast_pct = 0
    if 'delivery_days' in cur.columns:
        fast_pct = (cur['delivery_days'] <= 3).mean() * 100

    five_star_pct = 0
    if 'review_score' in cur.columns:
        five_star_pct = (cur['review_score'] == 5).mean() * 100

    period_label = sel_month_label if sel_month_label != 'All Months' else 'Full Year'
    rev_per_order = total_rev / total_orders if total_orders else 0

    st.markdown(f"""
    <div class="summary-strip">
        <div class="summary-item">
            <p class="summary-key">Period</p>
            <p class="summary-val">{selected_year}</p>
            <p class="summary-sub">{period_label} &middot; delivered orders</p>
        </div>
        <div class="summary-item">
            <p class="summary-key">Top Category</p>
            <p class="summary-val">{top_cat}</p>
            <p class="summary-sub">highest revenue segment</p>
        </div>
        <div class="summary-item">
            <p class="summary-key">Top State</p>
            <p class="summary-val">{top_state}</p>
            <p class="summary-sub">leading geographic market</p>
        </div>
        <div class="summary-item">
            <p class="summary-key">Fast Deliveries</p>
            <p class="summary-val">{fast_pct:.0f}%</p>
            <p class="summary-sub">arrived within 3 days</p>
        </div>
        <div class="summary-item">
            <p class="summary-key">5-Star Reviews</p>
            <p class="summary-val">{five_star_pct:.0f}%</p>
            <p class="summary-sub">of all customer ratings</p>
        </div>
        <div class="summary-item">
            <p class="summary-key">Rev / Order</p>
            <p class="summary-val">{fmt_currency(rev_per_order)}</p>
            <p class="summary-sub">average basket value</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="dash-footer">E-COMMERCE ANALYTICS &nbsp;&middot;&nbsp; DELIVERED ORDERS &nbsp;&middot;&nbsp; {selected_year}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
