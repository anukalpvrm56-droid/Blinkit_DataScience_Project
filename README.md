# Blinkit_DataScience_Project
> **AI-Driven Sales Forecasting and Territory Optimization System Using Blinkit Q-Commerce Data**  
> *Academic Course Project — B.Tech CSE (Data Science), UPES Dehradun | Course: Fundamentals of Data Science (`CSDS2002P`)*

An end-to-end data science decision support system forecasting daily quick-commerce sales (Random Forest, Linear Regression) and clustering delivery territories using K-Means and SQLite on Blinkit data.

---

## 📌 Project Overview
- **Objective**: Accurately predict daily sales to prevent dark-store stockouts and cluster delivery territories for balanced quick-commerce operations.
- **Dataset**: 6 relational tables from Blinkit spanning **600 consecutive days**, 4,538 orders, 268 products across 10 categories, and 2,277 customers.
- **Database**: Relational **SQLite** database (`database/blinkit.db`) with relational joins and foreign key constraints.
- **Statistics**: Chi-Square Test of Independence & One-Way ANOVA (*Unit II, Lab Exp 3*).
- **Machine Learning**: Supervised Linear Regression (*Lab 4*) & Random Forest (*Lab 7*) for daily sales forecasting.
- **Unsupervised Learning**: K-Means Clustering (*Lab 6*) for delivery territory design.
- **Data Mining**: Association Rule Mining (*Lab 8*) calculating Support, Confidence, and Lift for cross-category purchases.
- **Interface**: 5-page interactive **Streamlit** application.
- **Project Report**: Included as [PROJECT_REPORT.pdf](PROJECT_REPORT.pdf) (7-page formal report with live application screenshots).

---

## 👥 Team Details (UPES B2 Data Science)
- **Anukalp Verma** (SAP ID: 590028327) — *Team Lead*
- **Khemendra** (SAP ID: 590022531)
- **Aman Mishra** (SAP ID: 590023029)
- **Garvit Jain** (SAP ID: 590027230)

---

## 🎯 Syllabus Alignment Table (`CSDS2002P`)

| Course Unit | Syllabus Topic | Implementation in this Project | Code Module |
| :--- | :--- | :--- | :--- |
| **Unit I** | CRISP-DM Methodology | 6-stage lifecycle from Business Understanding to Streamlit Deployment | `app.py` (Page 1) |
| **Unit II** | Probability & Inferential Statistics | Chi-Square Test & One-Way ANOVA hypothesis testing | `src/statistical_tests.py` |
| **Unit III** | Relational DBs & Data Quality | SQLite database ingestion (`blinkit.db`) & SQL JOIN queries | `src/data_pipeline.py` |
| **Unit IV** | Feature Engineering | Time lags ($t-1, t-7$), 7-day rolling means, and day-of-week indicators | `src/forecasting.py` |
| **Unit V** | Supervised Learning (Regression) | Linear Regression (Lab 4) & Random Forest (Lab 7) | `src/forecasting.py` |
| **Unit V** | Unsupervised Clustering | K-Means clustering on territory demand volume and revenue (Lab 6) | `src/clustering.py` |
| **Unit V** | Association Rule Mining | Market basket analysis computing Support, Confidence, and Lift (Lab 8) | `src/association_rules.py` |

---

## 🚀 Quickstart Guide

### 1. Setup Virtual Environment & Install Dependencies
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Build the Relational SQLite Database
```bash
python database/make_db.py
```
*Creates `database/blinkit.db` containing 6 indexed relational tables.*

### 3. Run Automated Unit Tests (15 Tests)
```bash
PYTHONPATH=. .venv/bin/pytest tests/ -v
```
*All 15 tests pass in ~1.3 seconds.*

### 4. Launch the Streamlit Application
```bash
PYTHONPATH=. .venv/bin/streamlit run app.py
```
Open **`http://localhost:8502`** in your browser.

---

## 📂 Project Structure

```
Blinkit_DataScience_Project/
│
├── database/
│   ├── make_db.py             # Ingests CSVs into SQLite (database/blinkit.db)
│   └── blinkit.db             # Relational SQLite database
│
├── cleaned/                   # 6 cleaned Blinkit CSV transactional files
│
├── src/
│   ├── data_pipeline.py       # SQL queries, data ingestion & cleaning
│   ├── statistical_tests.py   # Chi-Square & One-Way ANOVA tests (Unit II)
│   ├── forecasting.py         # Linear Regression & Random Forest (Unit V)
│   ├── clustering.py          # K-Means territory clustering (Unit V)
│   └── association_rules.py   # Frequent itemsets & Market Basket Analysis (Unit V)
│
├── tests/
│   ├── test_audit.py          # Tests for database tables & cleaning
│   ├── test_statistical_tests.py # Tests for ANOVA, Chi-Square, t-test
│   ├── test_forecasting.py    # Tests for lags, feature engineering & models
│   └── test_optimization.py   # Tests for K-Means clustering & association rules
│
├── docs/                      # Screenshots, data dictionary, viva guide
├── app.py                     # 5-page interactive Streamlit web dashboard
├── PROJECT_REPORT.pdf         # 7-page comprehensive academic project report
├── PROJECT_REPORT.txt         # Full text report documentation
├── requirements.txt           # Minimal dependencies
└── README.md                  # Project overview
```

---

## 📊 Key Results

1. **Sales Forecasting Benchmark (119-Day Holdout Test)**:
   - **Baseline (Naive Persistence)**: WAPE = 54.40%
   - **Linear Regression (Lab Exp 4)**: WAPE = **36.93%**, MAE = ₹6,002.09
   - **Random Forest (Lab Exp 7)**: WAPE = **36.75%**, MAE = ₹5,973.24 *(Best Model — 32.4% error reduction)*
   - *Key Insight*: Both ML models significantly beat the baseline persistence heuristic by capturing weekly seasonality ($t-7$) and trailing 7-day momentum.

2. **Statistical Hypothesis Testing (Unit II)**:
   - **Chi-Square Test**: $\chi^2 = 8.8426, p = 0.1826 > 0.05 \implies$ Delivery delays are independent of customer tier (fulfillment delays stem from dark store congestion, not customer status).
   - **One-Way ANOVA**: $F = 0.5166, p = 0.8797 > 0.05 \implies$ Basket sizes are uniformly distributed across categories.

3. **K-Means Territory Clustering (Unit V)**:
   - Partitioned 30 delivery postal circles into 4 commercial clusters with a Silhouette Score of **0.3875**, separating high-density urban hubs from moderate-volume periphery zones.
