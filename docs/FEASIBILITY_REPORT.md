# Blinkit Dataset Feasibility Report & System Methodology

## 1. Executive Summary
This report documents the feasibility of building an AI-Driven Sales Forecasting and Territory Optimization System using the Blinkit dataset. In strict compliance with scientific integrity standards, this report identifies what the real dataset supports, what is missing, and how each component is addressed without fabricating synthetic data.

---

## 2. Capabilities Feasibility Assessment

### 2.1 Sales Forecasting Feasibility
* **Status**: **Fully Supported**
* **Evidence**:
  * The `orders` dataset contains continuous transaction history spanning **600 calendar days** (2023-03-16 to 2024-11-04) with **zero missing days**.
  * Total revenue across 4,538 transactions is **INR 10,024,769.44** with a mean daily revenue of **INR 16,707.95**.
  * Product categorization is well-defined across 11 departments.
* **Appropriate Granularity**:
  * Daily and weekly time frequencies at the platform level.
  * Category-level daily revenue series (e.g., Dairy & Breakfast, Snacks, Pet Care).
* **Forecasting Methodologies Supported**:
  * Naive & Seasonal Naive baselines (Lag 1, Lag 7).
  * Holt-Winters Exponential Smoothing (additive trend, weekly seasonality).
  * Auto-regressive & Moving Average (ARIMA/SARIMA).
  * Machine Learning Time-Series Regressors (Ridge, Lasso, Random Forest, Gradient Boosting) utilizing lag features ($t-1, t-2, t-7, t-14, t-28$), rolling windows, and calendar indicators.
* **Splitting & Evaluation**:
  * Chronological split: First 420 days (Train), next 90 days (Validation), final 90 days (Test).
  * Evaluation metrics: MAE, RMSE, and WAPE (Weighted Absolute Percentage Error).

---

### 2.2 Territory Optimization Feasibility
* **Status**: **Supported with Dual Strategy (Real Zonal Demand vs. Spatial Simulation)**
* **Real Dataset Attributes**:
  * Customer `area`: 316 unique urban towns/cities across India.
  * Customer `pincode`: 2,271 unique 6-digit Indian Postal PIN codes.
  * The first 2 digits of each pincode represent the **Indian Postal Circle / Sub-region** (e.g., Circle 11 = Delhi, Circle 40-44 = Maharashtra, Circle 56 = Karnataka, Circle 60-64 = Tamil Nadu).
* **Data Limitations**:
  * **No raw latitude/longitude coordinates** are present in any table.
  * `store_id` (4,538 unique values) and `delivery_partner_id` (4,538 unique values) are row-unique pseudo-identifiers, not recurring physical dark stores.
* **Methodological Solution**:
  1. **Real Data Regional Balancing**: Formulate an Operations Research model (Mixed-Integer Linear Programming) that groups and balances actual demand across Indian Postal Circles and Top Urban Clusters to minimize workload variance subject to capacity constraints.
  2. **Isolated Spatial Simulation Sandbox**: Provide a completely isolated, configurable spatial vehicle routing and territory clustering module using synthetic coordinates, clearly demarcated as a simulation to demonstrate Euclidean/Manhattan geographic territory optimization without corrupting the real dataset.

---

### 2.3 Sales Resource Allocation Feasibility
* **Status**: **Fully Supported**
* **Evidence**:
  * Product margins, unit prices, minimum stock levels, and shelf life are available in `blinkit_products_cleaned.csv`.
  * Category demand forecasts from the forecasting engine provide the direct input to the Operations Research model.
* **Methodology**:
  * Formulate a Linear Program (LP) maximizing net gross margin or fulfilling forecasted demand subject to dark-store shelf capacity, procurement working capital, and safety stock constraints.

---

## 3. Academic Integrity & Technical Decisions
1. **No Data Fabrication**: We do not inject fake GPS coordinates or synthetic sales history into the cleaned Blinkit dataset.
2. **Deterministic Redundancy Disclosures**: The report openly discloses that `delivery_delay_minutes` is $100\%$ derived from delivery timestamps, and `margin_percentage` is identical to MRP-price ratio.
3. **Reproducibility**: All models use fixed random seeds, standardized scalers, and formal out-of-sample evaluation.
