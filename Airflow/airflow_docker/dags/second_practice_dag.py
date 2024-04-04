from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner" : "Jacob Monks",
    "retries" : 5,
    "retry_delay" : timedelta(minutes = 2)
}

with DAG(
    dag_id = "second_practice_dag_v2",
    description = "This is a DAG for practicing Cron expressions and the PostgresOperator.",
    start_date = datetime(2024, 4, 2),
    schedule_interval = "0 0 * * *",
    default_args = default_args
) as dag:
    
    task1 = BashOperator(
        task_id = "startup",
        bash_command = "echo Starting Postgres Task..."
    )

    task2 = PostgresOperator(
        task_id = "create_table",
        postgres_conn_id = "postgres_localhost",
        sql = """
            create table if not exists practice_table (
                dt date,
                dag_run VARCHAR(63),
                name VARCHAR(63),
                primary key (dt, dag_run)
            );
"""
    )
    task3 = PostgresOperator(
        task_id = "delete_duplicate_data",
        postgres_conn_id = "postgres_localhost",
        sql = """
            delete from practice_table
            where dt = '{{ ds }}'
            and dag_run = '{{ dag.dag_id }}';
"""
    )
    task4 = PostgresOperator(
        task_id = "insert_data",
        postgres_conn_id = "postgres_localhost",
        sql = """
            insert into practice_table values ('{{ ds }}', '{{ dag.dag_id}}', 'Eric Suminski');
"""
    )

    task5 = BashOperator(
        task_id = "finish",
        bash_command = "echo Dag Run Completed."
    )

    task1 >> task2 >> task3 >> task4 >> task5