import vectorbt as vbt
# from mlflow import log_metric, log_param, log_artifacts, log_params
import mlflow
import random
from sqlalchemy import create_engine, select
from dotenv import load_dotenv
import os, sys
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join("./backend/")))
from models import User, BackTestResult, BackTestScene
from kafka import KafkaAdminClient
from kafka import KafkaConsumer
from kafka import KafkaProducer


load_dotenv()

class VectorbotPipeline():
    def __init__(self,user_id, indicator="sma",init_cash=1000, ema_value=0,stock='AMZN', fast_ma=10, slow_ma=50, start='2021-10-11', end='2022-10-11', period=None, fees=0.005, is_experiment=False):
        self.user_id = user_id
        self.init_cash = init_cash
        self.ema_value = ema_value
        self.indicator = indicator
        self.stock = stock
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.start = start
        self.end = end
        self.period = period
        self.fees = fees
        self.is_experiment = is_experiment
        self.price = vbt.YFData.download(self.stock, start=self.start, end=self.end).get('Close')
        if(is_experiment):
            try:
                mlflow.end_run()
            except:
                pass
            val = random.randint(1, 1000)
            mlflow.set_experiment(f"{self.stock}_{self.init_cash}_{val}")
            mlflow.set_tracking_uri('http://localhost:5000')
            mlflow.start_run(run_name="self_stock")
            mlflow.log_metric("experiment_extra_num", val)

    def setup_from_holding(self):
        if self.is_experiment:
            mlflow.log_param("stock", self.stock)
            mlflow.log_param("init_cash", self.init_cash)
        self.pf = vbt.Portfolio.from_holding(self.price, init_cash=self.init_cash)
    
    def setup_sma(self):
        if self.is_experiment:
            mlflow.log_param("stock_sma", self.stock)
            mlflow.log_param("stock_fast_sma", self.fast_ma)
            mlflow.log_param("stock_slow_sma", self.slow_ma)
            mlflow.log_metric("init_cash", self.init_cash)
        price = vbt.YFData.download(self.stock, start=self.start, end=self.end).get('Close')
        self.calc_fast_ma = vbt.MA.run(self.price, self.fast_ma, short_name='fast_ma')
        self.calc_slow_ma = vbt.MA.run(self.price, self.slow_ma, short_name='slow_ma')
        entries = self.calc_fast_ma.ma_crossed_above(self.calc_slow_ma)
        exits = self.calc_fast_ma.ma_crossed_below(self.calc_slow_ma)
        self.pf = vbt.Portfolio.from_signals(self.price, entries, exits, init_cash=self.init_cash)

    def readbale_records(self):
        print(self.pf.orders.records_readable)
        print(self.pf.total_profit())

    def plot_fast_and_slow(self):
        fig = self.price.vbt.plot(trace_kwargs=dict(name='Close'))
        self.calc_fast_ma.ma.vbt.plot(trace_kwargs=dict(name='Fast MA'), fig=fig)
        self.calc_slow_ma.ma.vbt.plot(trace_kwargs=dict(name='Slow MA'), fig=fig)
        self.pf.positions.plot(close_trace_kwargs=dict(visible=False), fig=fig)
        # vbt.save('fig.png', fig)
        with open('./images/vectorbt/fast_and_slow_plot.png','wb') as f:
            f.write(fig.to_image(format='png'))
        with open('./images/vectorbt/fast_and_slow_plot.png','rb') as f:
            if self.is_experiment:
                mlflow.log_artifact("./images/vectorbt/fast_and_slow_plot.png")

    def return_backtest_result(self):
        if self.is_experiment:
            mlflow.log_param("stock", self.stock)
            mlflow.log_param("init_cash", self.init_cash)
            for k,v in self.pf.stats().to_dict().items():
                mlflow.log_param(str(k).replace('%','').replace('[','').replace(']',''),str(v))

        with open('./backtest_result/vectorbt/fast_and_slow_plot.txt','w') as f:
            for key, value in self.pf.stats().to_dict().items(): 
                f.write('%s: %s\n' % (key, value))
            # f.write(self.pf.stats().to_dict())
        return self.pf.stats().to_dict()

    def setup_bbands(self):
        bbands = vbt.BBANDS.run(self.price)
        entries = bbands.close_crossed_below(bbands.lower)
        exits = bbands.close_crossed_above(bbands.upper)
        self.pf = vbt.Portfolio.from_signals(self.price, entries, exits)

    def run_indicator(self):
        if self.indicator == 'bbands':
            self.setup_bbands()
        elif self.indicator == 'sma':
            self.setup_sma()

    def save_result_and_publish(self):
        result_dict = self.return_backtest_result()
        DB_URL = os.environ["DB_URL"]
        sql_engine = create_engine(DB_URL)
        session = Session(sql_engine)

        user = session.query(User).filter_by(id=self.user_id).first()

        if user:
            backtest_scene = BackTestScene(coin_name="BTC",
                start_date=self.start_date,
                end_date=self.end_date,
                ema_value=self.ema_value,
                sma_value=self.slow_ma,
                fma_value=self.fast_ma,
                initial_cash=self.init_cash,
                fee=self.fee,
                user_id=user.id
            )

            session.add(backtest_scene)
            backtest_result = BackTestResult(
                returns=str(result_dict['Total Return [%]'] * 100) if result_dict.get('Total Return [%]') is not None else "NaN",
                number_of_trades=result_dict['Total Trades'] if result_dict.get('Total Trades') is not None else "NaN",
                winning_trades=str(result_dict['Avg Winning Trade [%]'] * 100) if result_dict.get('Avg Winning Trade [%]') is not None else "NaN",
                losing_trades=str(result_dict['Avg Losing Trade [%]'] * 100) if result_dict.get('Avg Losing Trade [%]') is not None else "NaN",
                max_drawdown=str(result_dict['Max Drawdown [%]'] * 100) if result_dict.get('Max Drawdown [%]') is not None else "NaN",
                sharpe_ratio=result_dict['Sharpe Ratio'] if result_dict.get('Sharpe Ratio') is not None else "NaN",
                backtest_scene_id=backtest_scene.id,
                backtest_scene=backtest_scene
            )
            session.add(backtest_result)
            session.commit()
            producer = KafkaProducer(
                bootstrap_servers=['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092'],
                client_id='g2-result-producer',value_serializer=lambda x: dumps(x).encode('utf-8'))
            producer.send(f"{self.user_id}",{"backtest_result_id":backtest_result.id}).get(timeout=30)
        else:
            raise Exception("User not found")

        
        
        


    # def plot_portfolio_summary(self):
    #     returns = self.price.vbt.to_returns()
    #     val = returns.vbt.returns.qs.html_report
    #     # val = returns.vbt.returns.qs.plot_snapshot()
    #     # print(val)
    #     # print(type(val))
    #     object_methods = [method_name for method_name in dir(val)
    #               if callable(getattr(val, method_name))]
    #     print(object_methods)

    


if __name__ == '__main__':
    # vbtp = VectorbotPipeline(12, is_experiment=False)
    # vbtp.setup_sma()
    # vbtp.save_result_and_publish()
    
    
    # vbtp.readbale_records()
    # vbtp.plot_fast_and_slow()
    # vbtp.return_backtest_result()
    # vbtp.plot_portfolio_summary()
    # vbtp.setup_from_holding()
    # vbtp.readbale_records()
    # vbtp.return_backtest_result()

    DB_URL = os.environ["DB_URL"]
    sql_engine = create_engine(DB_URL)
    session = Session(sql_engine)

    # new_user = User(email="example@example.com", password="12345",first_name="Jhon",last_name="Doe",user_role="normal")
    # session.add(new_user)
    # session.commit()
    user = session.query(User).filter_by(id=1).first()
    print(f"USER: {user.first_name}")

    backtest_scene = BackTestScene(coin_name="BTC",
        start_date="2022-10-13",
        end_date="2022-10-15",
        ema_value="50",
        sma_value="55",
        fma_value="23",
        initial_cash="1000",
        fee="0.00",
        user_id=user.id
    )

    session.add(backtest_scene)
    session.commit()
    print(backtest_scene.id)
    
    stmt = select(BackTestScene)

    for scene in session.scalars(stmt):
        print(scene.id)

