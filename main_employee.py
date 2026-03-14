from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()
# spark.sql("USE practice")
#
# spark.sql("SHOW TABLES").show()

df = spark.table("practice.employees")
# df.show()

result = spark.sql("""
SELECT department, AVG(salary) as avg_salary
FROM company.employees
GROUP BY department
""")

result.show()
