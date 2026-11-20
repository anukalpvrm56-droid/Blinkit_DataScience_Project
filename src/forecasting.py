"""
Sales Forecasting Module
[Aligned with UPES Course Plan CSDS2002P - Unit IV & Unit V]

Concepts Covered:
- Unit IV: Feature Engineering (Lags, Rolling Means, Calendar Features)
- Unit V: Supervised Learning (Linear Regression - Lab 4, Random Forest - Lab 7)
- Unit V: Model Evaluation Metrics (MAE, RMSE, WAPE)
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from src.data_pipeline import get_daily_sales

def create_features(daily_series: pd.Series) -> pd.DataFrame:
    """
    [Unit IV: Feature Construction]
    Transforms raw time-series into supervised machine learning features:
    - lag_1: Sales yesterday (t-1)
    - lag_7: Sales same day last week (t-7)
    - rolling_mean_7: 7-day trailing average
    - day_of_week: 0 (Monday) to 6 (Sunday)
    - is_weekend: 1 for Saturday/Sunday, else 0
    """
    df = pd.DataFrame({"y": daily_series.values}, index=daily_series.index)
    
    # Calendar features
    df["day_of_week"] = df.index.day_of_week
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    
    # Lag features (using shift to prevent lookahead data leakage)
    df["lag_1"] = df["y"].shift(1)
    df["lag_7"] = df["y"].shift(7)
    
    # Rolling window statistics
    df["rolling_mean_7"] = df["y"].shift(1).rolling(7).mean()
    
    # Drop rows with NaN created by lag shifts
    df = df.dropna()
    return df

def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> dict:
    """
    [Unit V: Model Evaluation Metrics]
    Calculates MAE, RMSE, and WAPE between actual and predicted values.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    total_actual = float(np.sum(y_true))
    wape = float(np.sum(np.abs(y_true - y_pred)) / total_actual * 100.0) if total_actual > 0 else 0.0
    
    return {
        "Model": model_name,
        "MAE (Rs)": round(mae, 2),
        "RMSE (Rs)": round(rmse, 2),
        "WAPE (%)": round(wape, 2)
    }

def train_and_evaluate_forecasting(category: str = "All", metric: str = "revenue", test_size: float = 0.20):
    """
    [Unit V: Supervised Forecasting Pipeline]
    1. Loads daily sales.
    2. Builds features.
    3. Chronological Train-Test Split (80% Train, 20% Holdout Test).
    4. Trains Linear Regression (Lab Exp 4) and Random Forest (Lab Exp 7).
    5. Returns forecast DataFrame and comparison metrics table.
    """
    series = get_daily_sales(category=category, metric=metric)
    featured_df = create_features(series)
    
    # Feature columns and target
    feature_cols = ["lag_1", "lag_7", "rolling_mean_7", "day_of_week", "is_weekend"]
    X = featured_df[feature_cols]
    y = featured_df["y"]
    
    # Chronological Split (No random shuffling in time series!)
    split_idx = int(len(featured_df) * (1 - test_size))
    
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    test_dates = featured_df.index[split_idx:]
    
    # Model 1: Baseline Naive (predicts previous day's sales)
    naive_preds = X_test["lag_1"].values
    
    # Model 2: Linear Regression (Syllabus Unit V, Lab Exp 4)
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_preds = np.clip(lr.predict(X_test), 0, None)
    
    # Model 3: Random Forest Regressor (Syllabus Unit V, Lab Exp 7)
    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = np.clip(rf.predict(X_test), 0, None)
    
    # Collect Metrics
    metrics = [
        calculate_metrics(y_test, naive_preds, "Baseline (Naive Persistence)"),
        calculate_metrics(y_test, lr_preds, "Linear Regression (Lab Exp 4)"),
        calculate_metrics(y_test, rf_preds, "Random Forest (Lab Exp 7)"),
    ]
    metrics_df = pd.DataFrame(metrics).sort_values("WAPE (%)")
    
    # Forecasts DataFrame
    forecast_df = pd.DataFrame({
        "Actual": y_test.values,
        "Baseline (Naive)": naive_preds,
        "Linear Regression": lr_preds,
        "Random Forest": rf_preds
    }, index=test_dates)
    
    return {
        "train_series": y_train,
        "test_series": y_test,
        "forecast_df": forecast_df,
        "metrics_df": metrics_df,
        "linear_model": lr,
        "rf_model": rf,
        "feature_importance": pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    }

if __name__ == "__main__":
    print("Testing forecasting engine...")
    res = train_and_evaluate_forecasting()
    print("\nModel Comparison Table:")
    print(res["metrics_df"].to_string(index=False))
    print("\nRandom Forest Feature Importances:")
    print(res["feature_importance"].to_string())
