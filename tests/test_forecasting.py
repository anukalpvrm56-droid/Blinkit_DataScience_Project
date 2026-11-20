"""
Unit tests for Sales Forecasting (Unit IV & V, Lab Exp 4 & 7).
"""
import pytest
import pandas as pd
import numpy as np
from src.data_pipeline import get_daily_sales
from src.forecasting import create_features, calculate_metrics, train_and_evaluate_forecasting

def test_feature_creation():
    series = get_daily_sales(metric="revenue")
    feat_df = create_features(series)
    assert "lag_1" in feat_df.columns
    assert "lag_7" in feat_df.columns
    assert "rolling_mean_7" in feat_df.columns
    assert "day_of_week" in feat_df.columns
    assert feat_df.isnull().sum().sum() == 0

def test_calculate_metrics():
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 300.0])
    m = calculate_metrics(y_true, y_pred, "Test")
    assert m["MAE (Rs)"] == 6.67
    assert m["RMSE (Rs)"] == 8.16
    assert m["WAPE (%)"] == 3.33

def test_forecasting_pipeline():
    res = train_and_evaluate_forecasting(category="All", metric="revenue")
    assert "metrics_df" in res
    assert "forecast_df" in res
    assert len(res["metrics_df"]) == 3
    assert len(res["forecast_df"]) > 0
    # Check that predictions are non-negative
    assert (res["forecast_df"]["Linear Regression"] >= 0).all()
    assert (res["forecast_df"]["Random Forest"] >= 0).all()
