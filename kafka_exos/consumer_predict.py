import sys
import json
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka_exos.data import Data
from kafka_exos.constants import BOOTSTRAP_SERVERS, INPUT_TOPIC, OUTPUT_TOPIC
from kafka_exos.model_loader import load_model, predict

model = load_model()
if not model:
    sys.exit(1)

partition_number = int(sys.argv[1]) if len(sys.argv) > 1 else 0

consumer = KafkaConsumer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id="grp_predictions"
)
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

topic_partition = TopicPartition(INPUT_TOPIC, partition_number)
consumer.assign([topic_partition])

print(f"Consumer started for partition {partition_number}")
print(f"Reading from '{INPUT_TOPIC}' and sending predictions to '{OUTPUT_TOPIC}'...\n")

try:
    for msg in consumer:
        try:
            data_raw = json.loads(msg.value.decode())
            data = Data(**data_raw)
            print(f"[Partition {msg.partition}] Received: {data.data}")

            prediction = predict(model, data.data)
            if prediction is not None:
                result = {
                    "input": data.data,
                    "prediction": prediction.tolist(),
                    "partition": msg.partition
                }
                print(f"[Partition {msg.partition}] Prediction: {prediction}")
                producer.send(
                    OUTPUT_TOPIC,
                    json.dumps(result).encode('utf-8'),
                    partition=partition_number
                )
                producer.flush()
                print(f"[Partition {msg.partition}] Sent to '{OUTPUT_TOPIC}'\n")
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
    producer.close()
