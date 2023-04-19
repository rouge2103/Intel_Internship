from pyspark.sql import SparkSession

def get_started(spark):
    df = spark.read.csv('taxi.csv')
    df.show()
    df.write.mode('overwrite').option("compression","GZIP").csv('taxi_compressd.csv')
    df.write.mode('overwrite').option('compression',"snappy").csv('taxi_snappy.csv')

    # csv
    df.write.format("csv").option("header", True)
    df.write.format("csv").save("/tmp/spark_output/datacsv")
    df.write.option("header", True).option("delimiter","|").csv("/tmp/spark_output/datacsv")

    #parquet
    df.write.parquet("/tmp/out/people.parquet")

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .appName("Basics") \
        .getOrCreate()

    get_started(spark)
    
