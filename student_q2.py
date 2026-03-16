from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()
# Read JSON file from HDFS
df = spark.read.json("/data/test/student.json")
#df.show()
df.createOrReplaceTempView("students")

# SQL to select first name and gender of students learning Java and not from OH
result = spark.sql("""SELECT name.firstname AS firstname, gender
    FROM students
    WHERE array_contains(languages, 'Java')
      AND state != 'OH'""")

result.show()