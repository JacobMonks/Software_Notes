from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner" : "coder2j",
    "retries" : 5,
    "retry_delay" : timedelta(minutes = 5)
}

with DAG(
    dag_id = "dag_postgres_operator_v4",
    description = "A DAG that connects to PostgreSQL database",
    start_date = datetime(2024, 4, 1),
    schedule_interval = "@daily",
    default_args = default_args
) as dag:
    task1 = PostgresOperator(
        task_id = "create_postgres_table",
        postgres_conn_id = "postgres_localhost",
        sql = """create table if not exists dag_runs (
        dt date,
        dag_id character varying,
        primary key (dt, dag_id)
        );"""
    )

    task2 = PostgresOperator(
        task_id = "delete_from_table",
        postgres_conn_id = "postgres_localhost",
        sql = "delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}';"
    )

    task3 = PostgresOperator(
        task_id = "insert_into_table",
        postgres_conn_id = "postgres_localhost",
        sql = "insert into dag_runs values ( '{{ ds }}', '{{ dag.dag_id }}');"

    # ds and dag_id are macros that reference airflow metadata. ds is the current date.
    )
    task1 >> task2 >> task3