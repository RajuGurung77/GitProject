from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()
spark.sql("use iphone_analytics")
sales = spark.table("silver_sale")
products = spark.table("silver_product")
fact_df = (
	sales.join(products, "product_id")
	.withColumn("total_amount", col("quantity") * col("unit_price"))
	.select("sale_id", "customer_id", "product_id", "store_id", col("sale_date").alias("date_key"),
	        "quantity",
	        "total_amount"
	        )
)

(
	fact_df.write.mode("overwrite").partitionBy("date_key").format("parquet").saveAsTable("fact_sale")
)
