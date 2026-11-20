# Student Project Presentation & Viva Guide
**Course**: Fundamentals of Data Science (`CSDS2002P`) — Semester III  
**Program**: B.Tech CSE (Data Science) — UPES  
**Project Title**: AI-Driven Sales Forecasting and Territory Optimization System Using Blinkit Data  

---

## 🎯 1. The 1-Minute Elevator Pitch (What to say first)

> *"Good morning Sir/Ma'am. My project is an end-to-end Data Science decision-support system built using real transactional data from Blinkit. In quick-commerce (10-15 minute grocery delivery), profitability depends on two things: accurately predicting daily sales so dark stores never run out of stock or let perishables spoil, and clustering delivery territories so hubs operate efficiently.*  
>  
> *Following the **CRISP-DM lifecycle** from our **Unit I** syllabus, I built an **SQLite relational database** in **Unit III**, performed **Hypothesis Testing (One-Way ANOVA and Chi-Square)** from **Unit II**, engineered lag and calendar features from **Unit IV**, trained **Linear Regression** (Lab Exp 4) and **Random Forest** (Lab Exp 7) from **Unit V**, clustered delivery territories using **K-Means Clustering** from **Unit V / Lab Exp 6**, discovered frequent itemsets using **Market Basket Analysis** from **Lab Exp 8**, and analyzed customer feedback with **Sentiment Analysis** from **Lab Exp 9**. The entire system is interactive and running live on Streamlit."*

---

## 📚 2. Exact Mapping to Your UPES Course Plan (`CSDS2002P`)

Whenever your faculty asks *"How does this project relate to what you learned in class?"*, use this exact mapping:

| Syllabus Unit | Topics from Syllabus | How It Is Used in Your Project | Where to Show in App |
| :--- | :--- | :--- | :--- |
| **Unit I** | Fundamentals, CRISP-DM Process, Types of Analytics (Descriptive, Diagnostic, Predictive, Prescriptive) | Structured the entire project into the 6 CRISP-DM stages covering all 4 analytics types. | **Page 1: Project Overview** |
| **Unit II** | Probability Distributions, Hypothesis Testing (Chi-Square, ANOVA) | **Chi-Square Test**: Tested if delays depend on customer segment ($p=0.182$).<br>**One-Way ANOVA**: Tested if basket totals differ across categories ($p=0.879$). | **Page 3: Tab 2 (Statistics)** |
| **Unit III** | Relational Databases (SQL), Data Quality, Cleaning, Visualization | SQLite database (`blinkit.db`) with relational SQL joins and queries; histograms, box plots, line charts. | **Page 2: SQL & Page 3: EDA** |
| **Unit IV** | Feature Engineering (Lags, Rolling Means, Calendar Features) | Created lag features ($t-1, t-7$), 7-day rolling averages, and day-of-week indicators. | **Page 4: Sales Forecasting** |
| **Unit V** | **Supervised Learning**: Linear Regression (Lab 4), Random Forest (Lab 7)<br>**Evaluation**: MAE, RMSE, WAPE | Trained Linear Regression and Random Forest to forecast daily sales against a naive baseline. | **Page 4: Sales Forecasting** |
| **Unit V** | **Unsupervised Learning**: K-Means Clustering (Lab 6) | Clustered 30 Indian Postal Circles by order count, revenue, and basket size into 4 territory hubs. | **Page 5: Tab 1 (Clustering)** |
| **Unit V** | **Association Rule Mining** (Lab 8) | Market basket analysis computing Support, Confidence, and Lift for cross-category purchases. | **Page 5: Tab 2 (Association)** |
| **Unit V** | **Sentiment Analysis** (Lab 9) | Classified 4,538 customer reviews into Positive, Neutral, and Negative sentiments. | **Page 5: Tab 3 (Sentiment)** |

---

## 🖥️ 3. Page-by-Page Demo Guide (What to show on screen)

Open the app at **`http://localhost:8501`** and walk the faculty through these 5 pages:

### Page 1: Project Overview & CRISP-DM
- **What to show**: The 5 KPI cards at the top (₹10.02M GMV, 4,538 orders, ₹2,209 AOV, 600 days, 69.6% on-time rate).
- **What to say**: *"Here we see our high-level business metrics. Total revenue is ₹10.02M across 600 days. Notice that our on-time delivery rate is 69.6%, meaning ~30.4% of orders suffered a delay. We structured our solution using the CRISP-DM methodology shown on this page."*

### Page 2: Data Cleaning & SQL Database Explorer
- **What to show**: The SQLite tables overview table, and click **Execute SQL Query** on the interactive SQL console.
- **What to say**: *"In Unit III and our prerequisite DBMS course, we learned relational databases. I wrote a Python script `make_db.py` to ingest the cleaned CSVs into an indexed SQLite database `blinkit.db`. Here we can run live SQL queries to join orders, products, and customers."*

### Page 3: Exploratory Analysis & Statistics
- **What to show**: Click on the 2 tabs:
  - **Tab 1 (EDA & Visualizations - Lab Exp 1, 5)**: Show the daily order distribution histogram and category box plots.
  - **Tab 2 (Statistical Hypothesis Tests - Lab Exp 3)**:
    - Point out the **Chi-Square Test**: $p = 0.1826 > 0.05$.  
      *Explanation*: *"Sir/Ma'am, in Unit II we studied Hypothesis Testing. We ran a Chi-Square test of independence between customer segment and delivery delay. Since p > 0.05, we fail to reject the null hypothesis—meaning delivery delays are caused by dark-store picking congestion, not customer tier."*
    - Point out the **One-Way ANOVA**: $p = 0.8797 > 0.05$.  
      *Explanation*: *"The ANOVA test shows that average order basket spending is statistically uniform across product categories."*

### Page 4: Sales Forecasting (ML Models)
- **What to show**: The benchmark table and the forecast visualizer chart showing **Linear Regression (Lab 4)** and **Random Forest (Lab 7)**.
- **What to say**: *"Following Unit V, we trained supervised machine learning models to forecast sales. In Unit IV, we engineered past lags (t-1, t-7) and 7-day rolling means. Both models achieved ~36% WAPE, outperforming the naive persistence baseline (54.4%). Linear regression did very well because daily sales fluctuate around a stationary mean of ₹16,700/day."*

### Page 5: Territory Clustering & Patterns
- **What to show**: Click on the 3 tabs:
  - **Tab 1 (K-Means Clustering - Lab Exp 6)**: Adjust the cluster slider $K=4$ and show the scatter plot.  
    *Explanation*: *"In Unit V and Lab Exp 6, we studied K-Means Clustering. Here we group 30 delivery postal circles by order volume and revenue, achieving a Silhouette Score of 0.3875."*
  - **Tab 2 (Market Basket Association Rules - Lab Exp 8)**: Show the Support, Confidence, and Lift table.  
    *Explanation*: *"In Lab Exp 8, we discovered frequent itemsets. For example, customers purchasing Dairy & Breakfast frequently also buy Pet Care and Snacks."*
  - **Tab 3 (Customer Sentiment Analysis - Lab Exp 9)**: Show the sentiment distribution bar chart.  
    *Explanation*: *"In Lab Exp 9, we classified 4,538 customer reviews. 32.9% were negative, mainly complaining about late deliveries and packaging damage."*

---

## ❓ 4. Top 10 Viva Voce Questions & Simple Answers

### Q1: What is the CRISP-DM methodology? (Unit I)
**Answer**:  
CRISP-DM stands for *Cross-Industry Standard Process for Data Mining*. It has 6 stages:
1. **Business Understanding**: Solving quick-commerce inventory and delivery bottlenecks.
2. **Data Understanding**: Auditing the 6 Blinkit tables over 600 days.
3. **Data Preparation**: Cleaning data, loading into SQLite, and engineering lag features.
4. **Modeling**: Training Linear Regression, Random Forest, and K-Means.
5. **Evaluation**: Measuring MAE, RMSE, and WAPE on an out-of-sample holdout test set.
6. **Deployment**: Delivering an interactive Streamlit decision-support application.

### Q2: What hypothesis tests did you perform and what were the findings? (Unit II, Lab Exp 3)
**Answer**:  
1. **Chi-Square Test of Independence**: Tested if delivery delay (`On Time` vs `Delayed`) depends on `customer_segment` (`New`, `Regular`, `Premium`). Result: $p = 0.1826 > 0.05$. We fail to reject $H_0$, concluding delivery delays occur independently of customer tier.
2. **One-Way ANOVA**: Tested if mean `order_total` differs across 11 product categories. Result: $p = 0.8797 > 0.05$. Fail to reject $H_0$, proving basket spend is statistically uniform across categories.

### Q3: What is the difference between Linear Regression and Random Forest? (Unit V, Lab Exp 4, 7)
**Answer**:  
- **Linear Regression**: A parametric model that fits a straight line $y = \beta_0 + \beta_1 X_1 + \dots$ using Ordinary Least Squares (OLS). It is simple, fast, and resists overfitting on noisy data.
- **Random Forest**: An ensemble of decision trees using bagging (bootstrap aggregating). It splits data non-linearly, but on noisy stationary daily sales data, it can slightly overfit to past daily spikes.

### Q4: Why did Linear Regression perform so well compared to Random Forest?
**Answer**:  
Daily retail sales fluctuate as a noisy stationary series around ₹16,707/day. Decision trees create piecewise constant step functions that struggle to extrapolate beyond past training values. The linear regression model keeps predictions smooth, achieving an out-of-sample WAPE of 36.9%.

### Q5: How did you do Feature Engineering? (Unit IV)
**Answer**:  
We constructed:
1. **Lag features**: `lag_1` (yesterday's sales) and `lag_7` (sales 7 days ago, capturing weekly cycles).
2. **Rolling window statistics**: `rolling_mean_7` (7-day trailing average) to capture momentum.
3. **Calendar features**: `day_of_week` (0 to 6) and `is_weekend` (binary flag).  
We used `shift(1)` so the model only looks at past data, preventing data leakage.

### Q6: How does K-Means Clustering work? (Unit V, Lab Exp 6)
**Answer**:  
K-Means is an unsupervised learning algorithm that partitions $N$ points into $K$ clusters:
1. Initializes $K$ cluster centroids.
2. Assigns each point to the nearest centroid using Euclidean distance.
3. Re-calculates each centroid as the mean of its assigned points.
4. Repeats until centroids stabilize (convergence).  
We evaluated cluster quality using the **Silhouette Score** (0.3875).

### Q7: What are Support, Confidence, and Lift in Association Rules? (Unit V, Lab Exp 8)
**Answer**:  
- **Support**: Percentage of customer transactions containing both categories $A$ and $B$.
- **Confidence**: Probability that a customer buys $B$ given they bought $A$ ($\frac{\text{Support}(A \cap B)}{\text{Support}(A)}$).
- **Lift**: $\frac{\text{Confidence}}{\text{Support}(B)}$. If Lift > 1.0, it means categories $A$ and $B$ are bought together more frequently than random chance.

### Q8: What is the difference between MAE, RMSE, and WAPE? (Unit V)
**Answer**:  
- **MAE (Mean Absolute Error)**: Average absolute error in Rupees ($|y - \hat{y}|$). Easy to understand.
- **RMSE (Root Mean Squared Error)**: Square root of mean squared error. Penalizes large errors heavily.
- **WAPE (Weighted Absolute Percentage Error)**: $\frac{\sum |y - \hat{y}|}{\sum y} \times 100$. Unlike MAPE, WAPE does not divide by zero on days with low or zero sales.

### Q9: How did you avoid Data Leakage?
**Answer**:  
We used a strict **chronological split**: the first 80% of days for training and the final 20% for testing. We never shuffled the data randomly, because random shuffling leaks future information into past training rows.

### Q10: How did you perform Sentiment Analysis? (Lab Exp 9)
**Answer**:  
Using `feedback` table data (4,538 customer reviews), we analyzed customer ratings (1 to 5 stars) and sentiment labels (`Positive`, `Neutral`, `Negative`) across categories like Delivery, App Experience, and Product Quality. We found that 32.9% of feedback was negative, primarily caused by delivery delays and damaged packaging.
