from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add scripts folder to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from fetch_weather import fetch_weather_for_cities

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='multi_city_weather_pipeline',
    default_args=default_args,
    description='Fetch hourly weather data for multiple cities and save to PostgreSQL + Excel',
    schedule_interval='@hourly',  # ⏰ Runs every hour
    start_date=datetime(2024, 4, 15),
    catchup=False,
    is_paused_upon_creation=False,
    tags=['weather', 'hourly']
) as dag:

    cities = [
        "Dallas", "New York", "London", "Tokyo", "Bengaluru", "San Francisco",
        "Chicago", "Berlin", "Sydney", "Toronto", "Mumbai", "Cape Town"
    ]

    fetch_and_save = PythonOperator(
        task_id='fetch_weather_for_all_cities',
        python_callable=lambda: fetch_weather_for_cities(cities)
    )

    fetch_and_save
