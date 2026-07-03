from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CURATED_DIR = DATA_DIR / "curated"
ANALYTICS_DIR = DATA_DIR / "analytics"

GREEN_TAXI_2024_01_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    "green_tripdata_2024-01.parquet"
)

GREEN_TAXI_RAW_FILE = RAW_DIR / "green_tripdata_2024-01.parquet"
GREEN_TAXI_CURATED_OUTPUT = CURATED_DIR / "green_taxi_trips_2024_01"

TRIPS_BY_PICKUP_HOUR_OUTPUT = ANALYTICS_DIR / "trips_by_pickup_hour"
PAYMENT_TYPE_SUMMARY_OUTPUT = ANALYTICS_DIR / "payment_type_summary"


def ensure_data_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CURATED_DIR.mkdir(parents=True, exist_ok=True)
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)