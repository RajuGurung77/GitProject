from pyspark.sql import SparkSession

from util import word_count, data_frame_with_enforced_schema

if __name__ == '__main__':

    spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
    #word_count(spark,"file:///home/takeo/test.txt")
    word_count(spark, "file:///home/takeo/test1.txt")

    data_frame_with_enforced_schema(spark)
