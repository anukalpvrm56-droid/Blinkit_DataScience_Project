# Academic Project Report: AI-Driven Sales Forecasting and Territory Optimization System Using Blinkit Data

**Degree Level**: B.Tech in Computer Science & Engineering (Specialization: Data Science / Artificial Intelligence)  
**Course**: Fundamentals of Data Science & Operations Research  
**Domain**: Quick-Commerce Retail Operations, Time-Series Econometrics, Mathematical Optimization  

---

## 1. Abstract
In quick-commerce (Q-Commerce) retail, fulfilling ultra-fast delivery promises (10–15 minutes) requires strict synchronization between demand forecasting, warehouse replenishment, and geographic territory workload balancing. This project designs, implements, and verifies an end-to-end decision-support system built upon real transaction data from Blinkit. The system operates on 4,538 customer orders across 600 consecutive calendar days (March 2023 to November 2024), 268 products across 11 categories, and 2,277 customers. 

We conduct a thorough data audit, uncover table-level structural redundancies, and benchmark eight time-series forecasting models (Naive, Seasonal Naive, Moving Average, Holt-Winters Exponential Smoothing, ARIMA, Ridge Regression, Random Forest, and Gradient Boosting Regressors) using chronological train-validation-test partitioning evaluated on MAE, RMSE, and WAPE. We further formulate and solve two Operations Research models: (1) a Mixed-Integer Linear Program (MILP) partitioning real Indian Postal Circle demand into equitably balanced territory hubs to minimize workload disparity, and (2) a Linear Program (LP) maximizing gross profit under dark-store shelf capacity and capital constraints. The entire architecture is packaged into an interactive 10-page Streamlit application and validated by automated unit tests.

---

## 2. Problem Statement & Motivation
Quick-commerce platforms such as Blinkit, Zepto, and Instamart operate under razor-thin margins and aggressive delivery service-level agreements (SLAs). Inefficiencies manifest in two core bottlenecks:
1. **Demand Misalignment & Perishable Stock-outs**: Under-forecasting leads to lost sales and customer churn, while over-forecasting leads to high holding costs and inventory write-offs (especially in short shelf-life categories such as Dairy and Fruits & Vegetables).
2. **Workload Inequity & Territory Fragmentation**: Delivery hubs with unbalanced demand experience delayed dispatches, rider fatigue, and high SLA breach rates, while neighboring hubs remain underutilized.

### Project Objectives
- Ingest and audit the 6-table Blinkit schema, identifying data quality issues, redundancies, and actual geographic support.
- Develop a multi-model forecasting engine evaluating both classical econometric and machine learning algorithms on out-of-sample data without lookahead leakage.
- Formulate and solve an Operations Research territory balancing model (MILP) to minimize regional workload variance.
- Formulate and solve an inventory resource allocation model (LP) driven by forecasted category demand.
- Build an interactive decision-support application with reproducible benchmark outputs.

---

## 3. Data Audit, Schemas & Structural Redundancies
The project operates on 6 cleaned CSV files in `cleaned/`:
- `blinkit_orders_cleaned.csv` ($N = 4,538$)
- `blinkit_customers_cleaned.csv` ($N = 2,277$)
- `blinkit_products_cleaned.csv` ($N = 268$)
- `blinkit_order_items_cleaned.csv` ($N = 4,538$)
- `blinkit_customer_feedback_cleaned.csv` ($N = 4,538$)
- `blinkit_marketing_performance_cleaned.csv` ($N = 5,400$)

### Key Audit Findings & Redundancies
1. **1-to-1 Table Lockstep**: `orders`, `order_items`, and `customer_feedback` each have exactly 4,538 rows matching row-by-row. Every order contains exactly one item line, and every order has one feedback entry.
2. **Direct Deterministic Leakage**:
   - $\text{delivery\_delay\_minutes} = \text{actual\_delivery\_time} - \text{promised\_delivery\_time}$ ($100\%$ collinear).
   - $\text{delivery\_status}$ is an exact deterministic step function of delay: $\le 5\text{ min} \to \text{On Time}$, $6\text{--}15\text{ min} \to \text{Slightly Delayed}$, $>15\text{ min} \to \text{Significantly Delayed}$.
   - $\text{margin\_percentage} = \frac{\text{mrp} - \text{price}}{\text{mrp}} \times 100$ ($r = 1.0$).
3. **Pseudo-Identifiers**: `store_id` (4,538 unique) and `delivery_partner_id` (4,538 unique) are row-unique synthetic IDs and were dropped from learning algorithms.
4. **Geographic Coverage**: No raw latitude/longitude coordinates exist. Real demand is geo-indexed by 316 urban `area` labels and 2,271 6-digit `pincode` records. The first 2 digits of the pincode map to official Indian Postal Circles.

---

## 4. Time-Series Sales Forecasting Methodology

### 4.1 Chronological Splitting Strategy
To avoid lookahead bias and data leakage, the continuous 600-day series is partitioned chronologically:
- **Training Set**: Days 1 to 420 (70.0%)
- **Validation Set**: Days 421 to 510 (15.0%)
- **Holdout Test Set**: Days 511 to 600 (15.0%, $N = 90$ days)

### 4.2 Algorithm Suite
1. **Naive Baseline**: $\hat{y}_{t+h} = y_t$
2. **Seasonal Naive**: $\hat{y}_{t+h} = y_{t+h-7}$ (7-day weekly seasonality)
3. **Trailing Moving Average**: $\hat{y}_{t+h} = \frac{1}{7} \sum_{i=1}^7 y_{t-i+1}$
4. **Holt-Winters Exponential Smoothing**:
   $$\ell_t = \alpha(y_t - s_{t-m}) + (1-\alpha)(\ell_{t-1} + b_{t-1})$$
   $$b_t = \beta(\ell_t - \ell_{t-1}) + (1-\beta)b_{t-1}$$
   $$s_t = \gamma(y_t - \ell_{t-1} - b_{t-1}) + (1-\gamma)s_{t-m}$$
   $$\hat{y}_{t+h} = \ell_t + h b_t + s_{t-m+h_m^+}$$
5. **ARIMA $(p, d, q)$**: Auto-regressive integrated moving average fitted on first differences.
6. **Supervised ML Regressors (Ridge, Random Forest, GBR)**:
   - Engineered features: Lags ($t-1, t-2, t-7, t-14, t-28$), 7-day and 14-day rolling means and standard deviations, day of week, day of month, month, weekend indicator.
   - Recursive multi-step generation across test horizons.

### 4.3 Evaluation Metrics
- **Mean Absolute Error (MAE)**: $\frac{1}{n} \sum_{t=1}^n |y_t - \hat{y}_t|$
- **Root Mean Squared Error (RMSE)**: $\sqrt{\frac{1}{n} \sum_{t=1}^n (y_t - \hat{y}_t)^2}$
- **Weighted Absolute Percentage Error (WAPE)**: $\frac{\sum_{t=1}^n |y_t - \hat{y}_t|}{\sum_{t=1}^n y_t} \times 100$

### 4.4 Empirical Out-of-Sample Forecasting Results (Holdout Test N=90 Days)
| Model | MAE (INR) | RMSE (INR) | WAPE (%) | Rank |
| :--- | :--- | :--- | :--- | :--- |
| **Naive (Last Value)** | **5,484.51** | **6,726.57** | **34.33%** | **1** |
| **ARIMA (1,1,1)** | 5,551.18 | 6,778.01 | 34.75% | 2 |
| **Moving Average (7-Day)** | 5,711.97 | 7,017.24 | 35.76% | 3 |
| **ML - Ridge Regression** | 5,724.49 | 6,908.21 | 35.83% | 4 |
| **Holt-Winters Exp Smoothing** | 5,838.62 | 7,110.66 | 36.55% | 5 |
| **ML - Random Forest** | 5,957.15 | 7,173.49 | 37.29% | 6 |
| **ML - Gradient Boosting** | 6,518.63 | 8,156.65 | 40.81% | 7 |
| **Seasonal Naive (Lag 7)** | 10,052.86 | 12,037.32 | 62.93% | 8 |

*Econometric Finding*: The daily series exhibits random-walk characteristics around a stationary mean of ₹16,707/day without strong persistent weekly seasonality, allowing simple and regularized linear models (Naive, ARIMA, Ridge) to outperform high-variance tree ensembles.

---

## 5. Operations Research Formulations & Optimization

### 5.1 Territory Balancing Problem (MILP)
Let $i \in \{1,\dots,N\}$ index regional demand units (Indian Postal Circles) with demand $d_i$, and $j \in \{1,\dots,K\}$ index operational territory hubs.

**Decision Variables**:
- $x_{i,j} \in \{0, 1\}$: Binary indicator whether zone $i$ is assigned to hub $j$.
- $W_{\max}, W_{\min} \ge 0$: Continuous auxiliary variables tracking the workload extremes across hubs.

**Objective Function**:
$$\min_{x, W_{\max}, W_{\min}} \quad Z = W_{\max} - W_{\min}$$

**Constraints**:
1. **Unambiguous Assignment**: Every postal zone is assigned to exactly one hub:
   $$\sum_{j=1}^K x_{i,j} = 1 \quad \forall i \in \{1,\dots,N\}$$
2. **Workload Definition & Bounding**:
   $$\sum_{i=1}^N d_i x_{i,j} \le W_{\max} \quad \forall j \in \{1,\dots,K\}$$
   $$\sum_{i=1}^N d_i x_{i,j} \ge W_{\min} \quad \forall j \in \{1,\dots,K\}$$
3. **Integrality**:
   $$x_{i,j} \in \{0, 1\}, \quad W_{\max}, W_{\min} \ge 0$$

**Optimization Results (Top 30 Postal Circles, K=4 Hubs)**:
- Baseline (Round-Robin) Workload Std: **34.37** | Workload Range: **74.0**
- MILP Optimized Workload Std: **0.43** | Workload Range: **1.0**
- **Workload Variance Reduction**: **98.74%**
- **Solver Guarantee**: Proven global optimum via SciPy HiGHS solver in 4.2 ms.

---

### 5.2 Category Sales & Inventory Allocation Problem (LP)
Let $c \in \{1,\dots,C\}$ index product categories with selling price $p_c$, unit procurement cost $c_c$, unit storage volume footprint $v_c$, minimum safety stock $\text{MinStock}_c$, and forecasted customer demand $\hat{D}_c$.

**Decision Variables**:
- $x_c \ge 0$: Quantity procured/stocked.
- $s_c \ge 0$: Quantity sold/fulfilled to customers.

**Objective Function**:
$$\max_{x, s} \quad \sum_{c=1}^C (p_c s_c - c_c x_c)$$

**Constraints**:
1. **Fulfillment Upper Bounds**:
   $$s_c \le x_c \quad \forall c \in \{1,\dots,C\}$$
   $$s_c \le \hat{D}_c \quad \forall c \in \{1,\dots,C\}$$
2. **Procurement Budget Limit**:
   $$\sum_{c=1}^C c_c x_c \le B$$
3. **Warehouse / Shelf Space Capacity**:
   $$\sum_{c=1}^C v_c x_c \le V_{\max}$$
4. **Safety Stock Level**:
   $$x_c \ge \text{MinStock}_c \times \lambda_{\text{service}} \quad \forall c \in \{1,\dots,C\}$$
5. **Non-negativity**:
   $$x_c \ge 0, \quad s_c \ge 0$$

**Optimization Results**:
- Baseline Proportional Profit: ₹-193,548.44 (Over-procurement penalty)
- LP Optimized Profit: **₹14,662.12**
- **Demand Fulfillment Rate**: **100.0%**
- Budget & Shelf Utilization: Completely within feasibility limits.

---

## 6. System Architecture & Implementation
The application is structured into a modular Python package:
```
├── app.py                         # 10-page interactive Streamlit dashboard
├── requirements.txt               # Dependencies
├── README.md                      # Academic documentation & quickstart
├── src/
│   ├── audit.py                   # Data ingestion, schema validation & auditing
│   ├── forecasting/
│   │   ├── baselines.py           # Naive, Seasonal Naive, Moving Average
│   │   ├── classical.py           # Holt-Winters Exponential Smoothing, ARIMA
│   │   ├── ml_forecasting.py      # Feature engineering, ML regressors
│   │   ├── evaluate.py            # MAE, RMSE, WAPE calculation
│   │   └── runner.py              # Automated benchmark runner
│   ├── optimization/
│   │   ├── territory_solver.py    # MILP territory balancing & spatial simulation
│   │   └── resource_solver.py     # LP inventory & budget allocation optimizer
│   └── utils/
│       └── visualizer.py          # Interactive Plotly charts
├── tests/
│   ├── test_audit.py              # Schema integrity unit tests
│   ├── test_forecasting.py        # Model fitting & evaluation tests
│   └── test_optimization.py       # MILP & LP constraint tests
└── docs/
    ├── DATA_DICTIONARY.md         # Full column-by-column schema
    ├── FEASIBILITY_REPORT.md      # Data audit & limitation report
    └── ACADEMIC_REPORT.md         # Full project report & viva guide
```

---

## 7. Limitations & Future Scope
1. **Absence of Real-Time GPS Coordinates**: The dataset does not contain latitude/longitude coordinates; geographic balancing was conducted on official Postal Circles and Urban Clusters. Future work should ingest road-network graph APIs (e.g., OpenStreetMap / OSRM) for last-mile travel-time routing.
2. **Pseudo-Identifiers in Production Schema**: In a production setting, dark stores and riders must have static IDs to model store queue times and rider transit velocities.
3. **Hierarchical Forecasting**: Future scope includes implementing Top-Down and Bottom-Up reconciliation (MinT algorithm) across SKU, Category, and Hub levels.

---

## 8. Viva Voce Examination Questions & Answers

**Q1: What is WAPE and why was it preferred over MAPE?**  
*Answer*: WAPE (Weighted Absolute Percentage Error) is defined as $\frac{\sum |y_t - \hat{y}_t|}{\sum y_t} \times 100$. Mean Absolute Percentage Error (MAPE) divides each error by individual actual sales $y_t$. In daily retail demand, days with 0 or near-zero sales cause division by zero or infinite error spikes. WAPE aggregates total error against total volume, ensuring numerical stability and business relevance.

**Q2: Why did tree-based models (Random Forest, GBR) perform worse than the Naive and ARIMA models?**  
*Answer*: Tree-based regressors cannot extrapolate beyond the range of training target values and struggle with stationary noisy time series without strong monotonic trends. The daily Blinkit revenue series fluctuates randomly around a stable mean; consequently, the Naive last-value and regularized linear models minimized variance more effectively without overfitting.

**Q3: Explain how the Territory Balancing problem is formulated as an MILP.**  
*Answer*: The problem is framed as a min-max integer program. Decision variables $x_{ij} \in \{0, 1\}$ assign postal circle $i$ to hub $j$. We introduce two continuous bounding variables $W_{\max}$ and $W_{\min}$ and constrain the workload of every hub $j$ ($\sum_i d_i x_{ij}$) to lie between $W_{\min}$ and $W_{\max}$. The objective function minimizes $(W_{\max} - W_{\min})$. The SciPy HiGHS solver finds the global optimum, reducing workload standard deviation by $98.74\%$.

**Q4: How was data leakage prevented in feature engineering?**  
*Answer*: All lag features ($t-1, t-7$, etc.) and rolling statistics were computed using values strictly preceding the forecast period. During multi-step forecasting across the 90-day test horizon, predictions were generated recursively, appending past model predictions to the input vector rather than using future ground truth.
