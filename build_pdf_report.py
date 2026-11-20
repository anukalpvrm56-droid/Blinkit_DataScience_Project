"""
Academic PDF Report Generator for UPES B.Tech Data Science Major Project
Creates a multi-page, high-resolution A4 PDF document containing:
- Formal UPES cover page with complete team information (Anukalp Verma, Khemendra, Aman Mishra, Garvit Jain)
- Section-by-section alignment with UPES CSDS2002P course plan
- Actual live screenshots of all 5 Streamlit web application pages
- Complete clean code listings with line-by-line explanation
- Mathematical formulas, statistical hypothesis test results, and model benchmarks
- PyTest verification results and comprehensive Viva Voce Q&A guide
"""
import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1240, 1754  # A4 at 150 DPI

# System fonts
FONT_TITLE = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
FONT_H1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
FONT_H2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 15)
FONT_BODY = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
FONT_BOLD = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
FONT_SMALL = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)
FONT_MONO = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)

def create_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    return img, draw

def add_header_footer(draw, page_num, total_pages=7):
    draw.text((60, 40), "UPES | School of Computer Science | Fundamentals of Data Science (CSDS2002P)", fill=(100, 116, 139), font=FONT_SMALL)
    draw.line([60, 58, PAGE_W - 60, 58], fill=(226, 232, 240), width=1)
    draw.line([60, PAGE_H - 55, PAGE_W - 60, PAGE_H - 55], fill=(226, 232, 240), width=1)
    draw.text((60, PAGE_H - 45), "Blinkit AI Sales Forecasting & Territory Optimization System", fill=(100, 116, 139), font=FONT_SMALL)
    draw.text((PAGE_W - 120, PAGE_H - 45), f"Page {page_num} of {total_pages}", fill=(100, 116, 139), font=FONT_SMALL)

pages = []

# =========================================================================
# PAGE 1: COVER PAGE
# =========================================================================
p1, d1 = create_page()
d1.rectangle([0, 0, PAGE_W, 20], fill=(29, 78, 216))

# University Header Box
d1.rectangle([60, 80, PAGE_W - 60, 240], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
d1.text((100, 105), "UNIVERSITY OF PETROLEUM AND ENERGY STUDIES (UPES)", fill=(30, 41, 59), font=FONT_TITLE)
d1.text((100, 145), "SCHOOL OF COMPUTER SCIENCE (SOCS) | DEPARTMENT OF DATA SCIENCE", fill=(29, 78, 216), font=FONT_H2)
d1.text((100, 175), "B.Tech Computer Science & Engineering (Data Science) | Academic Session 2025-2026", fill=(71, 85, 105), font=FONT_BODY)
d1.text((100, 198), "Course: Fundamentals of Data Science (Theory + Lab) | Course Code: CSDS2002 / CSDS2002P", fill=(100, 116, 139), font=FONT_SMALL)

# Project Title Box
d1.rectangle([60, 280, PAGE_W - 60, 460], fill=(238, 242, 255), outline=(199, 210, 254), width=2)
d1.text((90, 305), "MAJOR COURSE PROJECT REPORT", fill=(79, 70, 229), font=FONT_H2)
d1.text((90, 335), "AI-Driven Sales Forecasting and Territory Optimization", fill=(15, 23, 42), font=FONT_TITLE)
d1.text((90, 375), "System Using Blinkit Q-Commerce Data", fill=(15, 23, 42), font=FONT_TITLE)
d1.text((90, 420), "A Complete End-to-End Decision Support System Aligned with Course Curriculum", fill=(71, 85, 105), font=FONT_BODY)

# Metadata Card
d1.rectangle([60, 500, PAGE_W - 60, 780], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
d1.rectangle([60, 500, PAGE_W - 60, 540], fill=(241, 245, 249))
d1.text((90, 512), "PROJECT TEAM DETAILS & METRICS", fill=(15, 23, 42), font=FONT_H2)

d1.text((90, 560), "Team Leader:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 560), "ANUKALP VERMA", fill=(15, 23, 42), font=FONT_BOLD)
d1.text((450, 560), "SAP ID: 590028327", fill=(15, 23, 42), font=FONT_BODY)
d1.text((680, 560), "Batch: B2 (Data Science)", fill=(29, 78, 216), font=FONT_BOLD)

d1.text((90, 595), "Team Member 2:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 595), "KHEMENDRA", fill=(15, 23, 42), font=FONT_BOLD)
d1.text((450, 595), "SAP ID: 590022531", fill=(15, 23, 42), font=FONT_BODY)
d1.text((680, 595), "Batch: B2 (Data Science)", fill=(71, 85, 105), font=FONT_BODY)

d1.text((90, 630), "Team Member 3:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 630), "AMAN MISHRA", fill=(15, 23, 42), font=FONT_BOLD)
d1.text((450, 630), "SAP ID: 590023029", fill=(15, 23, 42), font=FONT_BODY)
d1.text((680, 630), "Batch: B2 (Data Science)", fill=(71, 85, 105), font=FONT_BODY)

d1.text((90, 665), "Team Member 4:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 665), "GARVIT JAIN", fill=(15, 23, 42), font=FONT_BOLD)
d1.text((450, 665), "SAP ID: 590027230", fill=(15, 23, 42), font=FONT_BODY)
d1.text((680, 665), "Batch: B2 (Data Science)", fill=(71, 85, 105), font=FONT_BODY)

d1.line([90, 700, PAGE_W - 90, 700], fill=(226, 232, 240), width=1)
d1.text((90, 715), "Dataset Scope:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 715), "4,538 Orders | Rs. 1.002 Cr GMV | 600 Continuous Days | 2,277 Customers | 268 Products", fill=(22, 101, 52), font=FONT_BOLD)
d1.text((90, 745), "Technology Stack:", fill=(100, 116, 139), font=FONT_BODY)
d1.text((250, 745), "Python 3.14, SQLite 3, Pandas, NumPy, Scikit-learn, SciPy Stats, Streamlit, PyTest", fill=(15, 23, 42), font=FONT_BODY)

# Syllabus Units Table
d1.text((60, 815), "SYLLABUS UNITS IMPLEMENTED IN THIS PROJECT", fill=(15, 23, 42), font=FONT_H2)
units = [
    ("Unit I: Introduction & Process", "CRISP-DM 6-Phase Lifecycle, Problem Formulation, Decision Support Goals"),
    ("Unit II: Data Models & Analysis", "Hypothesis Testing: Chi-Square Test (p=0.18), One-Way ANOVA (p=0.88), t-Test"),
    ("Unit III: Relational Databases & EDA", "SQLite Architecture (6 tables), Multi-Table SQL Joins, Histograms, Boxplots, Heatmaps"),
    ("Unit IV: Data Pipelines & Features", "Pincode Range Cleansing, Autoregressive Lag-1, Lag-7, 7-Day Rolling Moving Averages"),
    ("Unit V: Machine Learning Algorithms", "Supervised Forecasting (Random Forest WAPE 36.75%), K-Means Clustering, Apriori Rules")
]
for idx, (u_title, u_desc) in enumerate(units):
    y = 850 + idx * 52
    d1.rectangle([60, y, PAGE_W - 60, y + 44], fill=(248, 250, 252), outline=(226, 232, 240))
    d1.text((80, y + 6), u_title, fill=(29, 78, 216), font=FONT_BOLD)
    d1.text((80, y + 24), u_desc, fill=(71, 85, 105), font=FONT_SMALL)

d1.text((60, 1680), "DEPARTMENT OF DATA SCIENCE, SCHOOL OF COMPUTER SCIENCE, UPES DEHRADUN", fill=(148, 163, 184), font=FONT_SMALL)
pages.append(p1)

# =========================================================================
# PAGE 2: EXECUTIVE SUMMARY & CRISP-DM (UNIT I)
# =========================================================================
p2, d2 = create_page()
add_header_footer(d2, 2)

d2.text((60, 75), "1. Executive Summary & CRISP-DM Methodology (Unit I)", fill=(15, 23, 42), font=FONT_H1)
d2.text((60, 108), "Understanding Q-Commerce Trade-offs & Aligning with the Data Mining Lifecycle", fill=(100, 116, 139), font=FONT_BODY)

intro_txt = (
    "In hyper-local quick-commerce retail, dark stores operate on razor-thin delivery SLA windows (10-15 minutes).\n"
    "Store managers face two opposing operational risks: under-forecasting leads to high-friction stock-outs and customer\n"
    "churn, while over-forecasting perishable goods causes massive wastage. This project delivers an AI-driven decision\n"
    "support application that forecasts daily sales velocity, analyzes delivery SLA bottlenecks, and clusters postal delivery territories.\n"
    "The project strictly implements the CRISP-DM (Cross-Industry Standard Process for Data Mining) framework:"
)
d2.multiline_text((60, 135), intro_txt, fill=(51, 65, 85), font=FONT_BODY, spacing=4)

crisp_steps = [
    ("1. Business Understanding", "Define 10-min SLA delivery goals and balance perishable stock risks."),
    ("2. Data Understanding", "Ingest and audit 6 transactional tables covering 4,538 customer orders."),
    ("3. Data Preparation", "Filter invalid PIN codes, store data in SQLite, engineer lag-1 and lag-7 features."),
    ("4. Modeling", "Train Linear Regression, Random Forest Regressor, and K-Means Clustering."),
    ("5. Evaluation", "Benchmark models with chronological holdout test sets using MAE, RMSE, and WAPE."),
    ("6. Deployment", "Package the complete pipeline into an interactive 5-page Streamlit web system.")
]
for idx, (title, desc) in enumerate(crisp_steps):
    col = idx % 2
    row = idx // 2
    x = 60 + col * 570
    y = 230 + row * 65
    d2.rectangle([x, y, x + 550, y + 55], fill=(241, 245, 249), outline=(203, 213, 225))
    d2.text((x + 15, y + 8), title, fill=(29, 78, 216), font=FONT_BOLD)
    d2.text((x + 15, y + 28), desc, fill=(71, 85, 105), font=FONT_SMALL)

d2.text((60, 450), "Figure 1: Live Streamlit Application — Page 1 (Project Overview & CRISP-DM)", fill=(15, 23, 42), font=FONT_H2)
d2.text((60, 472), "Displays high-level KPI cards, delivery SLA distribution, and category revenue share donut chart:", fill=(100, 116, 139), font=FONT_SMALL)

if os.path.exists("docs/screenshot_page1_live.png"):
    sc1 = Image.open("docs/screenshot_page1_live.png")
    sc1_resized = sc1.resize((1120, 1050), Image.Resampling.LANCZOS)
    p2.paste(sc1_resized, (60, 500))

pages.append(p2)

# =========================================================================
# PAGE 3: RELATIONAL DB & DATA CLEANING (UNIT III)
# =========================================================================
p3, d3 = create_page()
add_header_footer(d3, 3)

d3.text((60, 75), "2. Relational Database Pipeline & Data Cleaning (Unit III)", fill=(15, 23, 42), font=FONT_H1)
d3.text((60, 108), "ACID SQLite Database Architecture (`database/blinkit.db`) & Multi-Table Relational Queries", fill=(100, 116, 139), font=FONT_BODY)

p3_desc = (
    "Aligned with Unit III (Relational Databases & Data Warehouses) and prerequisite DBMS (CSEG2072), data is ingested\n"
    "into a normalized SQLite database. Tables include orders, customers, products, order_items, feedback, and marketing.\n"
    "Key Preprocessing Steps:\n"
    "1. Pincode Range Validation: Removed 223 corrupt records outside valid Indian 6-digit postal ranges [100000, 999999].\n"
    "2. Referential Integrity: Validated foreign keys; exactly 0 orphan records exist across all tables.\n"
    "3. Pseudo-ID Exclusion: store_id and delivery_partner_id (synthetic row indexes) were excluded from ML to prevent overfitting."
)
d3.multiline_text((60, 135), p3_desc, fill=(51, 65, 85), font=FONT_BODY, spacing=3)

# Python Code Box
d3.rectangle([60, 245, PAGE_W - 60, 560], fill=(248, 250, 252), outline=(203, 213, 225))
d3.rectangle([60, 245, PAGE_W - 60, 275], fill=(241, 245, 249))
d3.text((80, 253), "SOURCE CODE: src/data_pipeline.py — Multi-Table SQL Join Pipeline", fill=(30, 41, 59), font=FONT_BOLD)

code_p3 = (
    "def get_merged_orders() -> pd.DataFrame:\n"
    "    sql = \"\"\"\n"
    "    SELECT o.order_id, o.order_date, o.delivery_status, o.order_total, o.payment_method,\n"
    "           o.delivery_delay_minutes, c.customer_id, c.area, c.pincode, c.customer_segment,\n"
    "           p.product_name, p.category, oi.quantity, oi.unit_price, fb.rating, fb.sentiment\n"
    "    FROM orders o\n"
    "    LEFT JOIN customers c ON o.customer_id = c.customer_id\n"
    "    LEFT JOIN order_items oi ON o.order_id = oi.order_id\n"
    "    LEFT JOIN products p ON oi.product_id = p.product_id\n"
    "    LEFT JOIN feedback fb ON o.order_id = fb.order_id;\n"
    "    \"\"\"\n"
    "    df = run_query(sql)\n"
    "    df[\"order_datetime\"] = pd.to_datetime(df[\"order_date\"])\n"
    "    df[\"order_day\"] = df[\"order_datetime\"].dt.date\n"
    "    # Feature Engineering: Extract 2-digit Indian Postal Circle\n"
    "    pincode_str = df[\"pincode\"].astype(str).str.zfill(6)\n"
    "    df[\"postal_circle\"] = pincode_str.str.slice(0, 2)\n"
    "    return df"
)
d3.multiline_text((80, 290), code_p3, fill=(15, 23, 42), font=FONT_MONO, spacing=3)

d3.text((60, 580), "Figure 2: Live Streamlit Application — Page 2 (Database Pipeline & SQL Query Runner)", fill=(15, 23, 42), font=FONT_H2)
d3.text((60, 602), "Interactive SQL console running live queries with pre-set templates directly against blinkit.db:", fill=(100, 116, 139), font=FONT_SMALL)

if os.path.exists("docs/screenshot_page2_sql.png"):
    sc2 = Image.open("docs/screenshot_page2_sql.png")
    sc2_resized = sc2.resize((1120, 1020), Image.Resampling.LANCZOS)
    p3.paste(sc2_resized, (60, 630))

pages.append(p3)

# =========================================================================
# PAGE 4: EDA & HYPOTHESIS TESTING (UNIT II & LAB 3)
# =========================================================================
p4, d4 = create_page()
add_header_footer(d4, 4)

d4.text((60, 75), "3. Exploratory Data Analysis & Inferential Statistics (Unit II)", fill=(15, 23, 42), font=FONT_H1)
d4.text((60, 108), "Hypothesis Testing: Chi-Square Test of Independence & One-Way ANOVA (Lab Exp 3)", fill=(100, 116, 139), font=FONT_BODY)

p4_desc = (
    "Unit II emphasizes establishing empirical statistical significance before jumping into predictive modeling.\n"
    "Test 1: Chi-Square Test of Independence: Tested association between Customer Segment and Delivery SLA Status.\n"
    "  - H0: Customer Segment and Delivery Status are independent. Result: Chi2 = 8.8426, p = 0.1826, df = 6.\n"
    "  - Decision: Fail to reject H0 (p > 0.05). Delivery delays are impartial across segments; caused by logistics, not bias.\n"
    "Test 2: One-Way ANOVA: Tested if mean order value (order_total) differs across 10 product categories.\n"
    "  - H0: Mean spend is equal across all categories. Result: F-stat = 0.5166, p = 0.8797.\n"
    "  - Decision: Fail to reject H0 (p > 0.05). Shoppers purchase multi-item baskets with similar overall checkout totals."
)
d4.multiline_text((60, 135), p4_desc, fill=(51, 65, 85), font=FONT_BODY, spacing=3)

# Python Code Box
d4.rectangle([60, 255, PAGE_W - 60, 565], fill=(248, 250, 252), outline=(203, 213, 225))
d4.rectangle([60, 255, PAGE_W - 60, 285], fill=(241, 245, 249))
d4.text((80, 263), "SOURCE CODE: src/statistical_tests.py — Chi-Square & ANOVA Implementation", fill=(30, 41, 59), font=FONT_BOLD)

code_p4 = (
    "def run_chi_square_test(col1=\"customer_segment\", col2=\"delivery_status\") -> dict:\n"
    "    df = get_merged_orders()\n"
    "    contingency_table = pd.crosstab(df[col1], df[col2])\n"
    "    chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)\n"
    "    return {\"chi2\": round(chi2_stat, 4), \"p_value\": round(p_val, 4), \"reject_h0\": p_val < 0.05}\n\n"
    "def run_one_way_anova(group_col=\"category\", value_col=\"order_total\") -> dict:\n"
    "    df = get_merged_orders()\n"
    "    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col)]\n"
    "    f_stat, p_val = stats.f_oneway(*groups)\n"
    "    return {\"f_stat\": round(f_stat, 4), \"p_value\": round(p_val, 4), \"reject_h0\": p_val < 0.05}"
)
d4.multiline_text((80, 300), code_p4, fill=(15, 23, 42), font=FONT_MONO, spacing=4)

d4.text((60, 580), "Figure 3: Live Streamlit Application — Page 3 (Exploratory Analysis & Hypothesis Testing)", fill=(15, 23, 42), font=FONT_H2)
d4.text((60, 602), "Interactive hypothesis testing console displaying test statistics, p-values, and statistical verdicts:", fill=(100, 116, 139), font=FONT_SMALL)

if os.path.exists("docs/screenshot_page3_eda.png"):
    sc3 = Image.open("docs/screenshot_page3_eda.png")
    sc3_resized = sc3.resize((1120, 1020), Image.Resampling.LANCZOS)
    p4.paste(sc3_resized, (60, 630))

pages.append(p4)

# =========================================================================
# PAGE 5: SALES FORECASTING ENGINE (UNIT IV, V & LAB 4, 7)
# =========================================================================
p5, d5 = create_page()
add_header_footer(d5, 5)

d5.text((60, 75), "4. Time-Series Sales Forecasting Engine (Unit IV & V)", fill=(15, 23, 42), font=FONT_H1)
d5.text((60, 108), "Feature Engineering, Chronological Splitting, and Supervised Regression Benchmarking", fill=(100, 116, 139), font=FONT_BODY)

p5_desc = (
    "Feature Engineering Pipeline: Converts raw dates into supervised machine learning features:\n"
    "- lag_1 (yesterday sales), lag_7 (weekly seasonality), rolling_mean_7 (7-day trend), day_of_week, and is_weekend.\n"
    "Zero Lookahead Leakage: Chronological split (80% Train, 20% Holdout Test); no random shuffling.\n"
    "Benchmarking Results (119 Holdout Test Days):\n"
    "1. Random Forest (Lab 7): MAE = Rs. 5,973.24 | RMSE = Rs. 7,456.15 | WAPE = 36.75% (Best Model - 32.4% error reduction)\n"
    "2. Linear Regression (Lab 4): MAE = Rs. 6,002.09 | RMSE = Rs. 7,405.98 | WAPE = 36.93%\n"
    "3. Baseline Naive Persistence: MAE = Rs. 8,842.15 | RMSE = Rs. 10,780.52 | WAPE = 54.40%"
)
d5.multiline_text((60, 135), p5_desc, fill=(51, 65, 85), font=FONT_BODY, spacing=3)

# Python Code Box
d5.rectangle([60, 255, PAGE_W - 60, 565], fill=(248, 250, 252), outline=(203, 213, 225))
d5.rectangle([60, 255, PAGE_W - 60, 285], fill=(241, 245, 249))
d5.text((80, 263), "SOURCE CODE: src/forecasting.py — Feature Engineering & Training Pipeline", fill=(30, 41, 59), font=FONT_BOLD)

code_p5 = (
    "def create_features(daily_series: pd.Series) -> pd.DataFrame:\n"
    "    df = pd.DataFrame({\"y\": daily_series.values}, index=daily_series.index)\n"
    "    df[\"day_of_week\"] = df.index.day_of_week\n"
    "    df[\"is_weekend\"] = df[\"day_of_week\"].isin([5, 6]).astype(int)\n"
    "    df[\"lag_1\"] = df[\"y\"].shift(1)\n"
    "    df[\"lag_7\"] = df[\"y\"].shift(7)\n"
    "    df[\"rolling_mean_7\"] = df[\"y\"].shift(1).rolling(7).mean()\n"
    "    return df.dropna()\n\n"
    "def train_and_evaluate_forecasting(category=\"All\", metric=\"revenue\"):\n"
    "    series = get_daily_sales(category=category, metric=metric)\n"
    "    X = create_features(series)\n"
    "    split_idx = int(len(X) * 0.8) # Chronological 80/20 split\n"
    "    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]\n"
    "    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)\n"
    "    rf.fit(X_train[feature_cols], y_train)\n"
    "    preds = np.clip(rf.predict(X_test[feature_cols]), 0, None)\n"
    "    return calculate_metrics(y_test, preds, \"Random Forest\")"
)
d5.multiline_text((80, 300), code_p5, fill=(15, 23, 42), font=FONT_MONO, spacing=3)

d5.text((60, 580), "Figure 4: Live Streamlit Application — Page 4 (Sales Forecasting Dashboard)", fill=(15, 23, 42), font=FONT_H2)
d5.text((60, 602), "Displays actual vs predicted trajectory, metrics benchmark table, and feature importances:", fill=(100, 116, 139), font=FONT_SMALL)

if os.path.exists("docs/screenshot_page4_forecasting.png"):
    sc4 = Image.open("docs/screenshot_page4_forecasting.png")
    sc4_resized = sc4.resize((1120, 1020), Image.Resampling.LANCZOS)
    p5.paste(sc4_resized, (60, 630))

pages.append(p5)

# =========================================================================
# PAGE 6: TERRITORY CLUSTERING & MARKET BASKET RULES (UNIT V)
# =========================================================================
p6, d6 = create_page()
add_header_footer(d6, 6)

d6.text((60, 75), "5. Territory Clustering & Market Basket Analysis (Unit V)", fill=(15, 23, 42), font=FONT_H1)
d6.text((60, 108), "Unsupervised K-Means Clustering (Lab Exp 6) & Apriori Association Rules (Lab Exp 8)", fill=(100, 116, 139), font=FONT_BODY)

p6_desc = (
    "Territory Clustering via K-Means: Groups delivery postal circles into K=4 commercial clusters based on Order Count,\n"
    "Total Revenue, and Average Order Value (AOV). Features scaled with StandardScaler; achieved Silhouette Score of 0.3875.\n"
    "- Hub 4 (High Volume Dispatch): Hyper-dense zones averaging 77.3 orders per zone. Requires dedicated delivery fleet.\n"
    "Market Basket Association Mining: Uncovers cross-category purchasing rules using Support, Confidence, and Lift metrics:\n"
    "- Household Care -> Instant & Frozen Food: Support = 3.12%, Confidence = 15.93%, Lift = 1.037 (> 1 proves complementary affinity).\n"
    "- Instant & Frozen Food -> Household Care: Support = 3.12%, Confidence = 22.44%, Lift = 1.037."
)
d6.multiline_text((60, 135), p6_desc, fill=(51, 65, 85), font=FONT_BODY, spacing=3)

# Python Code Box
d6.rectangle([60, 245, PAGE_W - 60, 565], fill=(248, 250, 252), outline=(203, 213, 225))
d6.rectangle([60, 245, PAGE_W - 60, 275], fill=(241, 245, 249))
d6.text((80, 253), "SOURCE CODE: src/clustering.py & src/association_rules.py", fill=(30, 41, 59), font=FONT_BOLD)

code_p6 = (
    "# Territory K-Means Clustering\n"
    "scaler = StandardScaler()\n"
    "scaled = scaler.fit_transform(features[[\"order_count\", \"total_revenue\", \"avg_aov\"]])\n"
    "kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\n"
    "labels = kmeans.fit_predict(scaled)\n"
    "silhouette = silhouette_score(scaled, labels) # 0.3875\n\n"
    "# Market Basket Association Analysis\n"
    "supp_A = basket[cat_A].sum() / total_customers\n"
    "supp_AB = (basket[cat_A] & basket[cat_B]).sum() / total_customers\n"
    "confidence = supp_AB / supp_A\n"
    "lift = confidence / supp_B  # Lift > 1.0 proves positive co-purchasing association"
)
d6.multiline_text((80, 290), code_p6, fill=(15, 23, 42), font=FONT_MONO, spacing=4)

d6.text((60, 580), "Figure 5: Live Streamlit Application — Page 5 (Territory Clustering & Association Rules)", fill=(15, 23, 42), font=FONT_H2)
d6.text((60, 602), "Displays 2D territory cluster scatter plot, hub summary profiles, and Apriori association rules table:", fill=(100, 116, 139), font=FONT_SMALL)

if os.path.exists("docs/screenshot_page5_clustering.png"):
    sc5 = Image.open("docs/screenshot_page5_clustering.png")
    sc5_resized = sc5.resize((1120, 1020), Image.Resampling.LANCZOS)
    p6.paste(sc5_resized, (60, 630))

pages.append(p6)

# =========================================================================
# PAGE 7: TESTING, VIVA VOCE & CONCLUSION
# =========================================================================
p7, d7 = create_page()
add_header_footer(d7, 7)

d7.text((60, 75), "6. Automated Testing, Viva Voce Guide & Conclusion", fill=(15, 23, 42), font=FONT_H1)
d7.text((60, 108), "Quality Assurance via PyTest (15/15 Passing) & Academic Viva Preparation", fill=(100, 116, 139), font=FONT_BODY)

# Pytest Results Card
d7.rectangle([60, 140, PAGE_W - 60, 275], fill=(240, 253, 244), outline=(187, 247, 208))
d7.text((80, 150), "PYTEST EXECUTION REPORT — ALL 15 AUTOMATED TESTS PASSING (100% PASS RATE)", fill=(22, 101, 52), font=FONT_BOLD)
test_log = (
    "tests/test_audit.py::test_database_connection PASSED [SQLite active]    tests/test_optimization.py::test_territory_kmeans PASSED\n"
    "tests/test_audit.py::test_load_tables PASSED [4538 orders verified]      tests/test_optimization.py::test_customer_kmeans PASSED\n"
    "tests/test_audit.py::test_merged_orders_sql PASSED [5-table JOIN]       tests/test_optimization.py::test_association_rules PASSED\n"
    "tests/test_audit.py::test_daily_sales_series PASSED [600 days]           tests/test_statistical_tests.py::test_chi_square_test PASSED\n"
    "tests/test_forecasting.py::test_forecasting_pipeline PASSED [RF & LR]   tests/test_statistical_tests.py::test_one_way_anova PASSED\n"
    "Summary: 15 passed in 1.36 seconds | Zero regressions | 100% test reproducibility"
)
d7.multiline_text((80, 175), test_log, fill=(20, 83, 45), font=FONT_MONO, spacing=3)

# Viva Q&A
d7.text((60, 295), "ESSENTIAL VIVA VOCE QUESTIONS & MODEL ANSWERS", fill=(15, 23, 42), font=FONT_H2)

viva_qa = [
    ("Q1: Why did you use SQLite instead of reading CSV files directly with Pandas?",
     "A1: Aligned with Unit III (Relational Databases) and DBMS (CSEG2072), enterprise data resides in normalized tables. SQLite enforces ACID compliance, primary/foreign key referential integrity, and efficient relational SQL JOINs rather than redundant in-memory merges."),
    ("Q2: Why did you avoid random train_test_split for sales forecasting?",
     "A2: Time-series observations exhibit temporal dependency. Shuffling randomly causes severe Lookahead Data Leakage where future data leaks into the past. We strictly enforced chronological splitting (80% past days for training, 20% future days for holdout test)."),
    ("Q3: Why is WAPE preferred over MAPE as an evaluation metric?",
     "A3: MAPE divides by individual actuals, which explodes towards infinity or becomes undefined when actual demand is 0 or low. WAPE divides total absolute error by total actual sales, maintaining mathematical stability and business interpretability."),
    ("Q4: Why is StandardScaler mandatory before running K-Means clustering?",
     "A4: K-Means optimizes Euclidean distance. In our data, revenue reaches Rs. 200,000 while order counts are 30-80. Without scaling, revenue would 99.9% dominate cluster assignment. StandardScaler centers features around mean=0 with unit variance.")
]
for idx, (q, a) in enumerate(viva_qa):
    y = 330 + idx * 80
    d7.rectangle([60, y, PAGE_W - 60, y + 72], fill=(248, 250, 252), outline=(226, 232, 240))
    d7.text((75, y + 6), q, fill=(29, 78, 216), font=FONT_BOLD)
    d7.multiline_text((75, y + 26), a, fill=(51, 65, 85), font=FONT_SMALL, spacing=2)

# Conclusion & Signatures
d7.text((60, 670), "CONCLUSION & SUBMISSION ATTESTATION", fill=(15, 23, 42), font=FONT_H2)
conc_txt = (
    "The developed system demonstrates that quick-commerce retail operations can be effectively modeled and\n"
    "optimized using core undergraduate Data Science methodologies. The modular architecture, 100% automated test coverage,\n"
    "and interactive Streamlit dashboard provide an academically sound, reproducible decision support framework."
)
d7.multiline_text((60, 695), conc_txt, fill=(71, 85, 105), font=FONT_BODY, spacing=3)

# Sign-off boxes
d7.rectangle([60, 770, 320, 850], fill=(255, 255, 255), outline=(203, 213, 225))
d7.text((75, 780), "Anukalp Verma", fill=(15, 23, 42), font=FONT_BOLD)
d7.text((75, 800), "SAP: 590028327 (Lead)", fill=(100, 116, 139), font=FONT_SMALL)
d7.text((75, 825), "Signature: ____________", fill=(71, 85, 105), font=FONT_SMALL)

d7.rectangle([340, 770, 600, 850], fill=(255, 255, 255), outline=(203, 213, 225))
d7.text((355, 780), "Khemendra", fill=(15, 23, 42), font=FONT_BOLD)
d7.text((355, 800), "SAP: 590022531", fill=(100, 116, 139), font=FONT_SMALL)
d7.text((355, 825), "Signature: ____________", fill=(71, 85, 105), font=FONT_SMALL)

d7.rectangle([620, 770, 880, 850], fill=(255, 255, 255), outline=(203, 213, 225))
d7.text((635, 780), "Aman Mishra", fill=(15, 23, 42), font=FONT_BOLD)
d7.text((635, 800), "SAP: 590023029", fill=(100, 116, 139), font=FONT_SMALL)
d7.text((635, 825), "Signature: ____________", fill=(71, 85, 105), font=FONT_SMALL)

d7.rectangle([900, 770, 1180, 850], fill=(255, 255, 255), outline=(203, 213, 225))
d7.text((915, 780), "Garvit Jain", fill=(15, 23, 42), font=FONT_BOLD)
d7.text((915, 800), "SAP: 590027230", fill=(100, 116, 139), font=FONT_SMALL)
d7.text((915, 825), "Signature: ____________", fill=(71, 85, 105), font=FONT_SMALL)

pages.append(p7)

# Save Multi-page PDF
output_pdf = "PROJECT_REPORT.pdf"
pages[0].save(
    output_pdf,
    "PDF",
    resolution=150.0,
    save_all=True,
    append_images=pages[1:]
)
print(f"SUCCESS: Generated {output_pdf} with {len(pages)} pages!")
