from kafka import KafkaProducer
import json
from data import Data
from constants import BOOTSTRAP_SERVERS, INPUT_TOPIC

producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)

def send_data(data: Data):
    print(f"Sending on topic '{INPUT_TOPIC}': {data}")
    producer.send(INPUT_TOPIC, json.dumps(data.__dict__).encode('utf-8'))
    producer.flush()

if __name__ == '__main__':
    data = Data(data=[[1, 2], [3, 4]])
    send_data(data)
    producer.close()
