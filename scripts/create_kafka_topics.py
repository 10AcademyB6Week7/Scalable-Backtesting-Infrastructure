from kafka import KafkaAdminClient 
from kafka.admin import NewTopic
import logging

logging.basicConfig(filename='../log/log.log', filemode='a',encoding='utf-8', level=logging.DEBUG)


def create_topics(topic_list):
    client = KafkaAdminClient(
            bootstrap_servers = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
            api_version=(0,11,5),)
    
    new_topic = []
    
    for topic in topic_list:
        new_topic.append(NewTopic(name=topic,num_partitions=3,replication_factor=1))
    client.create_topics(new_topics=new_topic,validate_only=False)
    
    return client.list_topics()