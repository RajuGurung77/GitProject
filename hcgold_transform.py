import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, trim, upper
from hcsilver_clean_util import standardize_columns

BUCKET = "raju-capstone-healthcare"
BRONZE = f"s3a://{BUCKET}/bronze-healthcare"
SILVER = f"s3a://{BUCKET}/silver-healthcare/clean_data"
GOLD = f"s3a://{BUCKET}/gold-healthcare"

spark = SparkSession.builder \
    .appName("Healthcare-Gold-Transform") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
    .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .getOrCreate()

# Load
patient_df = spark.read.parquet(f"{SILVER}/patient/")
subscriber_df = spark.read.parquet(f"{SILVER}/subscriber/")
grpsubgrp_df = spark.read.parquet(f"{SILVER}/grpsubgrp/")
claims_df = spark.read.parquet(f"{SILVER}/claims/")

group_df = spark.read.option("header", True).csv(f"{BRONZE}/group.csv")
disease_df = spark.read.option("header", True).csv(f"{BRONZE}/disease.csv")
hospital_df = spark.read.option("header", True).csv(f"{BRONZE}/hospital.csv")
subgroup_df = spark.read.option("header", True).csv(f"{BRONZE}/subgroup.csv")

group_df = standardize_columns(group_df)
disease_df = standardize_columns(disease_df)
hospital_df = standardize_columns(hospital_df)
subgroup_df = standardize_columns(subgroup_df)

# Normalize keys
patient_df = patient_df.withColumn("hospital_id", upper(trim(col("hospital_id"))))
claims_df = claims_df.withColumn("disease_name", upper(trim(col("disease_name"))))
disease_df = disease_df.withColumn("disease_name", upper(trim(col("disease_name"))))

# Dimensions

dim_patient = patient_df.dropDuplicates()

dim_group = group_df.select(
    col("grp_id"),
    col("grp_name"),
    col("grp_type"),
    col("country"),
    col("city"),
    col("zipcode"),
    col("premium_written").cast("double"),
    col("year").cast("int")
).dropDuplicates()

dim_subgroup = subgroup_df.join(
    grpsubgrp_df, "subgrp_id", "left"
).select("subgrp_id", "grp_id").dropDuplicates()

dim_subscriber = subscriber_df.join(
    grpsubgrp_df, "subgrp_id", "left"
).select(
    "sub_id","first_name","last_name","street","birth_date","gender",
    "phone","country","city","zip_code",
    "subgrp_id","grp_id","elig_ind","eff_date","term_date"
).dropDuplicates()

dim_disease = disease_df.select(
    col("disease_id").cast("bigint"),
    col("disease_name")
).dropDuplicates()

dim_hospital = hospital_df.select(
    col("hospital_id"),
    col("hospital_name"),
    col("city"),
    col("state"),
    col("country")
).dropDuplicates()

# Fact

c = claims_df.alias("c")
d = dim_disease.alias("d")
s = dim_subscriber.alias("s")
p = dim_patient.alias("p")

claims_enriched = c.join(
    d, col("c.disease_name") == col("d.disease_name"), "left"
).join(
    s, col("c.sub_id") == col("s.sub_id"), "left"
).join(
    p, col("c.patient_id") == col("p.patient_id"), "left"
)

fact_claims = claims_enriched.select(
    col("c.claim_id"),
    col("c.patient_id"),
    col("c.sub_id"),
    col("d.disease_id"),
    col("p.hospital_id"),
    col("s.grp_id"),
    col("s.subgrp_id"),
    col("c.claim_amount"),
    col("c.claim_or_rejected").alias("claim_status"),
    col("c.claim_type"),
    col("c.claim_date")
).dropDuplicates()

dim_patient.write.mode("overwrite").parquet(f"{GOLD}/dim_patient/")
dim_subscriber.write.mode("overwrite").parquet(f"{GOLD}/dim_subscriber/")
dim_group.write.mode("overwrite").parquet(f"{GOLD}/dim_group/")
dim_subgroup.write.mode("overwrite").parquet(f"{GOLD}/dim_subgroup/")
dim_disease.write.mode("overwrite").parquet(f"{GOLD}/dim_disease/")
dim_hospital.write.mode("overwrite").parquet(f"{GOLD}/dim_hospital/")
fact_claims.write.mode("overwrite").parquet(f"{GOLD}/fact_claims/")

print("\nGold layer created successfully")