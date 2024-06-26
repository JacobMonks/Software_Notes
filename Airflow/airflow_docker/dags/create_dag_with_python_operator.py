import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner" : "coder2j",
    "retries" : 5,
    "retry_delay" : datetime.timedelta(minutes = 5)
}

def get_name(ti):
    ti.xcom_push(key = "first_name", value = "Jacob")
    ti.xcom_push(key = "last_name", value = "Monks")

def get_age(ti):
    ti.xcom_push(key = "age", value = 25)
    
def greet(ti):
    first_name = ti.xcom_pull(task_ids = "get_name", key = "first_name")
    last_name = ti.xcom_pull(task_ids = "get_name", key = "last_name")
    age = ti.xcom_pull(task_ids = "get_age", key = "age")
    print(f"Hello, World! My name is {first_name} {last_name}, and I am {age} years old.")

with DAG(
    dag_id = "dag_python_operator_v8",
    description = "This will be a dag created using the Python operator.",
    default_args = default_args,
    start_date = datetime.datetime(2024,3,31),
    schedule_interval = "@daily"
) as dag:
    
    task1 = PythonOperator(
        task_id = "greet",
        python_callable = greet
    )
    
    task2 = PythonOperator(
        task_id = "get_name",
        python_callable = get_name
    )

    task3 = PythonOperator(
        task_id = "get_age",
        python_callable = get_age
    )

[task2, task3] >> task1
