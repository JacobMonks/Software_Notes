import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner" : "coder2j",
    "retries" : 5,
    "retry_delay" : datetime.timedelta(minutes = 2),
}

with DAG(
    dag_id = "our_first_dag_v3",
    description = "This will be our first created dag.",
    start_date = datetime.datetime(2024, 3, 29, 2),
    schedule_interval = "@daily",
    default_args = default_args
) as dag:
    
    task1 = BashOperator(
        task_id = "task1",
        bash_command = "echo Hello, World!"
    )

    task2 = BashOperator(
        task_id = "task2",
        bash_command = "echo This is the second task."
    )

    task3 = BashOperator(
        task_id = "task3",
        bash_command = "echo This will run after task1 at the same time as task2."
    )

task1 >> [task2, task3]