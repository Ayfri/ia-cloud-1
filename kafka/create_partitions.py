import time
from kafka.admin import KafkaAdminClient, NewPartitions
from constants import BOOTSTRAP_SERVERS, INPUT_TOPIC, OUTPUT_TOPIC

time.sleep(2)

admin_client = KafkaAdminClient(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    client_id='partition_creator',
    request_timeout_ms=5000
)

topic_partitions = {}
for topic in [INPUT_TOPIC, OUTPUT_TOPIC]:
    topic_partitions[topic] = NewPartitions(total_count=2)

try:
    admin_client.create_partitions(topic_partitions, validate_only=False)
    print("Partitions created successfully")
except Exception as e:
    print(f"Note: {e}")
finally:
    admin_client.close()
