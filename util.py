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
