from pyspark.sql.functions import count, col, when

#Function to count Null values
def check_nulls(df, name):
	print(f"\n Null count for {name}")
	df.select(
		*[count(when(col(c).isNull(), c)).alias(c) for c in df.columns]
	).show()

#Function to check duplicates
def check_duplicates(df, name):
	total = df.count()
	distinct = df.dropDuplicates().count()
	print(f"\n{name} Duplicates: {total-distinct}")

#Function to standardize columns
def standardize_columns(df):
	for col_name in df.columns:
		df= df.withColumnRenamed(col_name, col_name.lower().replace(" ", "_"))
	return df