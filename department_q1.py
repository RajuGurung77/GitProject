from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()
df = spark.read.csv("/data/test/department.txt",
    schema="dept_name STRING, dept_id INT, salary LONG"
)
df.show()

df2 = df.withColumn("doubleSalary", col("salary") * 2)
df2.show()

#  Write DataFrame to parquet file
df2.write.mode("overwrite").format("parquet").saveAsTable("department_hive_parquet")
