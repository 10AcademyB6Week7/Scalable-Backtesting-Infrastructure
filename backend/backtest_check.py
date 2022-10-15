from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from secrets import db
import sys
import logging
sys.path.insert(0,'../scripts/')
from create_kafka_topics import create_topics
from kafka_producer import producer
from kafka_consumer import consumer
from vectorbt_pipeline import VectorbotPipeline
from models import BackTestScene,BackTestResult
logging.basicConfig(filename='../log/log.log', filemode='a',encoding='utf-8', level=logging.DEBUG)



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
        fma_value = value["fma_value"]
        inital_cash = value["inital_cash"]
        fee = value["fee"]
        check = session.query(BackTestScene).filter_by(user_id=user_ID,coin_name=coin_name,start_date=start_date,end_date=end_date,sma_value=sma_value,fma_value=fma_value,inital_cash=inital_cash,fee=fee).first()
        if check is not None:
            back_test_id = check.id
            response=session.query(BackTestResult ).filter_by(backtest_scene_id=back_test_id).first()
            create_topics([user_ID])
            return producer('backtest_producer',user_ID,{"returns":response.returns,"number_of_trades":response.number_of_trades,"winning_trades":response.winning_trades,"losing_trades":response.losing_trades,"max_drawdown":response.max_drawdown,"sharpe_ratio":response.sharpe_ratio})
        elif check is None:
            result = VectorbotPipeline(user_id=user_ID,start=start_date,end=end_date,slow_ma=sma_value,fast_ma=fma_value,init_cash=inital_cash,stock=coin_name)
            return result.save_result_and_publish()
