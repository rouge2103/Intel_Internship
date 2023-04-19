from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('lr_example').getOrCreate()

from pyspark.ml.regression import LinearRegression

data = spark.read.csv('Ecommerce_Customer.csv', inferSchema=True, header=True)

data.printSchema()

#imp

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(inputCols=[''], outputCol='features')

#now we transform the data using the assembler
output = assembler.transform(data)

output.printSchema()

final_data = output.select('features', 'Yearly Amount Spent')

train_data, test_data = final_data.randomSplit([0.7,0.3])

# checking the split data
train_data.describe().show()
test_data.describe().show()

# training and testing
lr = LinearRegression(labelCol='Yearly Amount Spent')
lr_model = lr.fit(train_data)
test_results = lr_model.evaluate(test_data)

# evalutaion matrics
test_results.residuals.show()
test_results.rootMeanSquaredError
test_results.r2

# unlabled data
unlabeled_data = test_data.select('features')
unlabeled_data.show()
predictions = lr_model.transform(unlabeled_data)
predictions.show()