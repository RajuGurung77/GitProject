from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri", "mongodb+srv://admin:Admin123@cluster0.opnsreg.mongodb.net/sampleDB.mycol").load()
#df.show()
df.select("title","by").show()