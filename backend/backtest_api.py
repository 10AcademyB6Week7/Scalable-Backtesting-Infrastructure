from inspect import Parameter
from urllib import response
from flask import *
import os
import sys
sys.path.insert(0,'../scripts/')
from kafka_producer import producer
from kafka_consumer import consumer

app = Flask(__name__)

@app.route('/get_backtest_scene', methods=['POST'])
def get_backtest_scene():
    if request.method == 'POST':
        user_ID = request.form.get("user_ID")
        coin_name = request.form.get("coin_name")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        sma_value = request.form.get("sma_value")
        inital_cash = request.form.get("inital_cash")
        fee = request.form.get("end_date")
        backtest_scene = {"user_ID":user_ID,"coin_name":coin_name,"start_date":start_date,"end_date":end_date,"sma_value":sma_value,"inital_cash":inital_cash,"fee":fee}
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
        user_ID = request.form.get("user_ID")
        backtests_result = consumer('backtest_reslut_consumer',user_ID,'earliest')
        global backtest_response
        for message in backtests_result:
            backtest_response = message.value
            break

        return jsonify({"status": "success","returns":backtest_response.returns,"number_of_trades":backtest_response.number_of_trades,"winning_trades":backtest_response.winning_trades,"losing_trades":backtest_response.losing_trades,"max_drawdown":backtest_response.max_drawdown,"sharpe_ratio":backtest_response.sharpe_ratio})
    else:
            return{
                "status": "error",
                "message": f"{request.method} is not allowed"
            }


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', debug=True, port=port)