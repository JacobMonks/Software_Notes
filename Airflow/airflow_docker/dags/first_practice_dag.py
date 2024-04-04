import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner" : "Jacob Monks",
    "retries" : 5,
    "retry_delay" : datetime.timedelta(minutes = 2)
}

with DAG(
    dag_id = "first_practice_dag",
    description = "This is my first DAG made from scratch.",
    start_date = datetime.datetime(2024,3,25),
    schedule_interval = "@daily",
    default_args = default_args
    
) as dag:
    task1 = BashOperator(
        task_id = "task1",
        bash_command = "echo Hello World!",
        retries = 2,
    )

    task2 = BashOperator(
        task_id = "task2",
        bash_command = "echo My name is Jacob!",
        retries = 2,
    )

task1 >> task2