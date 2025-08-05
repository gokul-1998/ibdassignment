from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert binary value to string and add timestamp
lines = df.selectExpr("CAST(value AS STRING)", "timestamp")

# Count rows over a sliding window of 10s, every 5s
counts = lines.groupBy(
    expr("window(timestamp, '10 seconds', '5 seconds')")
).count()

# Write the output to console
query = counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
