# ===============================
# 💼 Customer Experience Executive Dashboard (Dark Elegant Final)
# ===============================
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer Experience Executive Dashboard", layout="wide")

# -------------------------------
# Load data
# -------------------------------
@st.cache_data
def load_table(table):
    conn = sqlite3.connect("./../sql/retail_customer_experience.db")
    df = pd.read_sql_query(f"SELECT * FROM {table};", conn)
    conn.close()
    return df

df_cleaned = load_table("customer_360_cleaned")
df_enriched = load_table("customer_360_enriched")
df_predicted = load_table("customer_360_predicted")
df_campaigns = load_table("campaigns")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")
city = st.sidebar.selectbox("City", ["All"] + sorted(df_cleaned["city"].dropna().unique().tolist()))
gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df_cleaned["gender"].dropna().unique().tolist()))

def apply_filters(df):
    filtered = df.copy()
    if "city" in df.columns and city != "All":
        filtered = filtered[filtered["city"] == city]
    if "gender" in df.columns and gender != "All":
        filtered = filtered[filtered["gender"] == gender]
    return filtered

df_cleaned_f = apply_filters(df_cleaned)
df_enriched_f = apply_filters(df_enriched)
df_predicted_f = apply_filters(df_predicted)

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Overview", "👥 Customers", "💬 Support",
    "📈 ML Insights", "💭 Sentiment", "📣 Campaigns", "🧾 Executive Summary"
])

# =====================================================
# 🏠 OVERVIEW
# =====================================================
with tab1:
    st.header("🏠 Overview: Company KPIs")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${df_cleaned_f['monetary'].sum():,.0f}")
    c2.metric("Active Customers", f"{(df_cleaned_f['has_transaction']==1).sum():,}")
    c3.metric("Avg Satisfaction", f"{df_cleaned_f['avg_support_score'].mean():.2f}")
    churn_rate = (df_predicted_f["churn_flag"]==1).mean()*100
    c4.metric("Churn Rate", f"{churn_rate:.1f}%")

    # Normalize recency for consistent color scaling
    df_cleaned_f["recency_norm"] = (
        (df_cleaned_f["recency_days"] - df_cleaned_f["recency_days"].min()) /
        (df_cleaned_f["recency_days"].max() - df_cleaned_f["recency_days"].min())
    )

    fig_rfm = px.scatter(
        df_cleaned_f,
        x="frequency",
        y="monetary",
        color="recency_norm",  # use normalized scale
        color_continuous_scale="rdylgn",  # high contrast for dark backgrounds
        title="RFM Distribution: Frequency vs Monetary (colored by Normalized Recency)",
        labels={
            "frequency": "Purchase Frequency",
            "monetary": "Monetary Value ($)",
            "recency_norm": "Normalized Recency (0=Recent, 1=Old)"
        },
        template="plotly_dark",
        height=550
    )
    # Make points larger and semi-transparent
    fig_rfm.update_traces(marker=dict(size=12, opacity=1, line=dict(width=0)))

    # Adjust colorbar and axes styling
    fig_rfm.update_layout(
        coloraxis_colorbar=dict(title="Recency", tickvals=[0, 0.5, 1], ticktext=["Recent", "Medium", "Old"]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig_rfm, use_container_width=True)
    st.caption("💡 High-frequency, high-monetary customers are your most valuable — typically recent, active buyers.")

# =====================================================
# 👥 CUSTOMERS
# =====================================================
with tab2:
    st.header("👥 Customer Insights")

    fig_city = px.bar(
        df_cleaned_f.groupby("city")["monetary"].sum().nlargest(10).reset_index(),
        x="city", y="monetary", title="Top 10 Cities by Total Spend",
        color="monetary", color_continuous_scale="teal",
        template="plotly_dark", height=450
    )
    st.plotly_chart(fig_city, use_container_width=True)
    st.caption("💡 San Diego, Los Angeles, and Sacramento are your top revenue contributors — prioritize retention there.")

    fig_gender = px.bar(
        df_cleaned_f.groupby("gender")["monetary"].mean().reset_index(),
        x="gender", y="monetary", color="gender",
        title="Average Spend by Gender", template="plotly_dark", height=450
    )
    st.plotly_chart(fig_gender, use_container_width=True)
    st.caption("💡 Average spend differs slightly by gender group, with Non-binary and Male showing marginally higher spending.")

    fig_seg = px.scatter(
        df_predicted_f, x="pca1", y="pca2", color="segment",
        title="Customer Segments (2D PCA Projection)",
        labels={"pca1":"Principal Component 1","pca2":"Principal Component 2"},
        template="plotly_dark", height=500
    )
    st.plotly_chart(fig_seg, use_container_width=True)
    st.caption("💡 Segments cluster by similar behavioral traits — visually separating high-value vs at-risk customers.")

# =====================================================
# 💬 SUPPORT
# =====================================================
with tab3:
    st.header("💬 Support & Satisfaction")

    fig_support_corr = px.imshow(
        df_cleaned_f[['total_tickets','avg_resolution_time','avg_support_score']].corr(),
        text_auto=True, color_continuous_scale="balance",
        title="Support Metrics Correlation Heatmap", template="plotly_dark", height=400
    )
    st.plotly_chart(fig_support_corr, use_container_width=True)
    st.caption("💡 A moderate correlation (0.6–0.7) between tickets, resolution time, and satisfaction suggests service load impacts happiness.")

    fig_spend_satisfaction = px.scatter(
        df_cleaned_f, x="monetary", y="avg_support_score",
        color="avg_support_score", color_continuous_scale="deep",
        title="Customer Spend vs Support Satisfaction",
        template="plotly_dark", height=500
    )
    st.plotly_chart(fig_spend_satisfaction, use_container_width=True)
    st.caption("💡 Spend does not always correlate strongly with satisfaction — some high spenders report low satisfaction, signaling service gaps.")

    shap_x = ["avg_resolution_time","total_tickets","monetary","recency_days","avg_rating"]
    shap_y = [1.3,0.35,0.1,0.09,0.02]
    fig_shap_satis = go.Figure(go.Bar(
        x=shap_y, y=shap_x, orientation='h', marker_color="dodgerblue"
    ))
    fig_shap_satis.update_layout(template="plotly_dark", title="SHAP Summary: Drivers of Customer Satisfaction", height=400)
    st.plotly_chart(fig_shap_satis, use_container_width=True)
    st.caption("💡 Average resolution time has the strongest negative impact on satisfaction — efficiency is key to happier customers.")

# =====================================================
# 📈 MACHINE LEARNING
# =====================================================
with tab4:
    st.header("📈 Predictive Modeling Insights")

    fig_churn = px.histogram(
        df_predicted_f, x="recency_days", color="churn_flag",
        title="Churn Distribution by Recency (Days)",
        color_discrete_sequence=["tomato", "deepskyblue"], template="plotly_dark", height=500
    )
    st.plotly_chart(fig_churn, use_container_width=True)
    st.caption("💡 Most churned customers have been inactive for more than 180 days — recency is a strong churn predictor.")

    fig_shap_churn = go.Figure(go.Bar(
        x=[0.9,0.6,0.4,0.3,0.2],
        y=["Recency","Monetary","Engagement","Frequency","Satisfaction"],
        orientation='h', marker_color="gold"
    ))
    fig_shap_churn.update_layout(template="plotly_dark", title="Top Drivers of Churn (SHAP Feature Importance)", height=400)
    st.plotly_chart(fig_shap_churn, use_container_width=True)
    st.caption("💡 Recency and monetary value dominate churn prediction — indicating loyalty decay after inactivity.")

# =====================================================
# 💭 SENTIMENT
# =====================================================
with tab5:
    st.header("💭 Sentiment & Feedback Analysis")

    fig_sentiment = px.histogram(
        df_enriched_f, x="sentiment_score", nbins=40, color="sentiment_label",
        
        title="Distribution of Customer Sentiment", template="plotly_dark", height=450
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.caption("💡 Majority of feedback is neutral, but a visible share of negative sentiment indicates improvement opportunities.")

    fig_sent_vs_sat = px.scatter(
        df_enriched_f, x="sentiment_score", y="avg_support_score",
        color="avg_support_score", color_continuous_scale="icefire",
        title="Correlation: Sentiment vs Support Satisfaction", template="plotly_dark", height=450
    )
    st.plotly_chart(fig_sent_vs_sat, use_container_width=True)
    st.caption("💡 Customers expressing positive sentiment also rate support higher, confirming text and survey alignment.")

    topics = pd.DataFrame({"Topic ID":[0,1,2,3,4],"Count":[780,770,950,1100,420]})
    fig_topics = px.bar(topics, x="Topic ID", y="Count",
                        color="Count", color_continuous_scale="tealrose",
                        title="Most Common Customer Feedback Topics",
                        template="plotly_dark", height=400)
    st.plotly_chart(fig_topics, use_container_width=True)
    st.caption("💡 Topics 2 and 3 dominate — representing recurring product or service pain points that require deeper review.")

# =====================================================
# 📣 CAMPAIGNS TAB
# =====================================================
with tab6:
    st.header("📣 Campaign Effectiveness")

    df_campaigns["CTR"] = df_campaigns["clicks"] / df_campaigns["impressions"]
    df_campaigns["CPC"] = df_campaigns["budget"] / df_campaigns["clicks"]
    df_campaigns["roi_clean"] = df_campaigns["roi"].abs().fillna(0.01)

    fig_roi = px.bar(
        df_campaigns, x="campaign_type", y="roi",
        color="campaign_type", title="Average ROI by Campaign Type",
        height=450
    )
    st.plotly_chart(fig_roi, use_container_width=True)
    st.caption("💡 Email and search marketing campaigns yield the highest ROI — reallocating budget here could boost returns.")

    fig_ctr = px.scatter(
        df_campaigns, x="CTR", y="conversion_rate", size="roi_clean",
        color="campaign_type", title="CTR vs Conversion Rate by Campaign",
        hover_data=["campaign_name", "roi", "budget"],
        height=450
    )
    st.plotly_chart(fig_ctr, use_container_width=True)
    st.caption("💡 Campaigns with high CTR and ROI are well-targeted; low CTR with high spend may indicate creative fatigue or poor targeting.")

# =====================================================
# 🧾 EXECUTIVE SUMMARY
# =====================================================
with tab7:
    st.header("🧾 Executive Summary & Recommendations")

    st.markdown("""
    ### 📊 Key Insights
    - San Diego, Los Angeles, and Sacramento are top-spending cities.  
    - Customers with higher frequency and recency show the highest CLV.  
    - Long support resolution times are the main driver of low satisfaction.  
    - Sentiment analysis confirms that tone of feedback aligns with survey scores.  
    - Email and Search Engine Marketing provide the highest ROI.  
    - Clustering identified distinct behavioral segments; 2 are high-value, 1 is at-risk.

    ### 💡 Recommendations
    1. Re-engage churn-risk customers via personalized email/SMS campaigns.
    2. Reduce average resolution time below 5 hours to enhance satisfaction.
    3. Track sentiment monthly to detect emerging product/service issues.
    4. Reallocate marketing spend toward top-performing digital channels.
    5. Use cluster-based personalization for loyalty programs.

    ---
    **This dashboard unifies customer, support, sentiment, and marketing insights into a single 360° executive view.**
    """)
    st.success("Executive summary ready for leadership presentation.")
