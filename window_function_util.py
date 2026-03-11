from pyspark.sql import Window
from pyspark.sql.functions import row_number, rank, dense_rank, lag, lead


def df_simpledata(spark):

    simpleData = (
        ("James", "Sales", 3000),
        ("Michael", "Sales", 4600),
        ("Robert", "Sales", 4100),
        ("Maria", "Finance", 3000),
        ("James", "Sales", 3000),
        ("Scott", "Finance", 3300),
        ("Jen", "Finance", 3900),
        ("Jeff", "Marketing", 3000),
        ("Kumar", "Marketing", 2000),
        ("Saif", "Sales", 4100)
    )

    columns = ["employee_name", "department", "salary"]

    df = spark.createDataFrame(data=simpleData, schema=columns)

    df.printSchema()
    df.show(truncate=False)

    return df


def df_row_function(df,windowSpec):

    df.withColumn("row_number", row_number().over(windowSpec)).show(truncate=False)

def df_rank(df,windowSpec):

	df.withColumn("rank", rank().over(windowSpec)).show()


def df_dense_rank(df,windowSpec):

    df.withColumn("dense_rank", dense_rank().over(windowSpec)).show()


def df_lag(df,windowSpec):
	df.withColumn("lag", lag("salary", 2).over(windowSpec)).show()


def df_lead(df,windowSpec):
    df.withColumn("lead", lead("salary", 2).over(windowSpec)).show()