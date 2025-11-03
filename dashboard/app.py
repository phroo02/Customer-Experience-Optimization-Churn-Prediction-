# app.py
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Customer Experience Dashboard", layout="wide")

# --- Load data ---
@st.cache_data
def load_data():
    conn = sqlite3.connect("./../sql/retail_customer_experience.db")
    df = pd.read_sql_query("SELECT * FROM customer_360_cleaned;", conn)
    return df

customer_df = load_data()
st.sidebar.title("Filters")

# Sidebar filters
# Clean up city and gender values before sorting
city_options = ["All"] + sorted([str(x) for x in customer_df["city"].dropna().unique()])
gender_options = ["All"] + sorted([str(x) for x in customer_df["gender"].dropna().unique()])

city = st.sidebar.selectbox("Select City", city_options)
gender = st.sidebar.selectbox("Select Gender", gender_options)


# Filter logic
filtered_df = customer_df.copy()
if city != "All":
    filtered_df = filtered_df[filtered_df["city"] == city]
if gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender]

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Overview", "🧍 Customers", "💬 Support", "📈 Campaigns"])

with tab1:
    st.header("Company Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${filtered_df['monetary'].sum():,.0f}")
    col2.metric("Avg Satisfaction", f"{filtered_df['avg_support_score'].mean():.2f}")
    churn_rate = (filtered_df['has_transaction']==0).mean()*100
    col3.metric("Churn Rate (Inactive)", f"{churn_rate:.1f}%")

    fig_rev = px.histogram(filtered_df, x='monetary', nbins=30, title='Distribution of Customer Spend')
    st.plotly_chart(fig_rev, use_container_width=True)


with tab2:
    st.header("Customer Insights")

    fig_city = px.bar(filtered_df.groupby('city')['monetary'].sum().reset_index().sort_values('monetary', ascending=False),
                      x='city', y='monetary', title='Total Spend by City')
    st.plotly_chart(fig_city, use_container_width=True)

    fig_gender = px.bar(filtered_df.groupby('gender')['monetary'].mean().reset_index(),
                        x='gender', y='monetary', title='Average Spend by Gender')
    st.plotly_chart(fig_gender, use_container_width=True)


with tab3:
    st.header("Support & Satisfaction")

    fig_support = px.scatter(filtered_df, x='avg_resolution_time', y='avg_support_score',
                             color='total_tickets', title='Resolution Time vs Satisfaction')
    st.plotly_chart(fig_support, use_container_width=True)

    st.subheader("Support Summary")
    st.dataframe(filtered_df[['customer_id', 'total_tickets', 'avg_support_score']].sort_values('avg_support_score', ascending=False).head(10))


with tab4:
    st.header("Marketing Campaigns")
    conn = sqlite3.connect("./../sql/retail_customer_experience.db")
    campaigns = pd.read_sql_query("SELECT * FROM campaigns;", conn)
    fig_roi = px.bar(campaigns, x='campaign_type', y='roi', title='Campaign ROI by Type')
    st.plotly_chart(fig_roi, use_container_width=True)
