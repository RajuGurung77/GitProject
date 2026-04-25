import re
from pyspark.sql.functions import count, col, when

# Check nulls
def check_nulls(df, name):
    print(f"\nNull count for {name}")
    df.select(
        *[count(when(col(c).isNull(), c)).alias(c) for c in df.columns]
    ).show()

# Check duplicates
def check_duplicates(df, name):
    total = df.count()
    distinct = df.dropDuplicates().count()
    print(f"{name} Duplicates: {total - distinct}")

# Standardize column names
def standardize_columns(df):
    for c in df.columns:
        clean = c.strip().lower()
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_")
        df = df.withColumnRenamed(c, clean)
    return df