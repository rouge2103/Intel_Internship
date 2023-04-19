from pyspark.sql import SparkSession

spark = SparkSession.builder.config("spark.jars", "/home/aayush/hadoop/spark-3.1.3/jars/postgresql-42.5.1.jar").appName('spark_postgres_test').getOrCreate()

df = spark.read.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/tpcd_db").option("driver", "org.postgresql.Driver").option("dbtable", "customer").option("user", "aayush").option("password", "test123").load()
df2 = spark.read.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/tpcd_db").option("driver", "org.postgresql.Driver").option("dbtable", "item").option("user", "aayush").option("password", "test123").load()

# viewing your data
df.printSchema()
df.show(5)


# data frame operations
df2.filter('i_current_price > 10 ').show()
df2.filter((df2['i_current_price'] < 20) & (df2['i_current_price'] > 10)).show()
df2.groupBy('i_size').mean().show() # average price of an item by size
df2.agg({'i_current_price':'sum'}).show()
df2.agg({'i_current_price':'max'}).show()

#
from pyspark.sql.functions import countDistinct, avg, stddev
df2.select(avg('i_current_price').alias('Average current price')).show()
df2.orderBy(df2['i_current_price'].desc()).show()

# sql operations
df2.createOrReplaceTempView("item_temp")
spark.sql('select count(*) from item_temp')
spark.sql('select sum(i_current_sum) as total_cost from item_temp')
spark.sql('select avg(i_current_sum) as avg_ form item_temp')
