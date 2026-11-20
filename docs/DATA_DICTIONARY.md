# Blinkit Dataset Data Dictionary

This document details the schema, data types, constraints, and relationships for all 6 tables in the Blinkit data repository.

---

## 1. Table: `blinkit_orders_cleaned.csv`
- **Total Rows**: 4,538
- **Primary Key**: `order_id`
- **Foreign Keys**: `customer_id` -> `blinkit_customers_cleaned.csv`
- **Temporal Span**: 2023-03-16 to 2024-11-04 (600 consecutive calendar days)

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `int64` | 0 | 4,538 | Unique identifier for the customer order. |
| `customer_id` | `int64` | 0 | 1,974 | Identifier of the customer placing the order. |
| `order_date` | `string (datetime)` | 0 | 4,538 | Order timestamp (YYYY-MM-DD HH:MM:SS). |
| `promised_delivery_time` | `string (datetime)` | 0 | 4,538 | Target delivery timestamp based on 10-15 min SLA. |
| `actual_delivery_time` | `string (datetime)` | 0 | 4,538 | Doorstep delivery timestamp. |
| `delivery_status` | `string (categorical)`| 0 | 3 | Status: 'On Time' (3,160), 'Slightly Delayed' (935), 'Significantly Delayed' (443). |
| `order_total` | `float64` | 0 | 4,154 | Total basket amount in INR. Mean: ₹2,209.07. |
| `payment_method` | `string (categorical)`| 0 | 4 | Payment mode: 'Cash', 'Card', 'UPI', 'Wallet'. |
| `delivery_partner_id` | `int64` | 0 | 4,538 | Pseudo-identifier (100% unique per row, synthetic artifact). |
| `store_id` | `int64` | 0 | 4,538 | Pseudo-identifier (100% unique per row, synthetic artifact). |
| `delivery_delay_minutes` | `float64` | 0 | 36 | Difference in minutes between actual and promised delivery time. |

---

## 2. Table: `blinkit_customers_cleaned.csv`
- **Total Rows**: 2,277
- **Primary Key**: `customer_id`

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `int64` | 0 | 2,277 | Unique customer identifier. |
| `customer_name` | `string` | 0 | 2,269 | Customer full name. |
| `email` | `string` | 0 | 2,274 | Customer email address. |
| `phone` | `int64` | 0 | 2,277 | Contact phone number (+91). |
| `address` | `string` | 0 | 2,277 | Street address text. |
| `area` | `string` | 0 | 316 | Urban municipality / city in India. |
| `pincode` | `int64` | 0 | 2,271 | 6-digit Indian Postal PIN code. |
| `registration_date` | `string (datetime)` | 0 | 587 | Customer sign-up date. |
| `customer_segment` | `string (categorical)`| 0 | 4 | Segment: 'Regular', 'Premium', 'New', 'Inactive'. |
| `total_orders` | `int64` | 0 | 20 | Lifetime order count (1 to 20). |
| `avg_order_value` | `float64` | 0 | 2,265 | Customer historical AOV in INR. |

---

## 3. Table: `blinkit_products_cleaned.csv`
- **Total Rows**: 268
- **Primary Key**: `product_id`

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | `int64` | 0 | 268 | Unique product identifier. |
| `product_name` | `string` | 0 | 51 | Item name (e.g., Onions, Milk, Shampoo). |
| `category` | `string (categorical)`| 0 | 11 | Department (e.g., Dairy & Breakfast, Snacks & Munchies). |
| `brand` | `string` | 0 | 267 | Brand manufacturer. |
| `price` | `float64` | 0 | 267 | Selling price to customer (INR). |
| `mrp` | `float64` | 0 | 268 | Maximum Retail Price (INR). |
| `margin_percentage` | `float64` | 0 | 6 | Gross margin: strictly ((mrp - price)/mrp)*100. |
| `shelf_life_days` | `int64` | 0 | 5 | Shelf life (3, 7, 30, 90, 180 days). |
| `min_stock_level` | `int64` | 0 | 21 | Reorder safety stock threshold. |
| `max_stock_level` | `int64` | 0 | 51 | Dark store holding capacity. |

---

## 4. Table: `blinkit_order_items_cleaned.csv`
- **Total Rows**: 4,538
- **Primary Key**: `order_id` (1-to-1 relationship with orders)
- **Foreign Keys**: `order_id` -> `orders`, `product_id` -> `products`

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `int64` | 0 | 4,538 | Associated order identifier. |
| `product_id` | `int64` | 0 | 268 | Purchased product item identifier. |
| `quantity` | `int64` | 0 | 3 | Units ordered (1, 2, or 3). |
| `unit_price` | `float64` | 0 | 267 | Unit selling price at transaction. |

---

## 5. Table: `blinkit_customer_feedback_cleaned.csv`
- **Total Rows**: 4,538
- **Primary Key**: `feedback_id`
- **Foreign Keys**: `order_id` -> `orders`, `customer_id` -> `customers`

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `feedback_id` | `int64` | 0 | 4,538 | Unique feedback record identifier. |
| `order_id` | `int64` | 0 | 4,538 | Order linked to feedback. |
| `customer_id` | `int64` | 0 | 1,974 | Reviewing customer (redundant with orders). |
| `rating` | `int64` | 0 | 5 | Customer star rating (1 to 5). |
| `feedback_text` | `string` | 0 | 25 | Customer comment text (25 discrete templates). |
| `feedback_category` | `string (categorical)`| 0 | 4 | 'App Experience', 'Customer Service', 'Delivery', 'Product Quality'. |
| `sentiment` | `string (categorical)`| 0 | 3 | 'Negative', 'Neutral', 'Positive'. |
| `feedback_date` | `string (datetime)` | 0 | 600 | Review submission date. |

---

## 6. Table: `blinkit_marketing_performance_cleaned.csv`
- **Total Rows**: 5,400
- **Primary Key**: `campaign_id`

| Column Name | Data Type | Null Count | Unique Values | Description & Integrity Notes |
| :--- | :--- | :--- | :--- | :--- |
| `campaign_id` | `int64` | 0 | 5,400 | Unique ad run record identifier. |
| `campaign_name` | `string` | 0 | 9 | Campaign creative (e.g. Flash Sale, Festival Offer). |
| `date` | `string (datetime)` | 0 | 600 | Date of campaign execution. |
| `target_audience` | `string` | 0 | 4 | Audience segment: 'Regular', 'Premium', 'New', 'Inactive'. |
| `channel` | `string` | 0 | 4 | Delivery channel: 'App', 'Email', 'SMS', 'Social Media'. |
| `impressions` | `int64` | 0 | 4,058 | Total campaign ad views. |
| `clicks` | `int64` | 0 | 899 | Total click-throughs. |
| `conversions` | `int64` | 0 | 91 | Attributed checkout conversions. |
| `spend` | `float64` | 0 | 5,356 | Media ad spend in INR. |
| `revenue_generated` | `float64` | 0 | 5,386 | Attributed gross revenue in INR. |
| `roas` | `float64` | 0 | 251 | Return on Ad Spend metric. |
