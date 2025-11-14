# -- parquet file into streams
# -- read the Parquet file using Pandas, then serialize each row into JSON and send that as a Kafka message.
import pandas as pd
from confluent_kafka import Producer
import json

# Load parquet file
df = pd.read_parquet("data/fhv_tripdata_2023-09.parquet")

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

for _, row in df.iterrows():
    message = {
        "pickup_datetime": str(row["pickup_datetime"]),
        "dropoff_datetime": str(row["dropoff_datetime"]),
        "passenger_count": int(row["passenger_count"]),
        "trip_distance": float(row["trip_distance"])
    }
    producer.produce("taxi-events", json.dumps(message))
    producer.poll(0)

producer.flush()

