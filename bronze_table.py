from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()

def bronze_ingestion(csv_path, table_name):
	df=(
		spark.read.option("header","true").csv(csv_path)
	)
	(
		df.write.mode("overwrite").format("parquet").saveAsTable(f"iphone_analytics.bronze_{table_name}")
	)
bronze_ingestion("/data/iphone/raw/customers.csv", "customer")
bronze_ingestion("/data/iphone/raw/products.csv", "product")
bronze_ingestion("/data/iphone/raw/stores.csv", "store")
bronze_ingestion("/data/iphone/raw/sales.csv", "sale")



