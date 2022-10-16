# importing the required libraries
import json
from random import randrange
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from sqlalchemy import create_engine, text
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import random

default_args = {
    # 'start_date': days_ago(5),
    'owner': 'f0x_tr0t',
    'depends_on_past': False,
    'email': ['henokdes1@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'tags': ['week8', 'backtests, Kafka clusters']
}


# define the DAG
etl_dag = DAG(
    'prod.backtests.Kafka.X.postgresql',
    default_args=default_args,
    start_date=datetime(2022, 10, 11),
    description='An end to end data pipeline for week 8',
    schedule=timedelta(hours=5),    # run every given time
    catchup=False                   # dont perform a backfill of missing runs
)


# region produce scene


def gerRandomAsset() -> str:
    assets = ['MSFT', 'TSLA', 'RNDG', 'GGMU', 'KKSKU', 'BKR', 'TST']
    rand_ind = randrange(0, 7, 1)
    return assets[rand_ind]


def gerRandomStrategy() -> str:
    strats = ['SMA', 'SMA_RSA', 'TEST']
    rand_strat = randrange(0, 3, 1)
    return strats[rand_strat]


def produce_scene():
    print(f'publishing scenes to {SCENES_TOPIC}. . .')
    producer = KafkaProducer(bootstrap_servers=servers)

    _start_date = datetime.date(datetime.now())
    _asset = gerRandomAsset()
    _starting_money = randrange(100000, 50000000, 20000)
    _strat = gerRandomStrategy()

    test_scene = json.dumps({"asset": _asset,
                             "cash": _starting_money,
                             "strategy": _strat,
                             "start_date": str(_start_date),
                             "end_date": str(_start_date)
                             }, indent=4)

    print(f'test scene: {test_scene}\ntype: {type(test_scene)}')
    byte_encoded_data = bytes(f"{test_scene}", encoding='utf-8')
    print(f'byte encoded test scene: {byte_encoded_data}\ntype: ' +
          f'{type(byte_encoded_data)}')

    future = producer.send(SCENES_TOPIC, byte_encoded_data)
    producer.close()
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()
        pass
    # Successful result returns assigned partition and offset
    print(f"value: {record_metadata}")
    print(f"topic: {record_metadata.topic}")
    print(f"partition: {record_metadata.partition}")
    print(f"offset: {record_metadata.offset}")
    print('publishing scenes completed. . .')


publish_scene = PythonOperator(
    task_id='produce_scene',
    python_callable=produce_scene,
    dag=etl_dag
)


def gerRandomFloats() -> str:
    return random.uniform(100.0, 1000000.0)


def gerRandomInt() -> str:
    return randrange(0, 51, 1)


def produce_results():
    print(f'publishing results to {RESULTS_TOPIC}. . .')
    producer = KafkaProducer(bootstrap_servers=servers)

    _sharpe_ratio = gerRandomFloats()
    _return = gerRandomFloats()
    _max_drawdown = gerRandomFloats()
    _win_trade = gerRandomInt()
    _loss_trade = gerRandomInt()
    _total_trade = gerRandomInt()
    _start_portfolio = gerRandomFloats()
    _final_portfolio = gerRandomFloats()

    test_result = json.dumps({"sharpe_ratio": _sharpe_ratio,
                              "return": _return, "max_drawdown": _max_drawdown,
                              "win_trade": _win_trade,
                              "loss_trade": _loss_trade,
                              "total_trade": _total_trade,
                              "start_portfolio": _start_portfolio,
                              "final_portfolio": _final_portfolio
                              }, indent=4)

    print(f'test result: {test_result}\ntype: {type(test_result)}')
    byte_encoded_data = bytes(f"{test_result}", encoding='utf-8')
    print(f'byte encoded test result: {byte_encoded_data}\ntype: ' +
          f'{type(byte_encoded_data)}')

    future = producer.send(RESULTS_TOPIC, byte_encoded_data)
    producer.close()
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        logger.exception()
        pass
    # Successful result returns assigned partition and offset
    print(f"value: {record_metadata}")
    print(f"topic: {record_metadata.topic}")
    print(f"partition: {record_metadata.partition}")
    print(f"offset: {record_metadata.offset}")
    print('publishing results completed. . .')


publish_result = PythonOperator(
    task_id='publish_result',
    python_callable=produce_results,
    dag=etl_dag
)


publish_scene >> publish_result