"""
Unit tests for Data Pipeline & SQLite Relational Ingestion.
"""
import pytest
import pandas as pd
from src.data_pipeline import get_connection, run_query, load_table, get_merged_orders, get_daily_sales, get_data_quality_report

def test_database_connection():
    conn = get_connection()
    assert conn is not None
    conn.close()

def test_load_tables():
    orders = load_table("orders")
    customers = load_table("customers")
    products = load_table("products")
    assert len(orders) == 4538
    assert len(customers) == 2277
    assert len(products) == 268

def test_merged_orders_sql():
    df = get_merged_orders()
    assert len(df) == 4538
    assert "category" in df.columns
    assert "postal_circle" in df.columns
    assert "order_total" in df.columns

def test_daily_sales_series():
    series = get_daily_sales(metric="revenue")
    assert len(series) == 600
    assert series.mean() > 10000

def test_data_quality_report():
    report = get_data_quality_report()
    assert "orders" in report
    assert report["orders"]["null_values"] == 0
    assert report["orders"]["duplicate_rows"] == 0

def test_sql_join_query():
    sql = """
    SELECT 
        p.category, 
        COUNT(DISTINCT o.order_id) AS total_orders, 
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_gmv 
    FROM orders o 
    JOIN order_items oi ON o.order_id = oi.order_id 
    JOIN products p ON oi.product_id = p.product_id 
    GROUP BY p.category 
    ORDER BY total_gmv DESC 
    LIMIT 5;
    """
    df = run_query(sql)
    assert len(df) == 5
    assert "category" in df.columns
    assert "total_gmv" in df.columns
    assert df["total_gmv"].iloc[0] > 0
