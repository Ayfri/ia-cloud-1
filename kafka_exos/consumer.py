import sys
import json
from kafka import KafkaConsumer, TopicPartition
from kafka_exos.data import Data
from kafka_exos.constants import BOOTSTRAP_SERVERS, OUTPUT_TOPIC

partition_number = int(sys.argv[1]) if len(sys.argv) > 1 else 0

consumer = KafkaConsumer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id="grp1"
)

topic_partition = TopicPartition(OUTPUT_TOPIC, partition_number)
consumer.assign([topic_partition])

print(f"Waiting for processed messages on topic '{OUTPUT_TOPIC}' (partition {partition_number})...")
try:
    for msg in consumer:
        try:
            data_raw = json.loads(msg.value.decode())
            data = Data(**data_raw)
            print(f"Received from partition {msg.partition}: {data}")
        except json.JSONDecodeError as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    consumer.close()
