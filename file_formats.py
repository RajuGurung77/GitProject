from pyspark.sql import SparkSession

if __name__ == '__main__':

	spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

	#df = spark.read.csv("file:///home/takeo/zipcodes.csv")
	#df.printSchema()
	# df2 = spark.read.option("header", True).csv("file:///home/takeo/zipcodes.csv")
	# df4 = spark.read.options(inferSchema='True', delimiter=',') \
	# 	.csv("file:///home/takeo/zipcodes.csv")
	# df3 = spark.read.options(header='True', inferSchema='True', delimiter=',') \
	# 	.csv("file:///home/takeo/zipcodes.csv")
	#df3.printSchema()

	data = [("James ", "", "Smith", "36636", "M", 3000),
	        ("Michael ", "Rose", "", "40288", "M", 4000),
	        ("Robert ", "", "Williams", "42114", "M", 4000),
	        ("Maria ", "Anne", "Jones", "39192", "F", 4000),
	        ("Jen", "Mary", "Brown", "", "F", -1)]
	columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]

	df = spark.createDataFrame(data, columns)
	df.write.mode("overwrite").parquet("file:///tmp/output/people.parquet")
	parDF = spark.read.parquet("file:///tmp/output/people.parquet")
	parDF.createOrReplaceTempView("ParquetTable")
	sparkSQL = spark.sql("select * from ParquetTable where salary >= 4000 ")
	sparkSQL.show()
