from kafka import KafkaAdminClient 



def read_topics():
    client = KafkaAdminClient(
            bootstrap_servers = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
            api_version=(0,11,5),
        )
    
    print("Topics: ")
    print(client.list_topics())
    
read_topics()