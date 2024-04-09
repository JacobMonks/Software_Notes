
# DAG Visualization

## Task Groups
Purely for UI purposes and removing clutter, Task Groups can be added to your code using the @task_group() decorator.

Ex.

    from airflow.decorators import task_group

    @task_group()
    def group1():
        task1 = EmptyOperator(task_id = "task1")
        task2 = EmptyDecorator(task_id = "task2")
    
    task3 = EmptyOperator(task_id = "task3")

    group1() >> task3

Task Groups also support the "default_args" argument like DAG:

Ex.

    from airflow import DAG
    from airflow.decorators import task_group
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator

    with DAG(
        dag_id = "dag1",
        start_date = datetime.datetime(2025,1,1),
        schedule = "@daily",
        default_args = {"retries": 1}
    ):
        @task_group(default_args = {"retries":3})
        def group1():
            task1 = EmptyOperator(task_id = "task1")
            task2 = BashOperator(task_id = "task2", bash_command = "echo Hello World!", retries = 2)
            print(task1.retries) # 3
            print(task2.retries) # 2

### Edge Labels
Airflow also allows you to add labels to edges that will appear in the graph.

For example, you have a DAG with two branches, one that executed when errors occur and another that executes when no errors occur. You can make those purposes clear by adding Edge Labels:

    from airflow.utils.edgemodifier import Label

    check >> Label("No Errors") >> save >> report
    check >> Label("Errors Found") >> describe >> error >> report
