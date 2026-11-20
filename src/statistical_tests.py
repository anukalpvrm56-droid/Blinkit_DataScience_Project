"""
Statistical Hypothesis Testing Module
[Aligned with UPES Course Plan CSDS2002P - Unit II & Lab Exp 3]

Implements standard inferential statistical tests:
1. Chi-Square Test of Independence (Categorical vs Categorical)
2. One-Way ANOVA - Analysis of Variance (Numerical across Multiple Groups)
3. Two-Sample Independent t-Test (Numerical across 2 Groups)
"""
import pandas as pd
import numpy as np
from scipy import stats
from src.data_pipeline import get_merged_orders

def run_chi_square_test(col1: str = "customer_segment", col2: str = "delivery_status") -> dict:
    """
    [Unit II, Lab Exp 3: Chi-Square Test of Independence]
    Hypothesis:
      H0 (Null): col1 and col2 are independent (no relationship).
      H1 (Alt): col1 and col2 are dependent (a significant association exists).
    
    Rule of thumb: If p-value < 0.05, reject H0. Else, fail to reject H0.
    """
    df = get_merged_orders()
    contingency_table = pd.crosstab(df[col1], df[col2])
    
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)
    
    is_significant = bool(p_val < 0.05)
    interpretation = (
        f"Reject H0 (p = {p_val:.4f} < 0.05): Significant relationship between {col1} and {col2}."
        if is_significant else
        f"Fail to reject H0 (p = {p_val:.4f} >= 0.05): No statistically significant relationship found. "
        f"{col1} and {col2} are independent."
    )
    
    return {
        "test_name": "Chi-Square Test of Independence",
        "variables": (col1, col2),
        "contingency_table": contingency_table,
        "chi2_statistic": round(float(chi2_stat), 4),
        "p_value": round(float(p_val), 4),
        "degrees_of_freedom": int(dof),
        "is_significant": is_significant,
        "interpretation": interpretation
    }

def run_one_way_anova(group_col: str = "category", value_col: str = "order_total") -> dict:
    """
    [Unit II, Lab Exp 3: One-Way ANOVA (Analysis of Variance)]
    Hypothesis:
      H0 (Null): The population mean of value_col is equal across all groups.
      H1 (Alt): At least one group has a significantly different mean.
    """
    df = get_merged_orders()
    groups = [group[value_col].dropna().values for _, group in df.groupby(group_col)]
    
    f_stat, p_val = stats.f_oneway(*groups)
    
    is_significant = bool(p_val < 0.05)
    interpretation = (
        f"Reject H0 (p = {p_val:.4f} < 0.05): Significant difference in mean {value_col} across {group_col} groups."
        if is_significant else
        f"Fail to reject H0 (p = {p_val:.4f} >= 0.05): Mean {value_col} is statistically equal across {group_col} groups."
    )
    
    # Calculate group summary stats (mean, std, count)
    group_stats = df.groupby(group_col)[value_col].agg(["count", "mean", "std"]).round(2)
    
    return {
        "test_name": "One-Way ANOVA",
        "group_col": group_col,
        "value_col": value_col,
        "f_statistic": round(float(f_stat), 4),
        "p_value": round(float(p_val), 4),
        "is_significant": is_significant,
        "interpretation": interpretation,
        "group_summary": group_stats
    }

def run_two_sample_ttest(category1: str = "UPI", category2: str = "Cash") -> dict:
    """
    [Unit II, Lab Exp 3: Two-Sample Independent t-Test]
    Tests if mean order totals differ between two specific payment modes.
    """
    df = get_merged_orders()
    group1 = df[df["payment_method"] == category1]["order_total"].dropna()
    group2 = df[df["payment_method"] == category2]["order_total"].dropna()
    
    t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
    
    is_significant = bool(p_val < 0.05)
    interpretation = (
        f"Reject H0 (p = {p_val:.4f} < 0.05): Significant difference in spending between {category1} and {category2}."
        if is_significant else
        f"Fail to reject H0 (p = {p_val:.4f} >= 0.05): Average spending between {category1} and {category2} is statistically equal."
    )
    
    return {
        "test_name": "Two-Sample Independent t-Test",
        "groups": (category1, category2),
        "mean_group1": round(float(group1.mean()), 2),
        "mean_group2": round(float(group2.mean()), 2),
        "t_statistic": round(float(t_stat), 4),
        "p_value": round(float(p_val), 4),
        "is_significant": is_significant,
        "interpretation": interpretation
    }

if __name__ == "__main__":
    print("Testing Statistical Hypothesis Tests...")
    chi2_res = run_chi_square_test()
    print("Chi2:", chi2_res["chi2_statistic"], "p-val:", chi2_res["p_value"])
    anova_res = run_one_way_anova()
    print("ANOVA F-stat:", anova_res["f_statistic"], "p-val:", anova_res["p_value"])
