from pyspark.sql import SparkSession

from car_util import df_car_power_functions

if __name__ == '__main__':
	spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

	df_car_power_functions(spark)

