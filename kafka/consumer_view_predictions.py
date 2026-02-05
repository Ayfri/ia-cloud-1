import sys
import json
from kafka import KafkaConsumer, TopicPartition
from constants import BOOTSTRAP_SERVERS, OUTPUT_TOPIC

partition_number = int(sys.argv[1]) if len(sys.argv) > 1 else 0

consumer = KafkaConsumer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id="grp_view_predictions"
)

topic_partition = TopicPartition(OUTPUT_TOPIC, partition_number)
consumer.assign([topic_partition])

print(f"Consumer started for partition {partition_number}")
print(f"Reading predictions from '{OUTPUT_TOPIC}'...\n")

try:
    for msg in consumer:
        try:
            result = json.loads(msg.value.decode())
            print(f"[Partition {msg.partition}] Input: {result['input']}")
            print(f"[Partition {msg.partition}] Prediction: {result['prediction']}")
            print("---")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
