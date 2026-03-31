import os

import os
from pyspark.sql import SparkSession, functions as F

BUCKET = "covid19-takeo"
BRONZE = f"s3a://{BUCKET}/covid/bronze"
SILVER = f"s3a://{BUCKET}/covid/silver"

spark = SparkSession.builder.appName("covid-minimal-silver").getOrCreate()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", access_key)
hadoop_conf.set("fs.s3a.secret.key", secret_key)
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

# df = spark.read.csv("s3a://covid19-takeo/enigma-jhu/Enigma-JHU.csv.gz", header=True, inferSchema=True)
# df.show()

# Helpers
upper_trim = lambda c: F.upper(F.trim(F.col(c)))
to_date = lambda c: F.to_date(F.col(c).cast("string"))

# --- Lookups ---
states = (spark.read.option("header", True).csv(f"{BRONZE}/static-datasets/state-abv/states_abv.csv")
          .select(upper_trim("Abbreviation").alias("state_code"), F.initcap("State").alias("state_name")))

# --- Cases (NYT state file: date,state,cases,deaths or JHU state-level variant) ---
cases_raw = spark.read.option("header", True).csv(f"{BRONZE}/enigma-nytimes-data-in-usa/us-states/us_states.csv")

cases_std = (cases_raw
  # Handle date formats like "2020-05-01" or yyyymmdd; adjust if needed
  .withColumn("full_date", F.to_date("date"))
  # If the file stores state NAME, map to code; if it already stores code, this join still works
  .withColumn("state_name_raw", F.initcap(F.col("state")))
  .join(states, states.state_name == F.col("state_name_raw"), "left")
  .withColumn("cases_cum", F.col("cases").cast("long"))
  .withColumn("deaths_cum", F.col("deaths").cast("long"))
  .withColumn("year", F.year("full_date"))
  .withColumn("month", F.month("full_date"))
  .withColumn("day", F.dayofmonth("full_date"))
  .select("full_date", "state_code", "state_name", "cases_cum", "deaths_cum", "year", "month", "day")
  .dropna(subset=["full_date", "state_code"])
)

(cases_std.write.mode("overwrite")
  .partitionBy("state_code", "year", "month", "day")
  .parquet(f"{SILVER}/cases_standardized"))

