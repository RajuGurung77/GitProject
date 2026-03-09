from pyspark.sql import SparkSession

from data_cleaning_util import df_all_records, df_no_duplicates, df_unique_height_age

if __name__ == '__main__':
	spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

	df=df_all_records(spark)


	df_no_duplicates(spark)

	df_unique_height_age(spark)