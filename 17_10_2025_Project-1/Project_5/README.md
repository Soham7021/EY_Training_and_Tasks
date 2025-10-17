# Capstone Project 5 — Supply Chain & Logistics Tracking System

## Project Overview
This project simulates a **Supply Chain & Logistics Tracking System** using Python and Pandas.  
It handles products, warehouses, shipments, ETL processing, analytics, logging, and daily summaries — all without a database.

The project is divided into **modular components**, each handling a specific functionality:

- CRUD operations for products and warehouses
- ETL pipeline for shipments
- Queue system for async shipment updates
- Logging & error handling
- Analytics for logistics performance
- Scheduling daily summaries

---

## Folder Structure

Project_5/
├─ data/
│ ├─ products.csv
│ ├─ warehouses.csv
│ ├─ shipments.csv
│ ├─ processed_shipments.csv
│ └─ daily_summaries/
├─ reports/
│ └─ logistics_analytics.csv
├─ modules/
│ ├─ crud_operations/
│ │ └─ run_crud.py
│ ├─ etl_pipeline/
│ │ └─ etl_process.py
│ ├─ queue_system/
│ │ ├─ producer.py
│ │ └─ consumer.py
│ ├─ logging_module/
│ │ └─ shipment_logger.py
│ ├─ analytics/
│ │ └─ logistics_analytics.py
│ └─ scheduler/
│ └─ daily_summary_scheduler.py
└─ README.md


---

## Features / Modules

### 1. CRUD Operations
- Add, update, delete, and fetch products & warehouses
- Python script: `modules/crud_operations/run_crud.py`

### 2. ETL Pipeline
- Joins products, warehouses, and shipments
- Calculates `TotalValue` and `DeliveryDays`
- Generates `processed_shipments.csv`
- Python script: `modules/etl_pipeline/etl_process.py`

### 3. Queue System
- Simulates async shipment updates
- Producer pushes updates, consumer processes them
- Python scripts: `modules/queue_system/producer.py`, `consumer.py`

### 4. Logging & Error Handling
- Logs shipment dispatch/delivery events
- Logs errors for missing ProductID or WarehouseID
- Logs processing time for each shipment batch
- Python script: `modules/logging_module/shipment_logger.py`

### 5. Analytics
- Calculates:
  - Average delivery time per warehouse
  - Total shipment value per product category
  - Number of shipments per month
  - Late deliveries (`DeliveryDays > 5`)
- Saves analytics to `reports/logistics_analytics.csv`
- Python script: `modules/analytics/logistics_analytics.py`

### 6. Scheduling
- Generates daily shipment summary CSV: `daily_shipments_YYYYMMDD.csv`
- Scheduled to run at 7:00 AM daily
- Python script: `modules/scheduler/daily_summary_scheduler.py`

---

## How to Run

1. **Activate Virtual Environment**
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install pandas schedule

python modules/crud_operations/run_crud.py

python modules/etl_pipeline/etl_process.py

python modules/queue_system/producer.py
python modules/queue_system/consumer.py

python modules/analytics/logistics_analytics.py

python modules/scheduler/daily_summary_scheduler.py



