from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner" : "coder2j",
    "retries" : 5,
    "retry_delay" : timedelta(minutes = 5)
}

with DAG(
    dag_id = "dag_with_cron_expression_v5",
    description = "DAG that uses Cron Expressions",
    start_date = datetime(2024,3,25),
    schedule_interval = "12 * 2 4 *",
    default_args = default_args
) as dag:
    task1 = BashOperator(
        task_id = "task1",
        bash_command = "echo dag with cron expression!"
    )

    task1