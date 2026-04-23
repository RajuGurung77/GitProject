from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col

from hcsilver_clean_util import check_nulls, check_duplicates, standardize_columns

BUCKET='raju-capstone-healthcare'
BRONZE=f's3a://{BUCKET}/bronze-healthcare'
SILVER=f's3a://{BUCKET}/silver-healthcare/clean_data'

spark = SparkSession.builder.appName("Healthcare-DataCleaning").getOrCreate()

#load data from s3
patient_df=spark.read.option("header", True).csv(f"{BRONZE}/Patient_records.csv")
subscriber_df=spark.read.option("header", True).csv(f"{BRONZE}/subscriber.csv")
grpsubgrp_df= spark.read.option("header", True).csv(f"{BRONZE}/grpsubgrp.csv")
claims_df= spark.read.json(f"{BRONZE}/claims.json")

#patient_df.show()

#Check Nulls
check_nulls(patient_df,"Patient")
check_nulls(subscriber_df,"Subscriber")
check_nulls(grpsubgrp_df, "GroupSubgroup")
check_nulls(claims_df,"Claim")

#Replace Null with NA
patient_df_clean= patient_df.fillna("NA")
subscriber_df_clean = subscriber_df.fillna("NA")
grpsubgrp_df_clean = grpsubgrp_df.fillna("NA")
claims_df_clean = claims_df.fillna("NA")

#Check Duplicate Records
check_duplicates(patient_df_clean, "Patient")
check_duplicates(subscriber_df_clean, "Subscriber")
check_duplicates(grpsubgrp_df_clean, "GroupSubgroup")
check_duplicates(claims_df_clean, "Claims")

#Remove Duplicates
patient_df_clean= patient_df_clean.dropDuplicates()
subscriber_df_clean =subscriber_df_clean.dropDuplicates()
grpsubgrp_df_clean =grpsubgrp_df_clean.dropDuplicates()
claims_df_clean =claims_df_clean.dropDuplicates()


#Standardize column names (lower case)
patient_df_clean = standardize_columns(patient_df_clean)
subscriber_df_clean = standardize_columns(subscriber_df_clean)
grpsubgrp_df_clean = standardize_columns(grpsubgrp_df_clean)
claims_df_clean = standardize_columns(claims_df_clean)

#Convert data type
patient_df_clean= patient_df_clean.withColumn("patient_id", col("patient_id").cast("long"))
patient_df_clean = patient_df_clean.withColumn("patient_birth_date", to_date(col("patient_birth_date")))
subscriber_df_clean = subscriber_df_clean.withColumn("birth_date", to_date(col("birth_date")))
claims_df_clean =claims_df_clean.withColumn("claim_date", to_date(col("claim_date")))

claims_df_clean = claims_df_clean \
                   .withColumnRenamed("Claim_Or_Rejected", "claim_status") \
                   .withColumn("claim_amount", col("claim_amount").cast("double"))

patient_df_clean.write.mode("overwrite").parquet(f"{SILVER}/patient/")
subscriber_df_clean.write.mode("overwrite").parquet(f"{SILVER}/subscriber/")
grpsubgrp_df_clean.write.mode("overwrite").parquet(f"{SILVER}/grpsubgrp/")
claims_df_clean.write.mode("overwrite").parquet(f"{SILVER}/claims/")

print("\n Data Cleaned Successfully")





