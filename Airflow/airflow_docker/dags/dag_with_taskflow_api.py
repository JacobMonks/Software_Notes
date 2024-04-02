from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    "owner" : "coder2j",
    "retries" : 5,
    "retry_delay" : timedelta(minutes = 5)
}

@dag(
        dag_id = "dag_with_taskflow_api_v2",
        description = "First dag using the Taskflow API.",
        default_args = default_args,
        start_date = datetime(2024,3,31),
        schedule_interval = "@daily"
)
def hello_world_etl():
    
    @task(multiple_outputs = True)
    def get_name():
        return {"first_name" : "Jacob",
                "last_name" : "Monks"}

    @task()
    def get_age():
        return 25
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello World! My name is {first_name} {last_name}, and I am {age} years old.")

    name = get_name()
    age = get_age()
    greet(name["first_name"], name["last_name"], age)
    
greet_dag = hello_world_etl()