# Apache Airflow
more info: https://airflow.apache.org/docs/

## What is Airflow?

Airflow is an open-source tool that allows us to create, schedule, and monitor a workflow.
It is very useful when you have multiple tasks that must be executed regularly and in a specific order.

Airflow operates using Directed Acyclic Graphing (DAG), which is a way of breaking down jobs into tasks and assigning them a schedule and the necessary resources to complete them.

A simple example of DAG:

     / B -> D \
A ->|          |-> F
     \ C -> E /

- This graph shows 6 tasks that must be executed: A, B, C, D, E, and F.
- It also shows that A must be completed first before any other tasks.
- In the same way, tasks D and E are reliant on B and C, respectively, and F is reliant on both D and E.

A DAG will typically also include how frequently the DAG must be run.

### Installing and Setting up Airflow

Create and open a new Python project.
Using a WSL terminal, navigate to the correct directory and start a virtual environment:
'''
    py -m venv py_env
'''

Go to: https://github.com/apache/airflow?tab=readme-ov-file
OR search for "Apache Airflow official GitHub repository"
Scroll down and click the link: "Installing from PyPI"

Copy the command:
'''
    sudo pip install 'apache-airflow==2.8.3' \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.3/constraints-3.8.txt"
'''
Change the name of the constraints text file so that it matches your version of Python.

Set the project folder as the Airflow Home directory:
'''
    export AIRFLOW_HOME=~/airflow
'''

Set up the Airflow database using the following command:
'''
    airflow db init
'''

Create a new user:
'''
    airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com
'''

And create a memorable password.

Then start the Airflow webserver:
'''
    airflow webserver -p 8080
'''

Now you can see the Airflow dashboard when you go to "http://localhost:8080" and login.

Open a new WSL terminal, locate the project directory, and enter the following commands:
'''
export AIRFLOW_HOME=~/airflow
airflow scheduler
'''

## Declaring a DAG:

There are 3 main ways to declare a DAG:

1. Context Manager

    This will add the DAG to anything inside it implicitly.

    '''
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        with DAG(
            dag_id = "my_dag_name",
            start_date = datetime.datetime(YYYY,M,D),
            schedule = "@daily",
        ):
            EmptyOperator(task_id = "task")

    '''

2. Standard Constructor

    With this, you pass the DAG into any operator you use.

    '''
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        my_dag = DAG(
            dag_id = "my_dag_name",
            start_date = datetime.datetime(YYYY,M,D),
            schedule = "@daily",
        )
        EmptyOperator(task_id = "task", dag = my_dag)
    '''

3. Decorator

    Using the @dag decorator, you can turn a function into a DAG generator.

    '''
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        @dag(start_date = datetime.datetime(YYYY,M,D), schedule = "@daily")
        def generate_dag():
            EmptyOperator(task_id = "task")
        
        generate_dag()
    '''

DAGs are nothing without Tasks, and those usually come in the form of Operators, Sensors, or Taskflows.

Tasks come with dependencies, that is, tasks that must come before it (upstream) and tasks that follow after it (downstream).
You can declare task dependencies in a few ways:

1. Using << and >>
    '''
        first-task >> [second_task, third_task]
        third_task << fourth_task
    '''

2. Using set_upstream and set_downstream
    '''
        first_task.set_downstream([second_task, third_task])
        third_task.set_upstream(fourth_task)
    '''

3. For more complex dependencies, such as having two lists of tasks that depend on all parts of each other, you must use cross_downstream().
    '''
        from airflow.models.baseoperator import cross_downstream

        # The equivalent using << and >> would be:
        # [op1, op2] >> op3
        # [op1, op2] >> op4
        cross_downstream([op1, op2], [op3, op4])
    '''

4. To chain together dependencies, you can use chain()
    '''
        from airflow.models.baseoperator import chain
        from airflow.operators.empty import EmptyOperator

        # The equivalent of op1 >> op2 >> op3 >> op4
        chain(op1, op2, op3, op4)

        # You can also chain dynamically.
        chain(*[EmptyOperator(task_id = 'op' + i) for i in range(1,6)])

        # You can also use this for pairwise dependencies,
        # like in the example DAG near the beginning of this page.
        # op1 >> op2 >> op4 >> op6
        # op1 >> op3 >> op5 >> op6
        chain(op1, [op2, op3], [op4, op5], op6)
    '''

### Loading DAGs
DAGs are loaded from Python source files. You can define multiple DAGs in the same file or have one DAG split across multiple files.

Note: Airflow will only load DAGs from the top level. DAGs that exist in local or enclosed scopes won't be found.

Airflow will load DAGs from the "DAG_FOLDER" directory, and by default it will only consider files that contain the strings "dag" and "airflow".

You can create a .airflowignore file inside the DAG_FOLDER that describes patterns of files for the loader to ignore.
