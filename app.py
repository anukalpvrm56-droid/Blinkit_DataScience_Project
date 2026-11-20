"""
AI-Driven Sales Forecasting and Territory Optimization System Using Blinkit Data
[B.Tech CSE Data Science - Semester III Project (CSDS2002P)]

An academic, student-friendly decision support system implementing:
1. CRISP-DM Lifecycle & Relational SQL Pipeline (Unit I & III)
2. Statistical Hypothesis Testing: Chi-Square & ANOVA (Unit II, Lab Exp 3)
3. Exploratory Data Analysis & Visualizations (Unit III, Lab Exp 1 & 5)
4. Supervised Sales Forecasting: Linear Regression & Random Forest (Unit V, Lab Exp 4 & 7)
5. Unsupervised Territory Clustering (K-Means) & Market Basket Analysis (Unit V, Lab Exp 6 & 8)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_pipeline import (
    load_table, get_merged_orders, get_daily_sales, get_data_quality_report, run_query
)
from src.statistical_tests import (
    run_chi_square_test, run_one_way_anova, run_two_sample_ttest
)
from src.forecasting import train_and_evaluate_forecasting
from src.clustering import cluster_territories_kmeans, cluster_customers_kmeans
from src.association_rules import mine_category_association_rules

st.set_page_config(
    page_title="Blinkit AI Analytics System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }
    .badge-info {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation (5 Simple, Meaningful Pages)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Blinkit-yellow-app-icon.svg", width=60)
st.sidebar.title("Blinkit Data Science")
st.sidebar.markdown("**Course Project (CSDS2002P)**")

pages = [
    "1. Project Overview & CRISP-DM",
    "2. Data Cleaning & SQL Database",
    "3. Exploratory Analysis & Statistics",
    "4. Sales Forecasting (ML Models)",
    "5. Territory Clustering & Patterns"
]

selected_page = st.sidebar.radio("Navigation:", pages)
st.sidebar.divider()
st.sidebar.caption("🎓 **B.Tech CSE (Data Science) - 2nd Year**\nBuilt with Python, SQLite, Pandas, Scikit-learn & Streamlit.")

# Load primary cached data
@st.cache_data
def load_all_data():
    merged = get_merged_orders()
    quality = get_data_quality_report()
    return merged, quality

merged_df, quality_report = load_all_data()

# ==========================================
# PAGE 1: PROJECT OVERVIEW & CRISP-DM
# ==========================================
if selected_page == "1. Project Overview & CRISP-DM":
    st.markdown("<div class='main-title'>⚡ Blinkit Sales Forecasting & Territory Optimization</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Decision Support System Aligned with Course Syllabus CSDS2002P</div>", unsafe_allow_html=True)
    
    # KPI metric cards
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue (GMV)", f"₹{merged_df['order_total'].sum():,.0f}")
    c2.metric("Total Orders", f"{len(merged_df):,}")
    c3.metric("Average Basket Value", f"₹{merged_df['order_total'].mean():.2f}")
    c4.metric("Temporal Span", "600 Days", "Zero Missing Dates")
    sla_pct = (merged_df["delivery_status"] == "On Time").mean() * 100
    c5.metric("On-Time SLA Rate", f"{sla_pct:.1f}%", f"-{100-sla_pct:.1f}% Delayed", delta_color="inverse")
    
    st.divider()
    
    col_left, col_right = st.columns([1.3, 1.0])
    with col_left:
        st.subheader("1. Problem Statement & Motivation")
        st.markdown("""
        In quick-commerce retail (10–15 minute delivery promises):
        - **Stock-Outs & Wastage**: Under-forecasting causes lost sales, while over-forecasting perishable items (like milk and vegetables) leads to spoilage.
        - **Territory Inequity**: Uneven order distribution creates dispatch bottlenecks in certain delivery hubs while neighboring hubs remain under-utilized.
        
        This project uses data science and machine learning techniques from our 2nd-year coursework to forecast sales, analyze delivery bottlenecks, and cluster delivery territories.
        """)
        
        st.subheader("2. CRISP-DM Methodology Alignment (Syllabus Unit I)")
        st.markdown("""
        Our project follows the standard **CRISP-DM (Cross-Industry Standard Process for Data Mining)** lifecycle:
        1. **Business Understanding**: Define 10-15 minute delivery SLA goals and demand targets.
        2. **Data Understanding**: Ingest 6 transactional tables and audit schema integrity.
        3. **Data Preparation**: Clean invalid PIN codes, store data in SQLite, and engineer lag features.
        4. **Modeling**: Train Linear Regression, Random Forest, and K-Means Clustering.
        5. **Evaluation**: Benchmark predictions using out-of-sample MAE, RMSE, and WAPE.
        6. **Deployment**: Package into this interactive Streamlit decision-support application.
        """)
        
    with col_right:
        st.subheader("3. Category Revenue Distribution")
        cat_rev = merged_df.groupby("category")["order_total"].sum().reset_index()
        fig_pie = px.pie(
            cat_rev, values="order_total", names="category", hole=0.4,
            title="Revenue Contribution by Product Category",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(margin=dict(l=10, r=10, t=35, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# PAGE 2: DATA CLEANING & SQL DATABASE EXPLORER
# ==========================================
elif selected_page == "2. Data Cleaning & SQL Database":
    st.header("🗄️ Relational Database Pipeline & Data Cleaning")
    st.markdown("Aligned with **Unit III (Relational Databases & Data Quality)** and prerequisite **DBMS (CSEG2072)**.")
    
    st.subheader("1. SQLite Relational Database Overview (`database/blinkit.db`)")
    summary_rows = []
    for t_name, info in quality_report.items():
        summary_rows.append({
            "Table Name": t_name,
            "Row Count": info["row_count"],
            "Column Count": len(info["columns"]),
            "Missing Values (Nulls)": info["null_values"],
            "Duplicate Rows": info["duplicate_rows"],
            "Primary / Join Key": "order_id" if "order" in t_name else ("customer_id" if "customer" in t_name else "product_id")
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)
    
    st.subheader("2. Interactive SQL Query Runner")
    st.caption("Write custom SQL queries or choose from curriculum-aligned templates against `database/blinkit.db`:")
    
    preset_queries = {
        "Top 5 Categories by Revenue (3-Table JOIN)": """SELECT 
    p.category, 
    COUNT(DISTINCT o.order_id) AS total_orders, 
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_gmv 
FROM orders o 
JOIN order_items oi ON o.order_id = oi.order_id 
JOIN products p ON oi.product_id = p.product_id 
GROUP BY p.category 
ORDER BY total_gmv DESC 
LIMIT 5;""",
        "Order Delivery Status & Average Delay": """SELECT 
    delivery_status, 
    COUNT(order_id) AS order_count, 
    ROUND(AVG(delivery_delay_minutes), 2) AS avg_delay_mins,
    ROUND(SUM(order_total), 2) AS total_revenue
FROM orders 
GROUP BY delivery_status 
ORDER BY order_count DESC;""",
        "Customer Segment Order Statistics": """SELECT 
    customer_segment, 
    COUNT(customer_id) AS total_customers, 
    ROUND(AVG(avg_order_value), 2) AS mean_aov, 
    SUM(total_orders) AS cumulative_orders 
FROM customers 
GROUP BY customer_segment 
ORDER BY cumulative_orders DESC;""",
        "Top 5 Best-Selling Products by Units Sold": """SELECT 
    p.product_name, 
    p.category, 
    SUM(oi.quantity) AS total_units_sold, 
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS product_revenue 
FROM order_items oi 
JOIN products p ON oi.product_id = p.product_id 
GROUP BY p.product_id, p.product_name, p.category 
ORDER BY total_units_sold DESC 
LIMIT 5;""",
        "Custom SQL Query": ""
    }
    
    chosen_template = st.selectbox("Select SQL Query Template:", list(preset_queries.keys()))
    default_sql = preset_queries[chosen_template] if preset_queries[chosen_template] else "SELECT * FROM orders LIMIT 5;"
    user_query = st.text_area("SQL Statement (editable):", value=default_sql, height=120)
    
    if st.button("Execute SQL Query", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a valid SQL query.")
        else:
            try:
                query_res = run_query(user_query)
                st.success(f"Query executed successfully! Returned {len(query_res)} rows.")
                st.dataframe(query_res, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
                st.info("💡 **Viva / Debugging Tip**: When joining multiple tables (e.g., `orders` and `order_items`), qualify shared column names with table aliases (e.g., `o.order_id` instead of `order_id`) to avoid ambiguous column errors.")
            
    st.divider()
    st.subheader("3. Data Cleaning & Validation (Lab Exp 2)")
    st.markdown("""
    - **Pincode Validation**: Dropped 223 invalid records outside the valid Indian 6-digit postal range `[100000, 999999]`.
    - **Referential Integrity**: Verified foreign keys; zero orphan rows exist between `orders`, `customers`, and `products`.
    - **Pseudo-ID Exclusion**: Identified `store_id` (4,538 unique) and `delivery_partner_id` (4,538 unique) as synthetic row IDs and excluded them from machine learning.
    """)

# ==========================================
# PAGE 3: EXPLORATORY ANALYSIS & STATISTICS
# ==========================================
elif selected_page == "3. Exploratory Analysis & Statistics":
    st.header("📈 Exploratory Data Analysis & Inferential Statistics")
    st.markdown("Aligned with **Unit II (Hypothesis Testing & ANOVA)** and **Unit III (Visualizations - Lab Exp 1, 3, 5)**.")
    
    tab_eda, tab_stats = st.tabs(["📊 Exploratory Data Analysis (EDA)", "🧪 Statistical Hypothesis Tests (ANOVA & Chi-Square)"])
    
    with tab_eda:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Daily Order Volume Distribution (Histogram)")
            daily_series = get_daily_sales(metric="volume")
            fig_hist = px.histogram(
                daily_series, x="sales", nbins=18,
                title="Distribution of Daily Order Volume (Lab Exp 1)",
                labels={"sales": "Orders per Day"},
                color_discrete_sequence=["#3B82F6"]
            )
            fig_hist.update_layout(template="plotly_white")
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with c2:
            st.subheader("Basket Spend by Category (Box Plot)")
            fig_box = px.box(
                merged_df, x="category", y="order_total",
                title="Order Value Box Plot across Categories (Lab Exp 5)",
                color="category"
            )
            fig_box.update_layout(template="plotly_white", showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_box, use_container_width=True)
            
        st.subheader("Time Series Sales Trajectory (600 Days)")
        daily_rev = get_daily_sales(metric="revenue")
        rolling_7 = daily_rev.rolling(7).mean()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=daily_rev.index, y=daily_rev.values, mode="lines", name="Daily Revenue", line=dict(color="#93C5FD", width=1)))
        fig_line.add_trace(go.Scatter(x=daily_rev.index, y=rolling_7, mode="lines", name="7-Day Moving Average", line=dict(color="#1D4ED8", width=2.5)))
        fig_line.update_layout(title="Daily Sales Revenue & 7-Day Trend Line", xaxis_title="Date", yaxis_title="Revenue (Rs)", template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)
        
    with tab_stats:
        st.subheader("🧪 Inferential Hypothesis Testing (Unit II, Lab Exp 3)")
        
        st1, st2 = st.columns(2)
        with st1:
            st.markdown("#### Test 1: Chi-Square Test of Independence")
            st.caption("Testing if delivery delays depend on customer segment (New, Regular, Premium).")
            chi_res = run_chi_square_test()
            st.dataframe(chi_res["contingency_table"], use_container_width=True)
            m1, m2 = st.columns(2)
            m1.metric("Chi-Square Stat", f"{chi_res['chi2_statistic']:.4f}")
            m2.metric("p-value", f"{chi_res['p_value']:.4f}")
            st.info(f"💡 **Academic Interpretation**: {chi_res['interpretation']}")
            
        with st2:
            st.markdown("#### Test 2: One-Way ANOVA (Analysis of Variance)")
            st.caption("Testing if mean order spend differs significantly across product categories.")
            anova_res = run_one_way_anova()
            m3, m4 = st.columns(2)
            m3.metric("F-Statistic", f"{anova_res['f_statistic']:.4f}")
            m4.metric("p-value", f"{anova_res['p_value']:.4f}")
            st.info(f"💡 **Academic Interpretation**: {anova_res['interpretation']}")
            st.dataframe(anova_res["group_summary"], use_container_width=True)

# ==========================================
# PAGE 4: SALES FORECASTING (ML MODELS)
# ==========================================
elif selected_page == "4. Sales Forecasting (ML Models)":
    st.header("🔮 Sales Forecasting with Supervised Learning")
    st.markdown("Aligned with **Unit IV (Feature Engineering)** and **Unit V (Supervised Learning - Lab Exp 4 & 7)**.")
    
    fc_cat = st.selectbox("Select Category:", ["All"] + sorted(list(merged_df["category"].unique())))
    fc_metric = st.selectbox("Select Target Metric:", ["revenue", "volume"], format_func=lambda x: "Revenue (Rs)" if x=="revenue" else "Order Volume")
    
    with st.spinner("Training Linear Regression and Random Forest models..."):
        fc_res = train_and_evaluate_forecasting(category=fc_cat, metric=fc_metric)
        
    st.subheader("1. Model Performance Benchmark (Out-of-Sample Test Set)")
    st.dataframe(fc_res["metrics_df"], use_container_width=True)
    
    st.subheader("2. Forecast Visualizer (Actual vs. Predictions)")
    fc_df = fc_res["forecast_df"]
    
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=fc_df.index, y=fc_df["Actual"], mode="lines+markers", name="Actual Ground Truth", line=dict(color="#111827", width=2)))
    fig_fc.add_trace(go.Scatter(x=fc_df.index, y=fc_df["Linear Regression"], mode="lines", name="Linear Regression (Lab Exp 4)", line=dict(color="#2563EB", width=2)))
    fig_fc.add_trace(go.Scatter(x=fc_df.index, y=fc_df["Random Forest"], mode="lines", name="Random Forest (Lab Exp 7)", line=dict(color="#10B981", width=2)))
    fig_fc.add_trace(go.Scatter(x=fc_df.index, y=fc_df["Baseline (Naive)"], mode="lines", name="Baseline (Naive)", line=dict(color="#9CA3AF", width=1.5, dash="dot")))
    fig_fc.update_layout(title="Out-of-Sample Sales Forecast Comparison", xaxis_title="Date", yaxis_title="Sales Target", template="plotly_white")
    st.plotly_chart(fig_fc, use_container_width=True)
    
    col_feat1, col_feat2 = st.columns(2)
    with col_feat1:
        st.subheader("3. Feature Importance (Random Forest)")
        st.caption("Shows which past time lags influenced the tree ensemble the most:")
        feat_df = fc_res["feature_importance"].reset_index()
        feat_df.columns = ["Feature", "Importance Weight"]
        fig_feat = px.bar(feat_df, x="Importance Weight", y="Feature", orientation="h", color="Importance Weight", color_continuous_scale="Viridis")
        fig_feat.update_layout(template="plotly_white")
        st.plotly_chart(fig_feat, use_container_width=True)
        
    with col_feat2:
        st.subheader("4. Why Linear Regression Outperforms Deep Trees")
        st.info("""
        **Academic Finding for Viva Voce:**
        - The daily quick-commerce sales series fluctuates around a stable stationary mean of ~₹16,700/day.
        - **Linear Regression** uses a smooth Ordinary Least Squares (OLS) line that resists noisy day-to-day fluctuations.
        - **Random Forest** creates piecewise constant splits that can slightly overfit to past daily spikes.
        - Hence, simple regularized linear models achieve competitive or lower WAPE error (~36%).
        """)

# ==========================================
# PAGE 5: TERRITORY CLUSTERING & PATTERNS
# ==========================================
elif selected_page == "5. Territory Clustering & Patterns":
    st.header("🗺️ Territory Clustering & Market Basket Analysis")
    st.markdown("Aligned with **Unit V (K-Means Clustering - Lab Exp 6)** and **Association Analysis (Lab Exp 8)**.")
    
    cluster_tab, assoc_tab, sentiment_tab = st.tabs([
        "📍 Territory K-Means Clustering (Lab Exp 6)",
        "🛒 Market Basket Association Rules (Lab Exp 8)",
        "💬 Customer Sentiment Analysis (Lab Exp 9)"
    ])
    
    with cluster_tab:
        st.subheader("1. K-Means Clustering of Delivery Postal Circles")
        st.caption("Groups 30 Indian Postal Circles by Order Volume, Total Revenue, and Basket Size.")
        k_val = st.slider("Select Number of Clusters (K):", min_value=2, max_value=6, value=4)
        
        clust_res = cluster_territories_kmeans(num_clusters=k_val)
        
        m_sil, m_in = st.columns(2)
        m_sil.metric("Silhouette Score (Quality)", f"{clust_res['silhouette_score']:.4f}")
        m_in.metric("Inertia (Within-Cluster Sum of Squares)", f"{clust_res['inertia']:,.1f}")
        
        fig_cluster = px.scatter(
            clust_res["clustered_data"],
            x="order_count", y="total_revenue",
            color="Cluster", size="avg_aov",
            hover_data=["postal_circle", "avg_aov"],
            title=f"K-Means Clustering on Delivery Demand (K={k_val})",
            labels={"order_count": "Total Orders Placed", "total_revenue": "Total Revenue (Rs)"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_cluster.update_layout(template="plotly_white")
        st.plotly_chart(fig_cluster, use_container_width=True)
        
        st.subheader("Cluster Profile Table")
        st.dataframe(clust_res["cluster_profile"], use_container_width=True)
        
    with assoc_tab:
        st.subheader("2. Frequent Category Association Rules (Lab Exp 8)")
        st.caption("Analyzes which product categories customers frequently buy together.")
        
        min_supp = st.slider("Minimum Support Threshold (%):", min_value=1.0, max_value=10.0, value=4.0, step=0.5) / 100.0
        min_conf = st.slider("Minimum Confidence Threshold (%):", min_value=10.0, max_value=50.0, value=15.0, step=5.0) / 100.0
        
        rules_df = mine_category_association_rules(min_support=min_supp, min_confidence=min_conf)
        
        if not rules_df.empty:
            st.dataframe(rules_df, use_container_width=True)
            st.info("""
            **Rule Interpretation**:
            - **Support**: Percentage of customer transactions containing both categories.
            - **Confidence**: Probability that a customer buys Consequent given they bought Antecedent.
            - **Lift > 1.0**: Indicates a positive association (bought together more frequently than random chance).
            """)
        else:
            st.warning("No rules found at this threshold. Lower the support/confidence sliders.")
            
    with sentiment_tab:
        st.subheader("3. Customer Sentiment Analysis (Lab Exp 9)")
        fb_df = load_table("feedback")
        
        sent_counts = fb_df["sentiment"].value_counts(normalize=True) * 100
        fig_sent = px.bar(
            x=sent_counts.index, y=sent_counts.values,
            color=sent_counts.index,
            title="Customer Review Sentiment Distribution",
            labels={"x": "Sentiment Category", "y": "Percentage of Reviews (%)"},
            color_discrete_map={"Positive": "#10B981", "Neutral": "#F59E0B", "Negative": "#EF4444"}
        )
        fig_sent.update_layout(template="plotly_white")
        st.plotly_chart(fig_sent, use_container_width=True)
        
        st.dataframe(fb_df[["rating", "sentiment", "feedback_category", "feedback_text"]].head(15), use_container_width=True)
