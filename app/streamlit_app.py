from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_DIR = PROJECT_ROOT / "data" / "analytics"
CURATED_DIR = PROJECT_ROOT / "data" / "curated"

TRIPS_BY_HOUR_PATH = ANALYTICS_DIR / "trips_by_pickup_hour"
PAYMENT_TYPE_SUMMARY_PATH = ANALYTICS_DIR / "payment_type_summary"
CURATED_TRIPS_PATH = CURATED_DIR / "green_taxi_trips_2024_01"


st.set_page_config(
    page_title="PySpark Taxi Pipeline Dashboard",
    layout="wide",
)


@st.cache_data
def load_parquet_dataset(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


st.title("PySpark Taxi Pipeline Dashboard")

st.markdown(
    """
    This dashboard visualizes the curated and aggregated outputs produced by the
    PySpark batch pipeline.
    """
)


if not TRIPS_BY_HOUR_PATH.exists() or not PAYMENT_TYPE_SUMMARY_PATH.exists():
    st.warning(
        "Analytics data not found. Please run notebooks/02_load_public_dataset.ipynb "
        "first to generate the curated and analytics Parquet outputs."
    )
    st.stop()


trips_by_hour = load_parquet_dataset(TRIPS_BY_HOUR_PATH)
payment_summary = load_parquet_dataset(PAYMENT_TYPE_SUMMARY_PATH)

curated_trips = None
if CURATED_TRIPS_PATH.exists():
    curated_trips = load_parquet_dataset(CURATED_TRIPS_PATH)


st.subheader("Pipeline Output Overview")

col1, col2, col3, col4 = st.columns(4)

total_trips = int(trips_by_hour["trip_count"].sum())
avg_distance = trips_by_hour["avg_trip_distance"].mean()
avg_total_amount = trips_by_hour["avg_total_amount"].mean()
avg_tip_percentage = trips_by_hour["avg_tip_percentage"].mean()

col1.metric("Total trips", f"{total_trips:,}")
col2.metric("Avg. trip distance", f"{avg_distance:.2f} mi")
col3.metric("Avg. total amount", f"${avg_total_amount:.2f}")
col4.metric("Avg. tip percentage", f"{avg_tip_percentage:.2f}%")


st.subheader("Trips by Pickup Hour")

chart_data = trips_by_hour.set_index("pickup_hour")["trip_count"]
st.bar_chart(chart_data)


st.subheader("Average Total Amount by Pickup Hour")

amount_data = trips_by_hour.set_index("pickup_hour")["avg_total_amount"]
st.line_chart(amount_data)


st.subheader("Payment Type Summary")

st.dataframe(payment_summary, use_container_width=True)

payment_chart_data = payment_summary.set_index("payment_type")["trip_count"]
st.bar_chart(payment_chart_data)


if curated_trips is not None:
    st.subheader("Curated Dataset Preview")
    st.dataframe(curated_trips.head(50), use_container_width=True)