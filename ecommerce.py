from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("E-Commerce Analysis").getOrCreate()

# Sample data
data = [
	(1, 101, 5001, 'Laptop', 'Electronics', 1000.0, 1),
	(2, 102, 5002, 'Headphones', 'Electronics', 50.0, 2),
	(3, 101, 5003, 'Book', 'Books', 20.0, 3),
	(4, 103, 5004, 'Laptop', 'Electronics', 1000.0, 1),
	(5, 102, 5005, 'Chair', 'Furniture', 150.0, 1)
]

columns = ["transaction_id", "customer_id", "product_id", "product_name", "category", "price", "quantity"]

# Create DataFrame
df = spark.createDataFrame(data, columns)
df.show()

# Filter transactions where quantity is greater than 1
df_filtered = df.filter(df.quantity > 1)
df_filtered.show()

# Filling null values in price column with the average price
average_price = df.selectExpr("avg(price)").collect()[0][0]
df_filled = df.na.fill({"price": average_price})
df_filled.show()

# Drop duplicate rows based on customer_id and product_id
df_no_duplicates = df.dropDuplicates(["customer_id", "product_id"])
df_no_duplicates.show()

# Select specific columns
df_selected = df.select("customer_id", "product_name", "price")
df_selected.show()

# Calculate the total spending per customer
df_grouped = df.groupBy("customer_id").agg({"price": "sum"})
df_grouped.show()

# Assume we have another DataFrame with customer details
customer_data = [
	(101, "John Doe", "john@example.com"),
	(102, "Jane Smith", "jane@example.com"),
	(103, "Alice Johnson", "alice@example.com")
]
customer_columns = ["customer_id", "customer_name", "email"]
df_customers = spark.createDataFrame(customer_data, customer_columns)

# Join on customer_id
df_joined = df.join(df_customers, on="customer_id", how="inner")
df_joined.show()

# Create another DataFrame with similar schema
new_data = [
	(6, 104, 5006, 'Table', 'Furniture', 200.0, 1)
]
df_new = spark.createDataFrame(new_data, columns)

# Union the DataFrames
df_union = df.union(df_new)
df_union.show()

# Create a temporary view
df.createOrReplaceTempView("transactions")

# Run SQL query
sql_result = spark.sql(
	"SELECT customer_id, SUM(price * quantity) as total_spent FROM transactions GROUP BY customer_id")
sql_result.show()

