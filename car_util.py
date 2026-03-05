from pyspark.sql.functions import lit, col
from pyspark.sql.types import IntegerType, StructType, StructField, StringType

def df_car_power_functions(spark):
	data = [("Ford Torino", 140, 3449, "US"),
	        ("Chevrolet Monte Carlo", 150, 3761, "US"),
	        ("BMW 2002", 113, 2234, "Europe")
	        ]
	schema = StructType([
		StructField('carr', StringType(), True),
		StructField('horsepower', IntegerType(), True),
		StructField('weight', IntegerType(), True),
		StructField('origin', StringType(), True)
	])

	df= spark.createDataFrame(data=data, schema=schema)
	df.printSchema()
	df.show()

	##Adding column with constant value
	df1=df.withColumn("AvgWeight", lit(200))
	df1.show()

	##Adding column with kilowatt power * 1000 times hp
	df2=df.withColumn(("kilowatt_power"), col("horsepower") * 1000)
	df2.show()

	##Rename column carr to car
	df3=df.withColumnRenamed("carr", "car")
	df3.show()