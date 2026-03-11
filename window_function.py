from pyspark.sql import SparkSession, Window

from window_function_util import df_row_function, df_simpledata, df_rank, df_dense_rank, df_lag, df_lead

spark: SparkSession = SparkSession.builder.master("local[1]").appName("bootcamp.com").getOrCreate()

df=df_simpledata(spark)

windowSpec = Window.partitionBy("department").orderBy("salary")

df_row_function(df, windowSpec)

df_rank(df,windowSpec)

df_dense_rank(df,windowSpec)

df_lag(df,windowSpec)

df_lead(df,windowSpec)
