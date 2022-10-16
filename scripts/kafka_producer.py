from kafka import KafkaProducer
from json import dumps


def producer(client_id,topic,data):

    producer = KafkaProducer(
    bootstrap_servers=['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
    client_id=client_id,value_serializer=lambda x: dumps(x).encode('utf-8'))

    return producer.send(topic, value=data).get(timeout=30)