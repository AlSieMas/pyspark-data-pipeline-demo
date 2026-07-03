from pyspark.sql import DataFrame
from pyspark.sql import functions as F


GREEN_TAXI_COLUMNS = [
    "VendorID",
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "store_and_fwd_flag",
    "RatecodeID",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
    "payment_type",
    "trip_type",
]


def select_green_taxi_columns(df: DataFrame) -> DataFrame:
    """
    Select the columns used by the pipeline from the raw Green Taxi dataset.
    """
    return df.select(*GREEN_TAXI_COLUMNS)


def add_trip_features(df: DataFrame) -> DataFrame:
    """
    Add derived trip features used for downstream analytics.
    """
    return (
        df.withColumn(
            "trip_duration_minutes",
            (
                F.unix_timestamp("lpep_dropoff_datetime")
                - F.unix_timestamp("lpep_pickup_datetime")
            )
            / 60,
        )
        .withColumn("pickup_date", F.to_date("lpep_pickup_datetime"))
        .withColumn("pickup_hour", F.hour("lpep_pickup_datetime"))
        .withColumn(
            "tip_percentage",
            F.when(
                F.col("fare_amount") > 0,
                F.round((F.col("tip_amount") / F.col("fare_amount")) * 100, 2),
            ).otherwise(None),
        )
    )


def clean_green_taxi_trips(df: DataFrame) -> DataFrame:
    """
    Remove invalid or implausible records from the Green Taxi dataset.

    The cleaning rules are intentionally simple and transparent:
    - trip distance must be positive
    - fare amount must be positive
    - total amount must be positive
    - trip duration must be between 1 minute and 4 hours
    """
    df_with_features = add_trip_features(df)

    return (
        df_with_features.filter(F.col("trip_distance") > 0)
        .filter(F.col("fare_amount") > 0)
        .filter(F.col("total_amount") > 0)
        .filter(F.col("trip_duration_minutes").between(1, 240))
    )