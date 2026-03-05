from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType

from util import df_with_custom_schema, df_with_nested_schema

if __name__ == '__main__':

    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    df_with_custom_schema(spark)

    df_with_nested_schema(spark)