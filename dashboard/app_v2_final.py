# ===============================
# 📊 Executive Customer Experience Dashboard
# ===============================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# -------------------------------
# ⚙️ Page Configuration
# -------------------------------
st.set_page_config(page_title="Customer Experience Executive Dashboard", layout="wide")

# -------------------------------
# 🗄️ Load Tables from Database
# -------------------------------
@st.cache_data
def load_table(table_name):
    conn = sqlite3.connect("./../sql/retail_customer_experience.db")
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df

# Load datasets
df_cleaned = load_table("customer_360_cleaned")
df_enriched = load_table("customer_360_enriched")
df_predicted = load_table("customer_360_predicted")
df_sentiment = load_table("customer_sentiment")
df_campaigns = load_table("campaigns")

# -------------------------------
# 🎛 Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")
city_options = ["All"] + sorted([str(x) for x in df_cleaned["city"].dropna().unique()])
gender_options = ["All"] + sorted([str(x) for x in df_cleaned["gender"].dropna().unique()])

city = st.sidebar.selectbox("Select City", city_options)
gender = st.sidebar.selectbox("Select Gender", gender_options)

filtered_df = df_enriched.copy()
if city != "All":
    filtered_df = filtered_df[filtered_df["city"] == city]
if gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == gender]

# -------------------------------
# 🧭 Tabs for Each Business Area
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "👥 Customers & Segments",
    "💬 Support & Satisfaction",
    "📈 Churn Prediction",
    "💭 Sentiment Insights",
    "📣 Marketing Campaigns"
])

# =====================================================
# 🏠 OVERVIEW TAB
# =====================================================
with tab1:
    st.title("🏠 Executive Overview")
    st.write("A unified view of customer experience, churn, and sentiment metrics.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${filtered_df['monetary'].sum():,.0f}")
    col2.metric("Active Customers", f"{(filtered_df['has_transaction']==1).sum():,}")
    col3.metric("Avg Satisfaction", f"{filtered_df['avg_support_score'].mean():.2f}")
    churn_rate = (df_predicted['churn_flag']==1).mean()*100
    col4.metric("Churn Rate", f"{churn_rate:.1f}%")

    fig = px.histogram(filtered_df, x='monetary', nbins=30,
                       title="Distribution of Customer Monetary Value")
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 👥 CUSTOMERS & SEGMENTS TAB
# =====================================================
with tab2:
    st.header("👥 Customer Segmentation & Value")
    st.write("Clusters of customers based on spending, frequency, and engagement patterns.")

    seg_summary = df_predicted.groupby('segment')[['monetary','frequency','recency_days']].mean().reset_index()
    fig_seg = px.bar(seg_summary, x='segment', y='monetary', color='segment',
                     title="Average Spend by Customer Segment")
    st.plotly_chart(fig_seg, use_container_width=True)

    # PCA visualization
    fig_pca = px.scatter(df_predicted, x='pca1', y='pca2', color='segment',
                         title="Customer Segments (PCA Projection)")
    st.plotly_chart(fig_pca, use_container_width=True)

# =====================================================
# 💬 SUPPORT & SATISFACTION TAB
# =====================================================
with tab3:
    st.header("💬 Support Performance & Satisfaction")
    st.write("Analyze how resolution times and satisfaction impact customer retention.")

    fig_sup = px.scatter(filtered_df, x='avg_resolution_time', y='avg_support_score',
                         color='total_tickets', title="Resolution Time vs. Satisfaction")
    st.plotly_chart(fig_sup, use_container_width=True)

    sup_corr = filtered_df[['avg_resolution_time','avg_support_score','total_tickets']].corr()
    st.write("**Correlation Matrix:**")
    st.dataframe(sup_corr.style.background_gradient(cmap='Blues'))

    st.subheader("Top Customers by Support Satisfaction")
    st.dataframe(filtered_df[['customer_id','total_tickets','avg_support_score']]
                 .sort_values('avg_support_score', ascending=False)
                 .head(10))

# =====================================================
# 📈 CHURN PREDICTION TAB
# =====================================================
with tab4:
    st.header("📈 Churn Prediction Insights")
    st.write("Identify high-risk customers using predictive modeling.")

    fig_churn = px.histogram(df_predicted, x='recency_days', color='churn_flag',
                             title="Churn Distribution by Recency (Days)")
    st.plotly_chart(fig_churn, use_container_width=True)

    st.metric("Predicted Churn Rate", f"{(df_predicted['churn_flag']==1).mean()*100:.2f}%")

    # Optional SHAP images if available
    st.image("plots/shap_summary_churn.png", caption="SHAP: Top Churn Drivers", use_container_width=True)

# =====================================================
# 💭 SENTIMENT TAB
# =====================================================
with tab5:
    st.header("💭 Customer Sentiment & Feedback")
    st.write("Analyze customer tone and feedback from reviews and support tickets.")

    fig_sent = px.histogram(df_enriched, x='sentiment_score', color='sentiment_label',
                            nbins=30, title="Sentiment Score Distribution")
    st.plotly_chart(fig_sent, use_container_width=True)

    st.metric("Avg Sentiment Score", f"{df_enriched['sentiment_score'].mean():.2f}")
    st.metric("Positive Feedback %", f"{(df_enriched['sentiment_label']=='positive').mean()*100:.1f}%")

    st.image("plots/wordcloud_positive.png", caption="Positive Feedback Word Cloud", use_container_width=True)
    st.image("plots/wordcloud_negative.png", caption="Negative Feedback Word Cloud", use_container_width=True)

# =====================================================
# 📣 CAMPAIGNS TAB
# =====================================================
with tab6:
    st.header("📣 Marketing Campaign Performance")
    st.write("Evaluate campaign efficiency and ROI across different channels and segments.")

    df_campaigns['CTR'] = df_campaigns['clicks'] / df_campaigns['impressions']
    df_campaigns['CPC'] = df_campaigns['budget'] / df_campaigns['clicks']

    fig_roi = px.bar(df_campaigns, x='campaign_type', y='roi', color='campaign_type',
                     title="ROI by Campaign Type")
    st.plotly_chart(fig_roi, use_container_width=True)

    fig_ctr = px.scatter(df_campaigns, x='CTR', y='conversion_rate', size='roi',
                         color='campaign_type', title="CTR vs Conversion Rate by Campaign")
    st.plotly_chart(fig_ctr, use_container_width=True)

# =====================================================
# ✅ END
# =====================================================
st.success("Dashboard loaded successfully — powered by Customer 360 Database 🚀")
