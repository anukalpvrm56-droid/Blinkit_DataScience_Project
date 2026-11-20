"""
Unit tests for Statistical Hypothesis Testing (Unit II, Lab Exp 3).
"""
import pytest
from src.statistical_tests import run_chi_square_test, run_one_way_anova, run_two_sample_ttest

def test_chi_square_test():
    res = run_chi_square_test("customer_segment", "delivery_status")
    assert "chi2_statistic" in res
    assert "p_value" in res
    assert res["chi2_statistic"] > 0
    assert 0.0 <= res["p_value"] <= 1.0

def test_one_way_anova():
    res = run_one_way_anova("category", "order_total")
    assert "f_statistic" in res
    assert "p_value" in res
    assert res["f_statistic"] > 0
    assert 0.0 <= res["p_value"] <= 1.0
    assert len(res["group_summary"]) == 11

def test_two_sample_ttest():
    res = run_two_sample_ttest("UPI", "Cash")
    assert "t_statistic" in res
    assert "p_value" in res
    assert 0.0 <= res["p_value"] <= 1.0
