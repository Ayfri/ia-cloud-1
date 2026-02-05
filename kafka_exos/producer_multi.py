import sys
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
    num_messages = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Sending {num_messages} message(s)...\n")

    for _ in range(num_messages):
        size = random.randint(800, 3000)
        nb_rooms = random.randint(1, 6)
        garden = random.randint(0, 1)
        data = Data(data=[[size, nb_rooms, garden]])
        send_data(data)
        print()

    producer.close()
    print("Done!")
