from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

data = [
	("Alice", 25),
	("Bob", 30),
	("Cathy", 28)
]

# Define columns
columns = ["Name", "Age"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Show data
df.show()

# Print schema
df.printSchema()

# Stop Spark session
spark.stop()