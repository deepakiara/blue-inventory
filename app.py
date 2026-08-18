import pandas as pd
import plotly.express as px
import streamlit as st

# Configure the page
st.set_page_config(page_title="Inventory Dashboard", layout="wide")

# Load and cache data
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load the data
try:
    df = load_data('data.csv')
except FileNotFoundError:
    st.error("Error: 'data.csv' not found. Please make sure 'data.csv' is in the same directory as 'app.py'.")
    st.stop()

# Ensure required columns exist
required_columns = {'Name', 'Category'}
if not required_columns.issubset(df.columns):
    st.error(f"Error: The CSV file must contain the following columns: {', '.join(required_columns)}")
    st.stop()

# Page Title
st.title('📦 Inventory Performance Dashboard')
st.markdown("Interactive analysis of inventory status, usage, adjustments, and ending stock.")

# Dynamic Sidebar Filters
st.sidebar.header("🔍 Filters")

# Search by Name
search_query = st.sidebar.text_input("Search Item by Name:", "").strip()

# Filter by Category
categories = sorted(df['Category'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    'Filter by Category:', options=categories, default=[]
)

# Apply filters to dataframe
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False, na=False)]

if selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

# Key Inventory Metrics Row
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_items = len(filtered_df)
total_beginning = filtered_df['Beginning'].sum() if 'Beginning' in filtered_df.columns else 0.0
total_usage = filtered_df['Usage'].sum() if 'Usage' in filtered_df.columns else 0.0
total_ending = filtered_df['Ending'].sum() if 'Ending' in filtered_df.columns else 0.0

col1.metric("Total Items", f"{total_items:,}")
col2.metric("Total Beginning Stock", f"{total_beginning:,.2f}")
col3.metric("Total Usage", f"{total_usage:,.2f}")
col4.metric("Total Ending Stock", f"{total_ending:,.2f}")

# Chart Sections
st.subheader("Inventory Metrics Visualization")

# Let the user choose which numerical column to plot
numeric_cols = [c for c in ['Beginning', 'Production', 'Purchase Order', 'Usage', 'Transfer', 'Adjustment', 'Ending'] if c in filtered_df.columns]

if numeric_cols:
    selected_metric = st.selectbox("Select metric to visualize on charts:", numeric_cols, index=numeric_cols.index('Ending') if 'Ending' in numeric_cols else 0)
    
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        # Bar Chart of Top Items by selected metric
        # Limit to top 25 items for readability if there are many
        top_n = min(25, len(filtered_df))
        df_sorted = filtered_df.sort_values(by=selected_metric, ascending=False).head(top_n)
        fig_bar = px.bar(
            df_sorted,
            x='Name',
            y=selected_metric,
            color='Category',
            title=f"Top {top_n} Items by {selected_metric}",
            labels={selected_metric: f"{selected_metric} (Units vary)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with chart_col2:
        # Pie Chart of selected metric breakdown by Category
        category_sum = filtered_df.groupby('Category')[selected_metric].sum().reset_index()
        fig_pie = px.pie(
            category_sum,
            values=selected_metric,
            names='Category',
            title=f"Category Distribution ({selected_metric})",
            hole=0.4,
            template="plotly_dark"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("No numeric columns available to visualize.")

# Raw Data Table Section
st.subheader("📋 Filtered Inventory Data")
st.dataframe(filtered_df, use_container_width=True)
