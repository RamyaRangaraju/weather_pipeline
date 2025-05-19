from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='weather_test_dag',
    default_args=default_args,
    description='Test DAG for visibility',
    schedule='@daily',
    start_date=datetime(2024, 4, 10),
    catchup=False,
    tags=['test'],
) as dag:

    start = DummyOperator(task_id='start')
