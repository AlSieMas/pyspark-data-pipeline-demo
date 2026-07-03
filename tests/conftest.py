import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    spark_session = (
        SparkSession.builder
        .master("local[1]")
        .appName("pyspark-data-pipeline-tests")
        .getOrCreate()
    )

    spark_session.sparkContext.setLogLevel("ERROR")

    yield spark_session

    spark_session.stop()