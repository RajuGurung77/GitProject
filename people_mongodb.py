from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

people = spark.createDataFrame([("Bilbo Baggins",  50), ("Gandalf", 1000), ("Thorin", 195), ("Balin", 178), ("Kili", 77),("Dwalin", 169), ("Oin", 167), ("Gloin", 158), ("Fili", 82), ("Bombur", None)], ["name", "age"])
people.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("uri", "mongodb+srv://admin:Admin123@cluster0.opnsreg.mongodb.net/sampleDB.contacts").save()