from pyspark.sql.functions import col
from pyspark.sql.types import StructField, StructType, StringType, IntegerType


def word_count(spark,filepath):
    rdd = spark.sparkContext.textFile(filepath)
    rdd2 = rdd.flatMap(lambda x: x.split(" "))
    rdd3 = rdd2.map(lambda x: (x, 1))
    rdd5 = rdd3.reduceByKey(lambda a, b: a + b)
    print(rdd5.collect())

def data_frame_with_enforced_schema(spark):
    data = [("James", "", "Smith", "36636", "M", 3000),
            ("Michael", "Rose", "", "40288", "M", 4000),
            ("Robert", "", "Williams", "42114", "M", 4000),
            ("Maria", "Anne", "Jones", "39192", "F", 4000),
            ("Jen", "Mary", "Brown", "", "F", -1)
            ]

    schema = StructType([ \
        StructField("firstname", StringType(), True), \
        StructField("middlename", StringType(), True), \
        StructField("lastname", StringType(), True), \
        StructField("id", StringType(), True), \
        StructField("gender", StringType(), True), \
        StructField("salary", IntegerType(), True) \
        ])

    df = spark.createDataFrame(data=data, schema=schema)
    df.printSchema()
    df.show()

##########df with custom schema######################
def df_with_custom_schema(spark):
    data = [
        (("James", None, "Smith"), "OH", "M"),
        (("Anna", "Rose", ""), "NY", "F"),
        (("Julia", "", "Williams"), "OH", "F"),
        (("Maria", "Anne", "Jones"), "NY", "M"),
        (("Jen", "Mary", "Brown"), "NY", "M"),
        (("Mike", "Mary", "Williams"), "OH", "M")
    ]

    schema = StructType([
        StructField('name', StructType([
            StructField('firstname', StringType(), True),
            StructField('middlename', StringType(), True),
            StructField('lastname', StringType(), True)
        ])),
        StructField('state', StringType(), True),
        StructField('gender', StringType(), True)
    ])

    df = spark.createDataFrame(data=data, schema=schema)
    df.printSchema()
    df.show()
    df.select("name").show()

##########df with nested schema ##########################
def df_with_nested_schema(spark):
    data2 = [('James', '', 'Smith', '1991-04-01', 'M', 3000),
             ('Michael', 'Rose', '', '2000-05-19', 'M', 4000),
             ('Robert', '', 'Williams', '1978-09-05', 'M', 4000),
             ('Maria', 'Anne', 'Jones', '1967-12-01', 'F', 4000),
             ('Jen', 'Mary', 'Brown', '1980-02-17', 'F', -1)
             ]

    columns = ["firstname", "middlename", "lastname", "dob", "gender", "salary"]

    df2 = spark.createDataFrame(data=data2, schema=columns)
    ddf2 = df2.withColumn("salary", col("salary").cast("Double"))
    ddf2.printSchema()
