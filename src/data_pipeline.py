"""
Data Pipeline & Relational Ingestion Module
[Aligned with UPES Course Plan CSDS2002P - Unit III & Prerequisite DBMS CSEG2072]

Connects to the SQLite database, performs relational SQL queries (JOINs, aggregations),
and prepares clean DataFrames for statistical analysis and machine learning.
"""
import os
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "blinkit.db")

def get_connection():
    """Returns a connection to the SQLite database."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found at {DB_PATH}. Please run database/make_db.py first.")
    return sqlite3.connect(DB_PATH)

def run_query(sql_query: str) -> pd.DataFrame:
    """Executes any custom SQL query and returns the result as a Pandas DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql_query, conn)
    finally:
        conn.close()
    return df

def load_table(table_name: str) -> pd.DataFrame:
    """Loads a single table directly from the SQLite database."""
    return run_query(f"SELECT * FROM {table_name}")

def get_merged_orders() -> pd.DataFrame:
    """
    [Unit III: Working with Relational Databases & SQL Joins]
    Executes a relational SQL JOIN across 5 tables:
    orders -> customers -> order_items -> products -> feedback.
    """
    sql = """
    SELECT 
        o.order_id,
        o.order_date,
        o.promised_delivery_time,
        o.actual_delivery_time,
        o.delivery_status,
        o.order_total,
        o.payment_method,
        o.delivery_delay_minutes,
        c.customer_id,
        c.customer_name,
        c.area,
        c.pincode,
        c.customer_segment,
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        p.mrp,
        p.margin_percentage,
        p.shelf_life_days,
        f.rating,
        f.sentiment,
        f.feedback_category
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN feedback f ON o.order_id = f.order_id
    """
    df = run_query(sql)
    
    # Preprocess date and time features (Unit III & IV)
    df["order_date_dt"] = pd.to_datetime(df["order_date"])
    df["order_day"] = df["order_date_dt"].dt.date
    df["postal_circle"] = df["pincode"].astype(str).str[:2]
    
    return df

def get_daily_sales(category: str = None, metric: str = "revenue") -> pd.Series:
    """
    [Unit III & IV: Data Aggregation & Time Series Preparation]
    Aggregates orders to daily frequency.
    Ensures a continuous calendar date range from min date to max date (zero-filled for empty days).
    """
    df = get_merged_orders()
    
    if category and category != "All":
        df = df[df["category"] == category]
        
    df["order_day"] = pd.to_datetime(df["order_day"])
    
    if metric == "volume":
        daily = df.groupby("order_day")["order_id"].count()
    else:
        daily = df.groupby("order_day")["order_total"].sum()
        
    # Reindex to guarantee complete continuous date range (no missing days)
    full_date_range = pd.date_range(start=daily.index.min(), end=daily.index.max(), freq="D")
    daily = daily.reindex(full_date_range, fill_value=0.0)
    daily.name = "sales"
    
    return daily

def get_data_quality_report() -> dict:
    """
    [Unit III, Lab Exp 2: Data Quality & Preprocessing]
    Computes row counts, null counts, and duplicate counts across all database tables.
    """
    table_names = ["orders", "customers", "products", "order_items", "feedback", "marketing"]
    report = {}
    
    for t in table_names:
        df = load_table(t)
        report[t] = {
            "row_count": len(df),
            "columns": list(df.columns),
            "null_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
        }
        
    return report

if __name__ == "__main__":
    print("Testing data pipeline...")
    merged = get_merged_orders()
    print(f"Successfully joined {len(merged)} records via SQL.")
    daily = get_daily_sales()
    print(f"Daily sales time series spans {len(daily)} days. Mean daily revenue: Rs {daily.mean():,.2f}")
