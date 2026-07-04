# PySpark Data Pipeline Demo

A small data engineering portfolio project using **PySpark**, **JupyterLab**, **Docker** and **Parquet**.

The project demonstrates a reproducible local Spark environment and a simple batch data pipeline for processing public taxi trip data.

## Project Goal

The goal of this project is to show the core steps of a small data engineering workflow:

```text
Public Parquet Dataset
        |
        v
PySpark Notebook
        |
        v
Data Quality Checks
        |
        v
Cleaning and Feature Engineering
        |
        v
Curated Parquet Output
        |
        v
Spark SQL Analytics
```

This project is intentionally kept small and reproducible. It focuses on clean infrastructure, readable notebooks and basic Spark transformations instead of a large production-like architecture.

## Tech Stack

* Python
* PySpark
* JupyterLab
* Docker / Docker Compose
* Parquet
* Spark SQL
* Streamlit

## Dataset

The current pipeline uses the **NYC TLC Green Taxi Trip Records** dataset for January 2024.

The dataset contains taxi trip records with fields such as pickup and drop-off timestamps, trip distance, fare amounts, payment type, passenger count and location IDs.

The raw data is downloaded locally into:

```text
data/raw/
```

Generated curated output is written to:

```text
data/curated/
```

Aggregated analytical outputs are written to:

```text
data/analytics/
```

These data folders are excluded from Git tracking because raw, processed and aggregated data files can become large.

## Current Features

* Dockerized JupyterLab environment
* Local PySpark setup
* Public Parquet dataset download
* Spark-based Parquet loading
* Schema inspection
* Basic data quality checks
* Filtering of invalid or implausible records
* Feature engineering:

  * trip duration in minutes
  * pickup date
  * pickup hour
  * tip percentage
* Curated Parquet output
* Spark SQL analytics
* Reusable transformation logic in Python modules
* Basic pytest-based unit tests for Spark transformations
* Clear separation of raw, curated and analytics data layers
* Streamlit dashboard for visualizing analytical outputs

## Project Structure

```text
pyspark-data-pipeline-demo/
├── app/
    └── streamlit_app.py
├── data/
│   ├── raw/                 # Raw local data, ignored by Git
│   ├── curated/             # Cleaned and enriched data, ignored by Git
│   └── analytics/           # Aggregated analytical outputs, ignored by Git
│
├── notebooks/
│   ├── 01_infrastructure_test.ipynb
│   └── 02_load_public_dataset.ipynb
│
├── src/
│   └── pipeline/
│       ├── __init__.py
│       ├── config.py              # Central project paths and dataset configuration
│       ├── transformations.py     # Cleaning and feature engineering logic
│       └── analytics.py           # Reusable aggregation logic
│
├── tests/
│   ├── conftest.py
│   └── test_transformations.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Notebooks

### 01 Infrastructure Test

Validates that the Dockerized PySpark environment works correctly.

It tests:

* Spark session creation
* simple Spark DataFrame creation
* basic transformation
* Parquet write/read roundtrip

### 02 Load Public Dataset

Implements the first small batch data pipeline.

It performs:

* download of a public Parquet dataset
* loading with Spark
* schema inspection
* basic data quality checks
* cleaning and feature engineering
* writing curated Parquet output
* Spark SQL queries on the cleaned data

## How to Run

### 1. Start the Docker Container

From the project root:

```bash
docker compose up --build
```

### 2. Open JupyterLab

Open this URL in your browser:

```text
http://localhost:8888
```

### 3. Run the Notebooks

Run the notebooks in this order:

```text
notebooks/01_infrastructure_test.ipynb
notebooks/02_load_public_dataset.ipynb
```

### 4. Run Tests

After the container is running, execute:

```bash
docker compose exec jupyter pytest -q
```

### Open Streamlit Dashboard

After running the pipeline notebook, open:

```text
http://localhost:8501
```

## Example Data Quality Checks

The pipeline inspects numerical columns such as:

* passenger count
* trip distance
* fare amount
* tip amount
* total amount

The raw dataset contains invalid or implausible records, for example:

* zero-distance trips
* negative fare amounts
* negative total amounts
* extreme outliers
* missing passenger counts

These records are filtered during the cleaning step.

## Example Spark SQL Analysis

After cleaning, the curated dataset is registered as a temporary Spark SQL view.

Example analytical questions:

* How many trips occur by pickup hour?
* What is the average trip distance by hour?
* What is the average total amount by payment type?
* How does the average tip percentage vary by payment type?

## Current Status

* [x] Dockerized PySpark environment
* [x] JupyterLab setup
* [x] Infrastructure test notebook
* [x] Public Parquet dataset pipeline
* [x] Basic data quality checks
* [x] Curated Parquet output
* [x] Spark SQL analytics
* [x] Move reusable transformations into `src/`
* [x] Add automated tests for transformation logic
* [ ] Add PostgreSQL as an optional target
* [x] Add a small dashboard or summary report

## Roadmap

### Version 1: Notebook-Based Batch Pipeline

* Dockerized PySpark environment
* Public dataset loading
* Data quality checks
* Cleaning and feature engineering
* Curated Parquet output
* Spark SQL analytics

### Version 2: Modular Pipeline

* Move transformation logic from notebook to Python modules
* Add unit tests
* Improve configuration handling
* Add clearer separation between raw, curated and analytical layers

### Version 3: Streamlit Dashboard

* Add dashboard app
* Read curated and analytics Parquet outputs
* Show KPIs and charts
* Extend Docker Compose with Streamlit service

### Version 4: Optional Extensions

Possible future extensions:

* PostgreSQL export
* additional datasets
* orchestration with Airflow or Prefect
* Azure storage / Databricks architecture documentation

## Notes

This is a portfolio project and not a production system.

The focus is on demonstrating practical data engineering skills with a small, reproducible PySpark pipeline.
