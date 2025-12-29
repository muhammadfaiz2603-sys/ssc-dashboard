import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. SETUP & DATA LOADING
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SSC 2026 Dashboard", layout="wide")

# NOTE: I have embedded your CSV data here so the dashboard works instantly 
# without needing to upload separate files.

# Dataset 1: Regional Comparison
data_regional = {
    'Region': ['Central', 'Northern', 'Southern', 'East Coast', 'Sabah', 'Sarawak'],
    'Pass': [73, 48, 49, 55, 42, 36],
    'Fail': [25, 16, 13, 12, 8, 14],
    'Total Headcount': [98, 64, 62, 67, 50, 50]
}
df_regional = pd.DataFrame(data_regional)

# Dataset 2: Outlet Comparison
data_outlet = {
    'Outlet': ['MT', 'PY', 'EV', 'MF'],
    'Pass': [4, 5, 3, 1],
    'Fail': [2, 3, 2, 4]
}
df_outlet = pd.DataFrame(data_outlet)

# Dataset 3: LOB Comparison (More complex structure)
data_lob = {
    'Result': [
        'iPhone (Pass)', 'iPhone (Fail)', 'Mac (Pass)', 'Mac (Fail)',
        'iPad (Pass)', 'iPad (Fail)', 'Apple Watch (Pass)', 'Apple Watch (Fail)'
    ],
    'Central': [20, 45, 12, 24, 23, 12, 11, 7],
    'Northern': [45, 56, 9, 11, 11, 8, 45, 3],
    'Sarawak': [23, 12, 56, 7, 44, 4, 67, 99],
    'Sabah': [12, 54, 34, 6, 8, 22, 5, 66]
}
df_lob = pd.DataFrame(data_lob)

# -----------------------------------------------------------------------------
# 2. DATA PROCESSING
# -----------------------------------------------------------------------------

# Process LOB Data: Convert from Pivot table to Long format for plotting
df_lob_melted = df_lob.melt(id_vars=['Result'], var_name='Region', value_name='Count')

# Extract Product and Status from "Result" (e.g., "iPhone (Pass)" -> "iPhone", "Pass")
def extract_info(val):
    parts = val.replace(')', '').split(' (')
    return pd.Series([parts[0], parts[1]])

df_lob_melted[['Product', 'Status']] = df_lob_melted['Result'].apply(extract_info)

# -----------------------------------------------------------------------------
# 3. DASHBOARD LAYOUT
# -----------------------------------------------------------------------------
st.title("📊 SSC 2026 Performance Dashboard")
st.markdown("Overview of performance metrics across Regions, Outlets, and Lines of Business (LOB).")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["🌍 Regional Overview", "🏢 Outlet Performance", "📱 LOB Analysis"])

# --- TAB 1: REGIONAL OVERVIEW ---
with tab1:
    st.header("Regional Performance")
    
    # KPIs
    total_hc = df_regional['Total Headcount'].sum()
    total_pass = df_regional['Pass'].sum()
    total_fail = df_regional['Fail'].sum()
    pass_rate = (total_pass / total_hc) * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Headcount", total_hc)
    c2.metric("Total Pass", total_pass)
    c3.metric("Total Fail", total_fail)
    c4.metric("Overall Pass Rate", f"{pass_rate:.1f}%")
    
    # Bar Chart
    df_regional_melt = df_regional.melt(id_vars=['Region', 'Total Headcount'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    
    fig_reg = px.bar(
        df_regional_melt, 
        x='Region', 
        y='Count', 
        color='Status', 
        title="Pass vs Fail by Region",
        barmode='group',
        color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'},
        text_auto=True
    )
    st.plotly_chart(fig_reg, use_container_width=True)

# --- TAB 2: OUTLET PERFORMANCE ---
with tab2:
    st.header("Outlet Performance Metrics")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.dataframe(df_outlet, hide_index=True)
        
    with col_b:
        df_outlet_melt = df_outlet.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
        fig_out = px.bar(
            df_outlet_melt,
            x='Outlet',
            y='Count',
            color='Status',
            title="Outlet Pass/Fail Counts",
            barmode='group',
            color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'}
        )
        st.plotly_chart(fig_out, use_container_width=True)

# --- TAB 3: LOB ANALYSIS ---
with tab3:
    st.header("Line of Business (LOB) Analysis")
    
    # Filter
    selected_region = st.selectbox("Select Region for LOB Analysis:", options=df_lob_melted['Region'].unique())
    
    # Filter Data
    df_filtered = df_lob_melted[df_lob_melted['Region'] == selected_region]
    
    # Stacked Bar Chart
    fig_lob = px.bar(
        df_filtered,
        x='Product',
        y='Count',
        color='Status',
        title=f"Product Performance in {selected_region}",
        text_auto=True,
        color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'}
    )
    
    st.plotly_chart(fig_lob, use_container_width=True)
    
    with st.expander("View Raw LOB Data"):
        st.dataframe(df_filtered)