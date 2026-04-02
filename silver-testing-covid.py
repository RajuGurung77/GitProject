import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BUCKET = "covid19-takeo"
BRONZE = f"s3a://{BUCKET}/covid/bronze"
SILVER = f"s3a://{BUCKET}/covid/silver"

spark = SparkSession.builder.appName("covid-silver-testing").getOrCreate()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", access_key)
hadoop_conf.set("fs.s3a.secret.key", secret_key)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

print("ACCESS:", os.getenv("AWS_ACCESS_KEY_ID"))
print("SECRET:", os.getenv("AWS_SECRET_ACCESS_KEY"))

def upper_trim(col):
	return F.upper(F.trim(F.col(col)))

states = (spark.read.option("header", True)
          .csv(f"{BRONZE}/static-datasets/state-abv/states_abv.csv")
          .select(
              upper_trim("Abbreviation").alias("state_code"),
              F.initcap("State").alias("state_name")
          ))
# --- Testing (COVID Tracking: date(int yyyymmdd), state(code), positive, negative, totalTestResults) ---
tests_raw = spark.read.option("header", True).csv(f"{BRONZE}/covid_tracking/states_daily.csv")

tests_std = (tests_raw
             .withColumn("full_date", F.to_date(F.col("date").cast("string"), "yyyyMMdd"))
             .withColumn("state_code", upper_trim("state"))
             .join(states.select("state_code", "state_name"), "state_code", "left")
             .withColumn("tests_total_cum", F.col("totalTestResults").cast("long"))
             .withColumn("tests_pos_cum", F.col("positive").cast("long"))
             .withColumn("tests_neg_cum", F.col("negative").cast("long"))
             .withColumn("year", F.year("full_date"))
             .withColumn("month", F.month("full_date"))
             .withColumn("day", F.dayofmonth("full_date"))
             .select("full_date", "state_code", "state_name", "tests_total_cum", "tests_pos_cum", "tests_neg_cum",
                     "year", "month", "day")
             .dropna(subset=["full_date", "state_code"])
             )

(tests_std.write.mode("overwrite")
 .partitionBy("state_code", "year", "month", "day")
 .parquet(f"{SILVER}/testing_standardized"))

print("Silver complete.")
