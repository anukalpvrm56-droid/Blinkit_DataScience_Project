"""
Unit tests for K-Means Clustering & Association Analysis (Unit V, Lab Exp 6 & 8).
"""
import pytest
from src.clustering import cluster_territories_kmeans, cluster_customers_kmeans
from src.association_rules import mine_category_association_rules

def test_territory_kmeans():
    res = cluster_territories_kmeans(num_clusters=4, top_n=20)
    assert "clustered_data" in res
    assert "silhouette_score" in res
    assert "Cluster" in res["clustered_data"].columns
    assert res["clustered_data"]["Cluster"].nunique() == 4
    assert -1.0 <= res["silhouette_score"] <= 1.0

def test_customer_kmeans():
    res = cluster_customers_kmeans(num_clusters=3)
    assert "customer_data" in res
    assert res["profile"]["customer_count"].sum() == 2277

def test_association_rules():
    rules_df = mine_category_association_rules(min_support=0.03, min_confidence=0.10)
    assert len(rules_df) > 0
    assert "Support (%)" in rules_df.columns
    assert "Confidence (%)" in rules_df.columns
    assert "Lift" in rules_df.columns
