from pyspark.sql import SparkSession

from city_temp_util import df_process_temp

if __name__ == "__main__":
    # Initialize Spark
    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

    df_process_temp(spark)