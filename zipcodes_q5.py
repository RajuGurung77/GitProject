from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()

df = spark.read.option("header", True).csv("/data/test/simple_zipcodes.csv")
#df.show()
# Generating 50% sample of data
df_sample = df.sample(fraction=0.5, seed=42)

# Writing as Hive table partitioned by state and city
# Maximum 3 records per file using spark.sql.shuffle.partitions & coalesce
# Using coalesce each partition after repartitioning by state and city
df_sample.repartition("State", "City") \
         .write \
         .mode("overwrite") \
         .option("maxRecordsPerFile", 3) \
         .partitionBy("State", "City") \
         .format("parquet") \
         .saveAsTable("zipcodes_partitioned")

# Running Hive SQL to filter out AL state and SPRINGVILLE city
df_filtered = spark.sql("""SELECT *
    FROM zipcodes_partitioned
    WHERE State != 'AL'
      AND City != 'SPRINGVILLE'""")

df_filtered.show(truncate=False)
