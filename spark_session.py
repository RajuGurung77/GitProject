from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

df = spark.table(".employees")