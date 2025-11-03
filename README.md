# 🧠 Customer Experience Optimization & Churn Prediction Dashboard

## 📊 Executive Summary

This project builds a complete **Customer Experience Optimization and Churn Prediction System** using real-world multi-source retail data.  
The pipeline integrates customer, transaction, support, campaign, and review data to produce a **360° customer intelligence dashboard** with actionable insights.

---

## 🚀 Project Workflow Overview

| Phase | Description | Output |
|-------|-------------|---------|
| **1️⃣ SQL Layer (Data Integration)** | Multiple CSVs (customers, transactions, support, reviews, campaigns) were imported into a SQLite database and joined into a unified data model. | `customer_360_cleaned` table |
| **2️⃣ Data Cleaning & EDA (Pandas Layer)** | Cleaned missing data, engineered RFM and engagement metrics, analyzed customer spend, demographics, and satisfaction trends. | Exploratory plots (`output1.png` – `output9.png`) |
| **3️⃣ Support Analytics** | Correlated ticket volume, satisfaction, and resolution time to detect service inefficiencies. | Heatmaps & scatter plots |
| **4️⃣ ML Modeling (Churn & Satisfaction)** | Built predictive models for churn and customer satisfaction; used SHAP for explainability. | `output9.png` – `output11.png` |
| **5️⃣ Customer Segmentation (Clustering)** | Performed RFM and PCA-based segmentation using K-Means. Visualized customer groups via PCA and cluster heatmaps. | `output12.png` – `output13.png` |
| **6️⃣ NLP Sentiment Analysis** | Analyzed customer reviews and support notes using VADER & topic modeling (LDA) to detect pain points and satisfaction trends. | `output14.png` – `output21.png` |
| **7️⃣ BI Layer (Streamlit Dashboard)** | Developed an interactive dashboard connecting all insights into a unified executive view with filters and insights. | `app_final_dark.py` |

---

## 🧱 Data Sources

| Dataset | Description |
|----------|-------------|
| `customers.csv` | Demographics, preferences, and registration info |
| `transactions.csv` | Purchase history, product categories, spend data |
| `support_tickets.csv` | Support activity, resolution times, satisfaction scores |
| `campaigns.csv` | Marketing campaign metadata, ROI, and performance metrics |
| `customer_reviews_complete.csv` | Product reviews and ratings |
| `interactions.csv` | Web/app customer engagement logs |

All datasets were imported into **SQLite** and combined via SQL joins into a 360° unified dataset.

---

## 🧩 Techniques and Tools

### ⚙️ Data Engineering
- **SQLite** – Data storage & integration  
- **SQLAlchemy / pandas.read_sql_query()** – Table loading and joins  
- **Data normalization, deduplication, missing value imputation**

### 🔍 Feature Engineering
- **RFM Analysis** – Recency, Frequency, Monetary scoring  
- **Engagement & Satisfaction Index** – Aggregated behavioral and service metrics  
- **Sentiment Score** – Derived from NLP sentiment analysis  
- **Churn Flag** – Defined based on inactivity threshold (>180 days)

### 📊 Exploratory Data Analysis (EDA)
- **Libraries:** `pandas`, `matplotlib`, `plotly.express`  
- **Techniques:** Descriptive stats, outlier detection, correlation heatmaps, and RFM distributions  
- **Key Metrics Visualized:**
  - Spending by City (`output2.png`)
  - Average Spend by Gender (`output3.png`)
  - RFM Distribution (`output1.png`)
  - Customer Spend vs Support Satisfaction (`output4.png`)
  - Support Metrics Heatmap (`output5.png`)
  - Campaign ROI Comparison (`output6.png`)
  - Review Ratings Distribution (`output7.png`)
  - Product Category Ratings (`output8.png`)

---

## 🧠 Machine Learning and Predictive Analytics

### 📉 Churn Prediction
- **Model:** Logistic Regression / Random Forest  
- **Target:** Churn Flag (`churn_flag`)
- **Features:** Recency, Frequency, Monetary, Engagement, Satisfaction
- **Explainability:** SHAP feature importance

**Outputs:**
- SHAP Summary for Churn (`output9.png`)
- SHAP Drivers of Satisfaction (`output10.png`, `output11.png`)

### 🧩 Customer Segmentation
- **Algorithm:** K-Means Clustering  
- **Feature Set:** RFM + Satisfaction + Engagement  
- **Dimensionality Reduction:** PCA (2D projection)

**Outputs:**
- Elbow Method (`output12.png`)
- PCA Projection (`output13.png`)
- Cluster Heatmap (`output14.png`)

---

## 💬 Sentiment Analysis & Topic Modeling

### 🗣️ Sentiment Analysis
- **Tool:** VADER (NLTK)
- **Text Sources:** Reviews + Support Notes
- **Metric:** `sentiment_score` ∈ [-1, 1]

**Output:**
- Sentiment Distribution (`output16.png`)

### 🧵 Topic Modeling
- **Model:** Latent Dirichlet Allocation (LDA)
- **Goal:** Extract dominant customer feedback themes  
- **Key Topics Found:** Delivery issues, performance complaints, battery life, pricing concerns  

**Outputs:**
- Word Cloud (Positive Feedback) – `output14.png`  
- Word Cloud (Negative Feedback) – `output15.png`  
- Feedback Topic Frequency – `output20.png`  
- Sentiment vs Satisfaction Correlation – `output21.png`

---

## 📣 Marketing Campaign Analysis

### Campaign Performance Metrics
- **CTR (Click-Through Rate)** = Clicks / Impressions  
- **CPC (Cost per Click)** = Budget / Clicks  
- **ROI (Return on Investment)** = Revenue / Cost  

**Interactive Insights:**
- Average ROI by Campaign Type  
- CTR vs Conversion Rate Scatter  

**Output Plots:** `output6.png`

---

## 📊 Streamlit Executive Dashboard

### App File
> `dashboard/app_final_dark.py`

### Key Features
- **Dark Elegant Theme** (`plotly_dark`)
- **Dynamic Filters:** City & Gender  
- **Interactive Visuals:** All charts built with Plotly  
- **Tabs:**
  1. **Overview:** Company KPIs & RFM Analysis  
  2. **Customers:** City, Gender, and Segment Insights  
  3. **Support:** Ticket Correlations & SHAP Drivers  
  4. **ML Insights:** Churn and Satisfaction Explainability  
  5. **Sentiment:** NLP Sentiment & Topic Trends  
  6. **Campaigns:** ROI, CTR, and Conversion Efficiency  
  7. **Executive Summary:** Key insights & recommendations

---

## 🧾 Executive Insights Summary

### Key Findings
- **High-value markets:** San Diego, Los Angeles, Sacramento drive most revenue  
- **Customer retention:** Drop-off begins after 180 days inactivity  
- **Service bottlenecks:** Longer resolution time → lower satisfaction  
- **Sentiment correlation:** Positive tone aligns with higher satisfaction ratings  
- **Marketing ROI:** Email and Search Engine campaigns outperform others  
- **Segmentation:** Identified “Champions,” “At-Risk,” and “Disengaged” customer groups

### Strategic Recommendations
1. **Retention Campaigns:** Target customers inactive >180 days  
2. **Support Efficiency:** Automate low-level issues to cut resolution times  
3. **Sentiment Monitoring:** Integrate ongoing feedback NLP pipelines  
4. **Marketing Optimization:** Reallocate spend to Email/Search  
5. **Personalization:** Tailor campaigns per segment to maximize CLV  

---

## 🛠️ Tech Stack

| Layer | Tools & Libraries |
|--------|-------------------|
| **Database** | SQLite, SQLAlchemy |
| **Data Processing** | pandas, numpy |
| **Visualization** | plotly, seaborn, matplotlib |
| **Machine Learning** | scikit-learn, shap |
| **NLP** | nltk (VADER), sklearn (LDA) |
| **Dashboard** | Streamlit |
| **Environment** | Conda + Python 3.11 |

---

## 📂 Project Structure
Customer-Experience-Optimization/
│
├── sql/
│ └── retail_customer_experience.db
│
├── plots/
│ ├── output1.png → RFM Distribution
│ ├── output2.png → Top 10 Cities by Spend
│ ├── output3.png → Average Spend by Gender
│ ├── output4.png → Spend vs Support Satisfaction
│ ├── output5.png → Support Metrics Correlation
│ ├── output6.png → Campaign ROI
│ ├── output7.png → Review Rating Distribution
│ ├── output8.png → Avg Rating by Product Category
│ ├── output9.png → SHAP Summary (Churn)
│ ├── output10.png → SHAP Drivers (Satisfaction)
│ ├── output11.png → SHAP Feature Impact
│ ├── output12.png → Elbow Method for Clusters
│ ├── output13.png → PCA Segments
│ ├── output14.png → Cluster Heatmap
│ ├── output15.png → Word Cloud (Positive)
│ ├── output16.png → Word Cloud (Negative)
│ ├── output17.png → Sentiment Distribution
│ ├── output18.png → Sentiment vs Satisfaction
│ ├── output19.png → Topic Frequency
│ ├── output20.png → Topic Modeling Results
│ └── output21.png → Combined Sentiment Correlation
│
├── dashboard/
│ ├── app_final_dark.py
│
└── README.md

---

## 🧩 How to Run

### Install Requirements
```bash
pip install -r requirements.txt
