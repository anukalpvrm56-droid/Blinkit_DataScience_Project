"""
Unsupervised Clustering Module
[Aligned with UPES Course Plan CSDS2002P - Unit V & Lab Exp 6]

Concepts Covered:
- Unit V: K-Means Clustering, Inertia, and Silhouette Score
- Unit IV: Feature Scaling with StandardScaler
- Application: Territory Demand Grouping & Customer Behavioral Segmentation
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from src.data_pipeline import get_merged_orders, load_table

def cluster_territories_kmeans(num_clusters: int = 4, top_n: int = 30) -> dict:
    """
    [Unit V, Lab Exp 6: Territory Grouping via K-Means]
    Groups delivery postal circles into K commercial clusters based on:
    - Order Count (demand volume)
    - Total Revenue (commercial value)
    - Average Order Value (AOV / basket size)
    """
    df = get_merged_orders()
    
    # Aggregate demand by Indian Postal Circle (first 2 digits of PIN code)
    top_circles = df["postal_circle"].value_counts().head(top_n).index
    df_sub = df[df["postal_circle"].isin(top_circles)]
    
    agg_df = df_sub.groupby("postal_circle").agg(
        order_count=("order_id", "count"),
        total_revenue=("order_total", "sum"),
        avg_aov=("order_total", "mean")
    ).reset_index()
    
    features = agg_df[["order_count", "total_revenue", "avg_aov"]]
    
    # Feature Scaling (Unit IV: Essential for Euclidean distance in K-Means)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Train K-Means (Unit V)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    agg_df["Cluster"] = [f"Territory Hub {c+1}" for c in kmeans.fit_predict(scaled_features)]
    
    # Calculate Cluster Evaluation Metrics
    inertia = float(kmeans.inertia_)
    sil_score = float(silhouette_score(scaled_features, kmeans.labels_)) if num_clusters > 1 else 0.0
    
    # Cluster summary profiles
    cluster_profile = agg_df.groupby("Cluster").agg(
        total_zones=("postal_circle", "count"),
        avg_orders=("order_count", "mean"),
        avg_revenue=("total_revenue", "mean"),
        avg_basket=("avg_aov", "mean")
    ).round(2).reset_index()
    
    return {
        "clustered_data": agg_df,
        "cluster_profile": cluster_profile,
        "inertia": round(inertia, 2),
        "silhouette_score": round(sil_score, 4),
        "kmeans_model": kmeans
    }

def cluster_customers_kmeans(num_clusters: int = 3) -> dict:
    """
    [Unit V, Lab Exp 6: Customer Behavioral Segmentation via K-Means]
    Segments 2,277 customers by:
    - Lifetime order count (total_orders)
    - Average order spend (avg_order_value)
    """
    customers = load_table("customers")
    features = customers[["total_orders", "avg_order_value"]].dropna()
    
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    customers["Segment_Cluster"] = [f"Cluster {c+1}" for c in kmeans.fit_predict(scaled)]
    
    sil = float(silhouette_score(scaled, kmeans.labels_))
    
    profile = customers.groupby("Segment_Cluster").agg(
        customer_count=("customer_id", "count"),
        avg_orders=("total_orders", "mean"),
        avg_spend=("avg_order_value", "mean")
    ).round(2).reset_index()
    
    return {
        "customer_data": customers,
        "profile": profile,
        "silhouette_score": round(sil, 4)
    }

if __name__ == "__main__":
    print("Testing K-Means Clustering Module...")
    res = cluster_territories_kmeans()
    print("Territory Clustering Silhouette Score:", res["silhouette_score"])
    print("Cluster Profiles:\n", res["cluster_profile"].to_string(index=False))
