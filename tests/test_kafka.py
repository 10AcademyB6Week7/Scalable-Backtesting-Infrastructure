import unittest
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from testcontainers.kafka import KafkaContainer



def produce_and_consume_kafka_message(container):
    topic = 'test-topic'
    bootstrap_server = container.get_bootstrap_server()

    producer = KafkaProducer(bootstrap_servers=[bootstrap_server])
    producer.send(topic, b"verification message")
    producer.flush()
    producer.close()

    consumer = KafkaConsumer(bootstrap_servers=[bootstrap_server])
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])
    consumer.seek_to_beginning()
    assert consumer.end_offsets([tp])[tp] == 1, \
        "Expected exactly one test message to be present on test topic !"

class KafkaTest(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # print(KafkaContainer())
    
    # def test_kafka_producer_consumer(self):
    #     print("TESTING")
    #     with KafkaContainer() as container:
    #         produce_and_consume_kafka_message(container)
    #         print("TESTING")


    # def test_kafka_producer_consumer_custom_port(self):
    #     with KafkaContainer(port_to_expose=9888) as container:
    #         assert container.port_to_expose == 9888
    #         produce_and_consume_kafka_message(container)


    def test_kafka_confluent_7_1_3(self):
        with KafkaContainer(image='confluentinc/cp-kafka:7.1.3') as container:
            produce_and_consume_kafka_message(container)


    











if __name__ == "__main__":
    unittest.main()