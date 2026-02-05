from kafka import KafkaConsumer
import json
from data import Data
from constants import BOOTSTRAP_SERVERS, OUTPUT_TOPIC

consumer = KafkaConsumer(
    OUTPUT_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
)

print(f"Waiting for processed messages on topic '{OUTPUT_TOPIC}'...")
try:
    for msg in consumer:
        try:
            data_raw = json.loads(msg.value.decode())
            data = Data(**data_raw)
            print(f"Received: {data}")
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    consumer.close()
