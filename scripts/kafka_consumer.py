from kafka import KafkaConsumer
from json import loads
import logging

logging.basicConfig(filename='../log/log.log', filemode='a',encoding='utf-8', level=logging.DEBUG)

def consumer(group_id,topic,offset):
    consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
            auto_offset_reset=offset,
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8')))
    return consumer
