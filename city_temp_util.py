from pyspark.sql.types import StructType, StringType, StructField, DoubleType


def df_process_temp(spark):
	# Sample data
	data = [
		("New York", 10.0),
		("New York", 12.0),
		("Los Angeles", 20.0),
		("Los Angeles", 22.0),
		("San Francisco", 15.0),
		("San Francisco", 18.0)
	]

	# Define schema
	schema = StructType([
		StructField("city", StringType(), True),
		StructField("temperature", DoubleType(), True)
	])

	# Create DataFrame
	df = spark.createDataFrame(data, schema)
	# Create temporary views
	df.createOrReplaceTempView("temp_data")
	# Show the output
	df.show(truncate=False)

	# Compute total_temperature


	df_total = spark.sql("""
                     SELECT city, SUM(temperature) AS total_temperature
                     FROM temp_data
                     GROUP BY city
                     """)
	df_total.createOrReplaceTempView("total_temp")

# Compute avg_temperature
	df_avg = spark.sql("""
                   SELECT city, AVG(temperature) AS avg_temperature
                   FROM temp_data
                   GROUP BY city
                   """)
	df_avg.createOrReplaceTempView("avg_temp")

# Compute number of measurements
	df_count = spark.sql("""
                     SELECT city, COUNT(temperature) AS num_measurements
                     FROM temp_data
                     GROUP BY city
                     """)
	df_count.createOrReplaceTempView("count_temp")

# Join using SQL
	df_result = spark.sql("""
                      SELECT t.city, c.num_measurements, t.total_temperature, a.avg_temperature
                      FROM total_temp t
                               JOIN count_temp c ON t.city = c.city
                               JOIN avg_temp a ON t.city = a.city
                      WHERE t.total_temperature > 30
                      ORDER BY t.city ASC
                      """)

	return df_result
