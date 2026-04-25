import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from hcsilver_clean_util import standardize_columns, check_nulls, check_duplicates

BUCKET = "raju-capstone-healthcare"
BRONZE = f"s3a://{BUCKET}/bronze-healthcare"
SILVER = f"s3a://{BUCKET}/silver-healthcare/clean_data"

spark = SparkSession.builder \
    .appName("Healthcare-Silver-Transform") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .getOrCreate()

# Load
patient_df = spark.read.option("header", True).csv(f"{BRONZE}/Patient_records.csv")
subscriber_df = spark.read.option("header", True).csv(f"{BRONZE}/subscriber.csv")
grpsubgrp_df = spark.read.option("header", True).csv(f"{BRONZE}/grpsubgrp.csv")
claims_df = spark.read.json(f"{BRONZE}/claims.json")

# Standardize
patient_df = standardize_columns(patient_df)
subscriber_df = standardize_columns(subscriber_df)
grpsubgrp_df = standardize_columns(grpsubgrp_df)
claims_df = standardize_columns(claims_df)


check_nulls(patient_df, "Patient")
check_nulls(subscriber_df, "Subscriber")
check_nulls(claims_df, "Claims")
check_duplicates(patient_df, "Patient")
check_duplicates(claims_df, "Claims")

patient_df = patient_df.select(
    col("patient_id").cast("bigint"),
    col("patient_name"),
    col("patient_gender"),
    to_date(col("patient_birth_date")).alias("patient_birth_date"),
    col("patient_phone"),
    col("city"),
    col("hospital_id")  # STRING (important)
)

subscriber_df = subscriber_df.select(
    col("sub_id"),  # STRING
    col("first_name"),
    col("last_name"),
    col("street"),
    to_date(col("birth_date")).alias("birth_date"),
    col("gender"),
    col("phone"),
    col("country"),
    col("city"),
    col("zip_code"),
    col("subgrp_id"),
    col("elig_ind"),
    to_date(col("eff_date")).alias("eff_date"),
    to_date(col("term_date")).alias("term_date")
)

grpsubgrp_df = grpsubgrp_df.select(
    col("subgrp_id"),
    col("grp_id")
)

claims_df = claims_df.select(
    col("claim_id").cast("bigint"),
    col("patient_id").cast("bigint"),
    col("sub_id"),
    col("disease_name"),
    col("claim_or_rejected"),
    col("claim_type"),
    col("claim_amount").cast("double"),
    to_date(col("claim_date")).alias("claim_date")
)

patient_df.write.mode("overwrite").parquet(f"{SILVER}/patient/")
subscriber_df.write.mode("overwrite").parquet(f"{SILVER}/subscriber/")
grpsubgrp_df.write.mode("overwrite").parquet(f"{SILVER}/grpsubgrp/")
claims_df.write.mode("overwrite").parquet(f"{SILVER}/claims/")

print("\nSilver layer created successfully")