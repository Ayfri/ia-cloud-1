from kafka import KafkaProducer, KafkaConsumer
import json
from data import Data
from constants import BOOTSTRAP_SERVERS, INPUT_TOPIC, OUTPUT_TOPIC

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
)

print(f"Waiting for messages to process on topic '{INPUT_TOPIC}'...")
try:
    for msg in consumer:
        print(f"Received raw message: {msg.value.decode()}")
        try:
            data_raw = json.loads(msg.value.decode())
            data = Data(**data_raw)
            print(f"Received on topic '{INPUT_TOPIC}': {data}")

            # Process: mark as processed
            data.processed = True

            # Resend
            producer.send(OUTPUT_TOPIC, json.dumps(data.__dict__).encode('utf-8'))
            producer.flush()
            print(f"Sent processed on topic '{OUTPUT_TOPIC}': {data}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    producer.close()
    consumer.close()
