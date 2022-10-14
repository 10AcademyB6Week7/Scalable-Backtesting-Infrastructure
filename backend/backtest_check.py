from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from secrets import db
import sys
sys.path.insert(0,'../scripts/')
from create_kafka_topics import create_topics
from kafka_producer import producer
from kafka_consumer import consumer



def check_backtest():
    engine = create_engine(db, echo=True, future=True)
    session = Session(engine)
    consume_request = consumer('backtest_consumer','g2-backtest_requests','latest')
    for message in consume_request:
        value = message.value
        user_ID = value["user_ID"]
        coin_name =value["coin_name"]
        start_date = value["start_date"]
        end_date  = value["end_date"]
        sma_value = value["sma_value"]
        inital_cash = value["inital_cash"]
        fee = value["fee"]
        check = session.query(Backtest_Seen).filter_by(user_ID=user_ID,coin_name=coin_name,start_date=start_date,end_date=end_date,sma_value=sma_value,inital_cash=inital_cash,fee=fee).first()
        if check is not None:
            back_test_id = check.id
            response=session.query(Result_Table ).filter_by(Back_test_ID=back_test_id).first()
            return producer('backtest_producer',user_ID,response)
        elif check is None:
            pass
