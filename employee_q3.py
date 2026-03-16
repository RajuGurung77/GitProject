from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
# Read json file from HDFS
df = spark.read.json("/data/test/employee_spark.json")
#df.show()

# Removing duplicate employees
df_distinct = df.dropDuplicates(["employee_name"])

# writing to ORC file partitioned by department
df_distinct.write.mode("overwrite") \
    .partitionBy("department") \
    .format("orc") \
    .save("/data/hive/warehouse/practice.db/employee_orc")

 # finding mean salary per department and order descending
df_mean = df.groupBy("department") \
    .agg(avg("salary").alias("mean_salary")) \
    .orderBy(col("mean_salary").desc())
df_mean.show()
