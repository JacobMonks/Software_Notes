# Airflow APIs

## Airflow Postgres Connection:
Airflow UI has a handy feature to add new connections to databases. You can find this by going Admin > Conenctions.

In this case, let us create a new Postgres connection.

1. In your postgres/DBeaver client, create a new database and call it 'test'.

- Make sure the user credentials are easy to remember, such as username = airflow, password = airflow.
- Make sure the host is 'localhost' and the port is 5432.
- When everything is good, click 'test connection'.
- It may ask you to install the JDBC Driver for Postgres. Do that.

2. In the Airflow UI, go to Admin > Connections and create a new Postgres Connection called 'postgres_localhost' with the same information as the database we just created.

- If you are running Airflow in a Docker container, the value for 'host' must be 'host.docker.internal'. Otherwise, use 'localhost', you whatever other host you might be using.

3. Install the airflow postgres provider:

    pip install apache-airflow-providers-postgres

4. Create a new DAG with the dollowing import:

    from airflow.providers.postgres.operators.postgres import PostgresOperator

5. Create a new task with the PostgresOperator:

    task1 - PostgresOperator(
        task_id = "create_postgres_table",
        postgres_conn_id = "postgres_localhost",
        sql = "create table if not exists dag_runs (
            dt date,
            dag_run character varying,
            primary key(dt, dag_run)
        )
    )

