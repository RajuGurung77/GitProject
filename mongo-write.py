from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SalesToMongoDB") \
    .config("spark.mongodb.write.connection.uri", "mongodb://localhost:27017/mydb.sales") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("file:///home/takeo/sales/sales.csv")

df.show()
df.write \
    .format("mongodb") \
    .mode("overwrite") \
    .save()


spark.stop()