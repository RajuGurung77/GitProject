from pyspark.sql import SparkSession

if __name__ == '__main__':
	spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").enableHiveSupport().getOrCreate()

	#Create file in local and load it to hdfs using hadoop fs -put $HOME/zipcodes1.csv /data/spark/test
	df=spark.read.csv("/data/spark/test/zipcodes1.csv")
	# df.printSchema()
	# df.show()

	#Write dataframe to hadoop into parquet file
	#df.write.parquet("/data/spark/test/parquet/people.parquet")

	#Read parquet file
	parDf=spark.read.parquet("/data/spark/test/parquet/people.parquet")
	# parDf.show()

	#With headers
	df3 = spark.read.options(header='True', inferSchema='True', delimiter=',').csv("/data/spark/test/zipcodes1.csv")
	#df3.printSchema()

	#write into table
	df3.write.mode("overwrite").saveAsTable("sparkdb.zip_table")

	#Read from created table
	tabDF = spark.sql("select * from sparkdb.zip_table")
	#tabDF.show()

	#for partitioning
	spark.conf.set("hive.exec.dynamic.partition", "true")
	spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")

	df3.write.mode("overwrite").partitionBy("city").saveAsTable("sparkdb.city_part")

	#Check in hive to see the partitions --show partitions city_part;

	#New table creation  as state_city with partitions on state, city. Default hive table file format is parquet
	df3.write.mode("overwrite").partitionBy("state", "city").saveAsTable("sparkdb.state_city")

	#write to partitioned hive table with parquet file format
	df3.write.mode("overwrite").partitionBy("state", "city").format("parquet").saveAsTable("sparkdb.state_city_parquet")

	#Select only city where city is Asheboro
	sdf = spark.sql("select city from sparkdb.state_city_parquet where city='ASHEBORO'")
	# sdf.printSchema()
	sdf.show()

	#select all columns where city is mesa and state is AZ
	sdf = spark.sql("select * from sparkdb.state_city_parquet where city='MESA' and state= 'AZ' ")
	sdf.printSchema()
	sdf.show()

