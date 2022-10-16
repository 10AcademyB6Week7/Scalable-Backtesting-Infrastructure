from datetime import timedelta
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from vectorbt_pipeline import VectorbotPipeline
import os
import sys
sys.path.append(os.path.abspath(os.path.join("../scripts/")))


def run_sma():
    v = VectorbotPipeline(1, indicator="sma")  # user id is required
    v.run_indicator()  # runs the indicator based on the instantiated indicator value
    v.save_result_and_publish()


default_args = {
    'owner': 'group2',
    'start_date': datetime(2022, 9, 15),
    'retries': 2
    'retry_delay': timedelta(minutes=20)
}

sma_dag = DAG('sma_etl', default_args=default_args,
              schedule_interval='0 * * * *')


# Create the task
sma_task = PythonOperator(
    task_id='run_sma',
    python_callable=run_sma,
    dag=sma_dag
)
