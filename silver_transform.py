from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()
spark.sql("Use iphone_analytics")
sales = spark.table("bronze_sale")
silver_sales = (
	sales
	.withColumn("sale_id", col("sale_id").cast("int"))
	.withColumn("product_id", col("product_id").cast("int"))
	.withColumn("customer_id",col("customer_id").cast("int"))
	.withColumn("store_id",col("store_id").cast("int"))
	.withColumn("quantity",col("quantity").cast("int"))
	.withColumn("sale_date", to_date(col("sale_date")))
)
(
	silver_sales.write.mode("overwrite").partitionBy("sale_date").format("parquet").saveAsTable("silver_sale")
)

#Customers
spark.table("bronze_customer").write.mode("overwrite").format("parquet").saveAsTable("silver_customer")

#Products
spark.table("bronze_product").write.mode("overwrite").format("parquet").saveAsTable("silver_product")

#Stores
spark.table("bronze_store").write.mode("overwrite").format("parquet").saveAsTable("silver_store")
