from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('nlp_1').getOrCreate()

from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType

sen_df = spark.createDataFrame([(),(),()])

tokenizer = Tokenizer(inputCol='sentence', outputCol='words')
regex_tokenizer = RegexTokenizer(inputCol='sentence', outputCol='words', pattern="\\W")

count_tokens = udf(lambda words:len(words), IntegerType())

tokenized = tokenizer.transform(sen_df)
tokenized.withColumn('tokens', count_tokens(col('words'))).show()

rg_tokenized = regex_tokenizer.trasform(sen_df)
rg_tokenized.withColumn('token', count_tokens(col('words'))).show()
