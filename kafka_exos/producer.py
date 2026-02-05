import json
import random
from kafka import KafkaProducer
from kafka_exos.data import Data
from kafka_exos.constants import BOOTSTRAP_SERVERS, INPUT_TOPIC

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

def send_data(data: Data):
    partition = random.randint(0, 1)
    print(f"Sending to partition {partition}: {data}")
    producer.send(INPUT_TOPIC, json.dumps(data.__dict__).encode('utf-8'), partition=partition)
    producer.flush()

if __name__ == '__main__':
    data = Data(data=[[1500, 3, 1]])
    send_data(data)
    producer.close()
