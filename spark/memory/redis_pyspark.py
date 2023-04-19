from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('redis_spark').getOrCreate()

df = spark.read.format("org.apache.spark.sql.redis").option("table", "people").option("key.column", "en_curid").load()

