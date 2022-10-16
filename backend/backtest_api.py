from inspect import Parameter
from urllib import response
from flask import *
import os
import sys
import logging
sys.path.insert(0,'../scripts/')
sys.path.insert(0,'../log/')
from kafka_producer import producer
from kafka_consumer import consumer
from models import BackTestScene,BackTestResult
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from secretsi import db

logging.basicConfig(filename='../log/log.log', filemode='a', level=logging.DEBUG)
app = Flask(__name__)

@app.route('/get_backtest_scene', methods=['POST'])
def get_backtest_scene():
    if request.method == 'POST':
        user_ID = request.json["user_ID"]
        stock = request.json["stock"]
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
        indicator = request.json["indicator"]
        inital_cash = request.json["inital_cash"]
        backtest_scene = {"user_ID":user_ID,"stock":stock,"start_date":start_date,"end_date":end_date,"indicator":indicator,"inital_cash":inital_cash}
        producer('backtest_scene','g2-backtest_requests',backtest_scene)
        return jsonify({"status": "success","message":'backtest running'})
    else:
            return{
                "status": "error",
                "message": f"{request.method} is not allowed"
            }

@app.route('/backtest_results', methods=['POST'])
def backtest_results():
    if request.method == 'POST':
        engine = create_engine(db, echo=True, future=True)
        session = Session(engine)
        user_ID = request.json["user_ID"]
        backtests_result = consumer('backtest_reslut_consumer',str(user_ID),'latest')
        global backtest_response
        for message in backtests_result:
            backtest_response = message.value
            break
            
        response=session.query(BackTestResult ).filter_by(backtest_scene_id=backtest_response['backtest_scene_id']).first()
        return jsonify({"status": "success","returns":response.returns,"number_of_trades":response.number_of_trades,"winning_trades":response.winning_trades,"losing_trades":response.losing_trades,"max_drawdown":response.max_drawdown,"sharpe_ratio":response.sharpe_ratio})
    else:
            return{
                "status": "error",
                "message": f"{request.method} is not allowed"
            }


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', debug=True, port=port)