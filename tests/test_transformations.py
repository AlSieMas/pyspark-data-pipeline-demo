from datetime import datetime

from pipeline.transformations import clean_green_taxi_trips


def test_clean_green_taxi_trips_filters_invalid_records(spark):
    input_data = [
        # valid row
        (
            2,
            datetime(2024, 1, 1, 10, 0, 0),
            datetime(2024, 1, 1, 10, 30, 0),
            "N",
            1,
            75,
            236,
            1,
            3.5,
            18.0,
            3.0,
            24.0,
            1,
            1,
        ),
        # invalid: zero distance
        (
            2,
            datetime(2024, 1, 1, 11, 0, 0),
            datetime(2024, 1, 1, 11, 15, 0),
            "N",
            1,
            75,
            236,
            1,
            0.0,
            12.0,
            2.0,
            16.0,
            1,
            1,
        ),
        # invalid: negative fare
        (
            2,
            datetime(2024, 1, 1, 12, 0, 0),
            datetime(2024, 1, 1, 12, 20, 0),
            "N",
            1,
            75,
            236,
            1,
            2.0,
            -5.0,
            0.0,
            10.0,
            1,
            1,
        ),
        # invalid: duration too short
        (
            2,
            datetime(2024, 1, 1, 13, 0, 0),
            datetime(2024, 1, 1, 13, 0, 30),
            "N",
            1,
            75,
            236,
            1,
            2.0,
            10.0,
            1.0,
            13.0,
            1,
            1,
        ),
    ]

    columns = [
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

    df_input = spark.createDataFrame(input_data, columns)

    df_result = clean_green_taxi_trips(df_input)

    result_rows = df_result.collect()

    assert len(result_rows) == 1

    row = result_rows[0]

    assert row.trip_distance == 3.5
    assert row.fare_amount == 18.0
    assert row.total_amount == 24.0
    assert row.trip_duration_minutes == 30.0
    assert row.pickup_hour == 10
    assert row.tip_percentage == 16.67


def test_clean_green_taxi_trips_adds_expected_columns(spark):
    input_data = [
        (
            2,
            datetime(2024, 1, 1, 10, 0, 0),
            datetime(2024, 1, 1, 10, 30, 0),
            "N",
            1,
            75,
            236,
            1,
            3.5,
            18.0,
            3.0,
            24.0,
            1,
            1,
        )
    ]

    columns = [
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

    df_input = spark.createDataFrame(input_data, columns)

    df_result = clean_green_taxi_trips(df_input)

    assert "trip_duration_minutes" in df_result.columns
    assert "pickup_date" in df_result.columns
    assert "pickup_hour" in df_result.columns
    assert "tip_percentage" in df_result.columns