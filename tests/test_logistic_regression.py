"""
Unit tests for Standalone Logistic Regression Delivery Delay Prediction Module.
"""
import pytest
import pandas as pd
from logistic_regression_project import (
    load_and_preprocess_data,
    train_logistic_regression,
    evaluate_model,
    predict_order_delay
)

def test_load_and_preprocess_data():
    X, y, df = load_and_preprocess_data()
    assert len(df) == 4538
    assert len(y) == 4538
    assert "is_delayed" in df.columns
    assert set(y.unique()) == {0, 1}
    assert "order_total" in X.columns
    assert "is_peak_hours" in X.columns

def test_train_logistic_regression():
    X, y, _ = load_and_preprocess_data()
    pipeline = train_logistic_regression(X, y, test_size=0.20, random_state=42)
    assert pipeline["model_balanced"] is not None
    assert len(pipeline["X_test"]) == len(pipeline["y_test"])
    assert len(pipeline["X_train"]) + len(pipeline["X_test"]) == len(X)
    assert len(pipeline["odds_ratios"]) == X.shape[1]

def test_evaluate_model():
    X, y, _ = load_and_preprocess_data()
    pipeline = train_logistic_regression(X, y)
    metrics = evaluate_model(pipeline["model_balanced"], pipeline["X_test_scaled"], pipeline["y_test"])
    assert 0.0 <= metrics["Accuracy"] <= 1.0
    assert 0.0 <= metrics["Recall"] <= 1.0
    assert metrics["Confusion_Matrix"].shape == (2, 2)
    assert metrics["TP"] + metrics["FP"] + metrics["TN"] + metrics["FN"] == len(pipeline["y_test"])

def test_predict_order_delay():
    X, y, _ = load_and_preprocess_data()
    pipeline = train_logistic_regression(X, y)
    res = predict_order_delay(
        order_total=1500.0, order_hour=19, is_weekend=0, payment_method="UPI",
        trained_pipeline=pipeline
    )
    assert "delay_probability" in res
    assert 0.0 <= res["delay_probability"] <= 1.0
    assert res["prediction"] in ["Delayed (SLA Breach)", "On Time"]
    assert res["alert_level"] in ["HIGH RISK", "MODERATE RISK", "LOW RISK"]
