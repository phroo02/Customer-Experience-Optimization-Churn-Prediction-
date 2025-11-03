Step 1 — Data Sources (your building blocks)

From your database retail_customer_experience.db:

Table	Content
customer_360_enriched	Cleaned + sentiment-enriched master dataset
customer_360_segmented	Clustered customers (with segment labels)
customer_360_predicted	Model outputs (churn probability, predicted satisfaction)
campaigns	Marketing KPIs
support_tickets	Ticket details (for drill-downs)


Step 2 — Dashboard Architecture (Tabs)
Tab	Purpose
🏠 Overview / KPIs	Company-level metrics & trends
👥 Customers & Segments	RFM, clusters, top customers
💬 Support & Satisfaction	Service efficiency, SHAP drivers
📈 Churn Prediction	Model results, feature importance
💭 Sentiment & Feedback	Review & support tone, top themes
📣 Campaign ROI	Marketing performance
🧾 Executive Summary	One-page snapshot & download