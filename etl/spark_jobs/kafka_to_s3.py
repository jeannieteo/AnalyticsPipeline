# -- ingestion into S3 storage flow. 
# -- This job will read JSON messages from Kafka and write them into Parquet files in S3 (Bronze layer)

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Spark session
# Add recommended `s3a` Hadoop/Spark configs so Spark can talk to S3 reliably.
# Requirements: add `hadoop-aws` and a matching `aws-java-sdk` to the driver/executor classpath
# (or use `--packages` with `spark-submit`). Credentials are provided via the
# AWS SDK default provider chain (IAM role, environment, profile, etc.).
spark = SparkSession.builder \
    .appName("KafkaToS3Bronze") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .config("spark.hadoop.fs.s3a.multipart.size", "104857600") \
    .config("spark.hadoop.fs.s3a.threads.max", "256") \
    .getOrCreate()

# Define schema for incoming JSON messages
schema = StructType([
    StructField("pickup_datetime", StringType(), True),
    StructField("dropoff_datetime", StringType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", DoubleType(), True)
])

# Read stream from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "taxi-events") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON value
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to S3 (Bronze layer) # bucket s3://cdk-hnb659fds-assets-699111784748-ap-southeast-2
query = df_parsed.writeStream \
    .format("parquet") \
    .option("path", "s3a://your-bucket/bronze/taxi_events/") \
    .option("checkpointLocation", "s3a://your-bucket/checkpoints/taxi_events/") \
    .outputMode("append") \
    .start()

query.awaitTermination()

