from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from secretsi import db
import sys,os
import logging
sys.path.append(os.path.abspath(os.path.join("../scripts/")))
from create_kafka_topics import create_topics
from kafka_producer import producer
from kafka_consumer import consumer
from vectorbt_pipeline import VectorbotPipeline
from models import BackTestScene,BackTestResult,User
from kafka import KafkaAdminClient




def check_backtest():
    engine = create_engine(db, echo=True, future=True)
    session = Session(engine)
    consume_request = consumer('backtest_consumer','g2-backtest_requests','latest')
   
    for message in consume_request:
        value = message.value
        user_ID = value["user_ID"]
        stock =value["stock"]
        start_date = value["start_date"]
        end_date  = value["end_date"]
        indicator = value["indicator"]
        inital_cash = value["inital_cash"]
        check = session.query(BackTestScene).filter_by(user_id=int(user_ID)).first()
        user = session.query(User).filter_by(id=user_ID).first()
  
        if check is not None:
            back_test_id = check.id
            response=session.query(BackTestResult ).filter_by(backtest_scene_id=back_test_id).first()
            if response is not None:
                
                client = KafkaAdminClient(
                         bootstrap_servers = ['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
                         api_version=(0,11,5),)
                if str(user_ID) not in client.list_topics():
                    create_topics([user_ID])
                producer('backtest_producer',str(user_ID),{"backtest_scene_id":response.backtest_scene_id})
                
        elif check is None:
            if user:
                vectorbt_pipeline = VectorbotPipeline(
                user_ID, indicator=indicator,
                init_cash=int(inital_cash),
                stock=stock,
                start=start_date,
                end=end_date
                )
                vectorbt_pipeline.run_indicator()
                vectorbt_pipeline.save_result_and_publish()
check_backtest()