from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

spark = SparkSession.builder \
    .appName("YoutubeAssignment") \
    .config("spark.mongodb.read.connection.uri", "mongodb://localhost:27017/mydb.youtube") \
    .getOrCreate()

df = spark.read \
    .format("mongodb") \
    .load()

df2 = df.withColumn("item", explode("items"))

filtered_df = df2.filter(
    col("item.id.channelId") == "UCJowOS1R0FnhipXVqEnYU1A"
)

result = filtered_df.select("regionCode")

result.show()
spark.stop()