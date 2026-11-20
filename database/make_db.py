"""
Database Ingestion Script (SQLite)
[Aligned with UPES Course Plan CSDS2002P - Unit III & Prerequisite DBMS CSEG2072]

Loads all 6 cleaned Blinkit CSV files into a relational SQLite database (blinkit.db).
Creates indexes on primary and foreign keys for efficient SQL joins.
"""
import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
DB_PATH = os.path.join(BASE_DIR, "database", "blinkit.db")

def create_database():
    """Reads cleaned CSVs and writes them to SQLite database."""
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = {
        "orders": "blinkit_orders_cleaned.csv",
        "customers": "blinkit_customers_cleaned.csv",
        "products": "blinkit_products_cleaned.csv",
        "order_items": "blinkit_order_items_cleaned.csv",
        "feedback": "blinkit_customer_feedback_cleaned.csv",
        "marketing": "blinkit_marketing_performance_cleaned.csv"
    }

    for table_name, csv_file in tables.items():
        csv_path = os.path.join(CLEANED_DIR, csv_file)
        if not os.path.exists(csv_path):
            print(f"Warning: {csv_path} not found.")
            continue
            
        df = pd.read_csv(csv_path)
        # Store in SQLite table
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded table '{table_name}' ({len(df)} rows)")

    # Create relational indexes for fast SQL joins
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_order ON feedback(order_id);")
    conn.commit()

    # Verify tables created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    created_tables = [row[0] for row in cursor.fetchall()]
    print(f"Database successfully built with tables: {created_tables}")

    conn.close()

if __name__ == "__main__":
    create_database()
