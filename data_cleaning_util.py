def df_all_records(spark):
	data = [
		("Smith", 23, 5.3),
		("Rashmi", 27, 5.8),
		("Smith", 23, 5.3),
		("Payal", 27, 5.8),
		("Megha", 27, 5.4)
	]

	columns = ["Name", "Age", "Height"]
#Step 1: Create df and show all records
	df = spark.createDataFrame(data, columns)
	##show All records
	print("====Showing all records=========")
	df.show()
	df.createOrReplaceTempView("customers")
	return df

#Step 2: Remove exact duplicate rows using SQL DISTINCT.
def df_no_duplicates(spark):
	print("=== After Removing Exact Duplicates ===")
	df_no_dupes = spark.sql("SELECT DISTINCT Name, Age, Height FROM customers")
	df_no_dupes.show()
	df_no_dupes.createOrReplaceTempView("customers_no_dups")
	return df_no_dupes

def df_unique_height_age(spark):
	print("=== After Removing Row with duplicate height and age ===")
	df_unique=spark.sql("""SELECT cnd.Name,cnd.Age,cnd.Height FROM customers_no_dups cnd 
	                    JOIN (SELECT height,age, count(*) from customers_no_dups 
	                          group by height,age having count(*)=1) dc on dc.age=cnd.age and dc.height=cnd.height""")
	df_unique.show()
	return df_unique
