from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()
df_emp = spark.read.json("/data/test/employee.json")
df_dept = spark.read.json("/data/test/department.json")

df_emp.createOrReplaceTempView("employees")
df_dept.createOrReplaceTempView("departments")

# Using SQL query to join, aggregate, and compute max salary and employee count
df_result = spark.sql("""SELECT 
        d.dept_name,
        MAX(e.salary) AS maxSalary,
        COUNT(e.emp_id) AS employeesCount
    FROM employees e
    JOIN departments d
      ON CAST(e.emp_dept_id AS INT) = d.dept_id
    GROUP BY d.dept_name""")

# Saving result as Hive table partitioned by dept_name in Parquet
df_result.write \
    .mode("overwrite") \
    .format("parquet") \
    .partitionBy("dept_name") \
    .saveAsTable("part_department")
df_result.show()