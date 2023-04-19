from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('lr_project').getOrCreate()

from pyspark.ml.regression import LinearRegression

data = spark.read.csv('cruise_ship_info.csv', inferSchema=True, header=True)

data.printSchema()

from pyspark.ml.feature import VectorAssembler, StringIndexer
# Ship_name,Cruise_line,Age,Tonnage,passengers,length,cabins,passenger_density,crew
indexer = StringIndexer(inputCol='Cruise_line', outputCol='Cruise_line_index')
indexed_data = indexer.fit(data).transform(data)

assembler = VectorAssembler(inputCols=['Cruise_line_index','Age','Tonnage','passengers','length','cabins','passenger_density'], outputCol='features')
output = assembler.transform(indexed_data)
output.printSchema()

final_data = output.select(['features', 'crew'])

train, test = final_data.randomSplit([0.8,0.2])

train.describe().show()
test.describe().show()

lr = LinearRegression(labelCol='crew')
lr_model = lr.fit(train)
results = lr_model.evaluate(test)

