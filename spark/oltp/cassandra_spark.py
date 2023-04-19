from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('cassandra_spark').getOrCreate()

spark.conf.set("spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")
spark.read.table("myCatalog.test_keyspace.test").show()

df = spark.read.format("org.apache.spark.sql.cassandra").options(table="test", keyspace="test_keyspace").load()
df.printSchema()
#df.show()
df.createOrReplaceTempView("temp_table")
spark.sql("select * from temp_table").show()

