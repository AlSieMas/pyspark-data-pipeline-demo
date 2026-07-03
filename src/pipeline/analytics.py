from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def trips_by_pickup_hour(df: DataFrame) -> DataFrame:
    """
    Aggregate trip metrics by pickup hour.
    """
    return (
        df.groupBy("pickup_hour")
        .agg(
            F.count("*").alias("trip_count"),
            F.round(F.avg("trip_distance"), 2).alias("avg_trip_distance"),
            F.round(F.avg("total_amount"), 2).alias("avg_total_amount"),
            F.round(F.avg("tip_percentage"), 2).alias("avg_tip_percentage"),
        )
        .orderBy("pickup_hour")
    )


def payment_type_summary(df: DataFrame) -> DataFrame:
    """
    Aggregate trip metrics by payment type.
    """
    return (
        df.groupBy("payment_type")
        .agg(
            F.count("*").alias("trip_count"),
            F.round(F.avg("total_amount"), 2).alias("avg_total_amount"),
            F.round(F.avg("tip_percentage"), 2).alias("avg_tip_percentage"),
        )
        .orderBy(F.col("trip_count").desc())
    )