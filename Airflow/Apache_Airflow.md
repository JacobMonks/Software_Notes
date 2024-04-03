# Apache Airflow
more info: https://airflow.apache.org/docs/

## What is Airflow?

Airflow is an open-source tool that allows us to create, schedule, and monitor a workflow. It is very useful when you have multiple tasks that must be executed regularly and in a specific order.

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

Create and open a new Python project. Using a WSL terminal, navigate to the correct directory and start a virtual environment:

    py -m venv py_env

Activate the virtual environment:

    source py_env/bin/activate

Go to: https://github.com/apache/airflow?tab=readme-ov-file

OR search for "Apache Airflow official GitHub repository".

Scroll down and click the link: "Installing from PyPI".

Copy the command:

    sudo pip install 'apache-airflow==2.8.3' \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.3/constraints-3.8.txt"

Change the name of the constraints text file so that it matches your version of Python.

Set the project folder as the Airflow Home directory:

    export AIRFLOW_HOME=~/airflow

Set up the Airflow database using the following command:

    airflow db init

Create a new user:

    airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com

And create a memorable password.

Then start the Airflow webserver:

    airflow webserver -p 8080

Now you can see the Airflow dashboard when you go to "http://localhost:8080" and login.

Open a new WSL terminal, locate the project directory, and enter the following commands:

    export AIRFLOW_HOME=~/airflow
    airflow scheduler

## Declaring a DAG:

There are 3 main ways to declare a DAG:

1. Context Manager

    This will add the DAG to anything inside it implicitly.
    
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        with DAG(
            dag_id = "my_dag_name",
            start_date = datetime.datetime(YYYY,M,D),
            schedule = "@daily",
        ):
            EmptyOperator(task_id = "task")

2. Standard Constructor

    With this, you pass the DAG into any operator you use.

    
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        my_dag = DAG(
            dag_id = "my_dag_name",
            start_date = datetime.datetime(YYYY,M,D),
            schedule = "@daily",
        )
        EmptyOperator(task_id = "task", dag = my_dag)
    
3. Decorator

    Using the @dag decorator, you can turn a function into a DAG generator.
    
        import datetime
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        @dag(start_date = datetime.datetime(YYYY,M,D), schedule = "@daily")
        def generate_dag():
            EmptyOperator(task_id = "task")
        
        generate_dag()
    
DAGs are nothing without Tasks, and those usually come in the form of Operators, Sensors, or Taskflows.

Tasks come with dependencies, that is, tasks that must come before it (upstream) and tasks that follow after it (downstream). You can declare task dependencies in a few ways:

1. Using << and >>
    
        first-task >> [second_task, third_task]
        third_task << fourth_task
    
2. Using set_upstream and set_downstream
    
        first_task.set_downstream([second_task, third_task])
        third_task.set_upstream(fourth_task)
    
3. For more complex dependencies, such as having two lists of tasks that depend on all parts of each other, you must use cross_downstream().
    
        from airflow.models.baseoperator import cross_downstream

        # The equivalent using << and >> would be:
        # [op1, op2] >> op3
        # [op1, op2] >> op4
        cross_downstream([op1, op2], [op3, op4])
    
4. To chain together dependencies, you can use chain():
    
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
    
## Loading DAGs
DAGs are loaded from Python source files. You can define multiple DAGs in the same file or have one DAG split across multiple files.

Note: Airflow will only load DAGs from the top level. DAGs that exist in local or enclosed scopes won't be found.

Airflow will load DAGs from the "DAG_FOLDER" directory, and by default it will only consider files that contain the strings "dag" and "airflow".

You can create a .airflowignore file inside the DAG_FOLDER or its subdirectories that describes patterns of files for the loader to ignore.

## Running DAGs
DAGs can either be triggered manually or be executed on a schedule (the schedule defined in the DAG).

There are multiple valid values for the "schedule" property when defining a DAG:

- DAG(dag_id = "daily_dag", schedule = "0 0 * * *")
- DAG(dag_id = "one_time_dag", schedule = "@once")
- DAG(dag_id = "my_continuous_dag", schedule = "@continuous")

When you run a DAG, you are creating a new instance of that DAG, which Airflow calls a "DAG Run". DAG Runs can run in parallel using the same DAG, and you can specify a data interval for the tasks to operate on.

Every task you wish to run must be assigned a to DAG.

### Default Arguments:
Operators inside a DAG usually need to be given default arguments. Rather than specify them one by one for each Operator, you can pass "default_args" in a dictionary format that will apply to all Operators.

Ex.

    import pendulum
    
    with DAG(
        dag_id = "task_name",
        start_date = pendulum.datetime(2025,1,1),
        schedule = "@daily",
        default_args = {"retries":2}
    ):
        op = BashOperator(task_id = "hello_world", bash_command = "Hello World!")
        print(op.retries)

## DAG Control Flow
By default, a DAG will only run a task once all the other tasks it depends on are complete. However, this can be modified in a few ways:

- Branching: Selecting which task to move on to based on a condition.
- Trigger Rules: Set conditinos under which a DAG will run a task.
- Setup and Teardown: Define setup and teardown relationships.
- Latest Only: A form of branching that only runs on DAGs running against the present.
- Depends on Past: Tasks can depend on themselves from a previous run.

### Branching
You can make use of branching to tell a DAG not to run all dependent tasks, but instead choose between different paths to go down.

This is done with the "@task.branch" decorator.
When a function has this decorator, it must return an ID of a task so it knows which task to branch to. If it returns None, it will skip all downstream tasks.

Ex.

    @task.branch
    def branch_func(ti = None):
        xcom_value = int(xcom_pull(task_ids = "start_task"))
        if xcom_value > 5:
            return "continue_task"
        elif xcom_value >= 3:
            return "stop_task"
        else:
            return None

    start_op = BashOperator(
        task_id = "start_task",
        bash_command = "echo 5",
        do_xcom_push = True,
        dag = dag,
    )

    branch_op = branch_func()

    continue_op = EmptyOperator(task_id = "continue_task", dag = dag)
    stop_op = EmptyOperator(task_id = "Stop_task", dag = dag)

    start_op >> branch_op >> [continue_op, stop_op]


To create your own Branching operators, you can inherit from "BaseBranchOperator" and implement the "choose_branch" method to meet your needs.

Ex.

    class MyBranchOperator(BaseBranchOperator):
        def choose_branch(self, context):
            """
                Run an extra branch on the first day of the month.
            """
            if context['data_interval_start'].day == 1:
                return ['daily_task_id', 'monthly_task_id']
            elif context['data_interval_start'].day == 2:
                return 'daily_task_id'
            else:
                return None

### Latest Only
Airflow allows you to run tasks on data that is days or even months old. You can run one copy of the DAG for every day to backfill some data.

However, in some situations you might not want some (or all) parts of a DAG to run on previous data. This is where the "LatestOnlyOpeator" comes in handy. This will skip all downstream tasks if you are not on the "latest" DAG Run.

Ex.

    import pendulum
    import datetime
    from airflow.operators.latest_only import LatestOnlyOperator
    from airflow.operators.empty import EmptyOperator
    from airflow.models.dag import DAG
    from airflow.utils.trigger import TriggerRule

    with DAG(
        dag_id = "latest_only_with trigger",
        schedule = datetime.timedelta(hours = 4),
        start_date = pendulum.datetime(2025,1,1, tx = "UTC"),
        catchup = False,
        tags = {"example3"},
    ) as dag:
        latest_only = LatestOnlyOperator(task_id = "latest_only")
        task1 = EmptyOperator(task_id = "task1")
        task2 = EmptyOperator(task_id = "task2")
        task3 = EmptyOperator(task_id = "task3")
        task4 = EmptyOperator(task_id = "task4", trigger_rule = TriggerRule.ALL_DONE)

        latest_only >> task1 >> [task3, task4]
        task2 >> [task3, task4]
        # In this DAG:
        # task1 will be skipped for all except the latest instance.
        # task2 is independent of latest_only and will run in all instances.
        # task3 is downstream from task1, so it will also be skipped for all except the last instance.
        #         This is because the default trigger rule is "ALL_SUCCESS"
        # task4 has a trigger rule of "ALL_DONE", so it will run in all instances.

### Depends on Past
You can set your task to run only if the task in the previous DAG Run was successful.

This is done simply by setting the "depends_on_past" argument in the "default_args" to True.

Note: If this is the first ever instance of this DAG, then the task will still run.

### Trigger Rules

- all_success (default)
- all_failed
- all_done
- all_skipped
- one_failed
- one_success
- one_done
- none_failed
- none_failed_min_one_success
- none_skipped
- always

Be wary of using these triggers when skipping branches. You almost never want to use the "all_success" or "all_failed" triggers downstream of a branching operation.

Consider the following DAG:

                 / branch_a -> follow_branch_a \
    branching ->|                               |-> join
                 \------ skipped_branch -------/

If the trigger on the "join" task is "all_success", it will be skipped always, because skipped_branch is upstream of it, and it did not succeed.

In this case, you may want the trigger to be "none_failed_min_one_success".

### Setup and Teardown
In a lot of cases, you might be creating some resources, like a cluster, using it for a purpose, and then getting rid of it.

Airflow supports this setup and teardown workflow:

    create_cluster >> run_query >> delete_cluster.as_teardown(setups = create_cluster)

You can also have it written as such:

with delete_cluster.as_teardown(setups = create_cluster()):
    [RunQueryONe(), RunQuery2()] >> DoStuff()
    WorkOne() >> [DoMoreStuff(), DoSomeOtherstuff()]

This will create the cluster, use it to run all of the tasks in the context, then delete the cluster afterwards.

## DAG Visualization

### Task Groups
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

## Packaging DAGs
Simpler DAGs are usually confined to a single Python file, but more complex DAGs may be spread across multiple files and have added dependencies that must be shipped along with them.

You can either use the DAG_FOLDER with a standard file system layout, or you can package the Python files as a single zip file.

Ex.

    dag1.py
    dag2.py
    package1/__init__.py
    package1/functions.py

Packaged DAGs come with caveats:

- They cannot be used if you have pickling enabled for serialization.
- They cannot contain compiled libraries, only pure Python.
- They will be inserted into Python's 'sys.path' and can be imported by any other project in the Airflow process, so you must ensure that the package names don't clash with other packages on the system.

Generally, for more complex sets of dependencies, it is a good idea to just use a Python virtual environment and install necessary packages with pip.

## DAG Dependencies
Within a DAG, the task dependencies can be defined by using the upstream and downstream notations, but dependencies between different DAGs require something more nuanced. DAGs can be dependent on each other for a few reasons:

1. triggering - TriggerDagRunOperator
2. waiting - ExternalTaskSensor

To view all DAG dependencies on the Airflow dashboard, you can click on the DAG, hover over "Browse", and select "DAG Dependencies".

## Pausing, Deactivation, and Deletion
Using the UI or API, DAGs can be paused and unpaused. When a DAG is paused, any currently running task is completed and all downstream tasks are put in a state of "Scheduled".

DAGs can also be deactivated by removing them from the DAGS_FOLDER. The metadata and run history for this DAG will be maintained, and it can be added back into the DAGS_FOLDER to be reactivated. This cannot be done using the UI or API.

Using the UI or API, you can also delete DAGs. However, if it is not removed from the DAGS_FOLDER, the scheduler will be able to find it again, so deleting the DAG only deletes its metadata and run history.

So if you wish to fully remove a DAG from the processes, you must do 3 steps:

1. Pause the DAG via UI or API.
2. Delete the metadata via UI or API.
3. Remove it from DAGS_FOLDER.

## DAG Runs
DAG Runs are instances of a DAG being executed. Each DAG Run is separate, so you can have multiple DAG Runs at the same time using the same DAG. This allows for parallelism.

DAG Runs will be given a status after all of its tasks have a finished status (success, failed, or skipped). DAG Runs will have one of two states after completing:

1. Success (if all leaf nodes' states are either "success" or "skipped")
2. Failed (if any leaf node state is either "failed" or "upstream_failed")

### Data Interval
Each DAG Run has an assigned "data interval" that reprsents the time range it operates in. A dag with schedule = "@daily" will have a data interval starting from 00:00 and ending at 24:00.

DAG Runs are usually scheduled to run after the data interval has ended to ensure it is able to collect all the associated data. The "logical date" denotes the time that the DAG Run's data interval begins, not when it actually executes.

This means that a DAG will only run after a full interval has passed the "start_date".

### Re-running DAGs
If you ever need to run a DAG an additional time, or the original run failed, Airflow has options that allow you to get back on track:

1. Catchup
2. Backfilling
3. Re-run tasks.

By default, the scheduler will make new DAG Runs for every interval that has not been run since the last data interval (or has been cleared). This is known as CATCHUP.

If your DAG is not limited to specific intervals, you can turn Catchup off when defining the DAG:

    import pendulum
    import datetime
    from airflow.models.dag import DAG
    from airflow.operators.bash import BashOperator

    with DAG(
        dag_id = "tutorial",
        default_args = {
            "depends_on_past" : True,
            "retries" : 3,
            "retry_delay" : datetime.timedelta(minutes = 3)
        },
        start_date = pendulum.datetime(2025,1,1, tz = "UTC"),
        schedule = "@daily",
        description = "A simple tutorial DAG",
        catchup = False,
    )

In the above DAG, with Catchup set to False, the scheduler will only execute a DAG Run for the previous day, after midnight on the day it was activated.

If Catchup is set to True, the scheduler will create a DAG Run for each interval since 1/1/2025 that has passed, and they will execute sequentially.

Let's say a DAG start_date is 12/1/2020, but someone wants to execute a DAG Run on data from the previous month. This is called BACKFILLING, and it can be done using CLI commands:

Ex.

    airflow dags backfil \
        -- start-date START_DATE \
        -- end-date END_DATE \
        dag_id

When tasks fail during a scheduled run, you can fix the problem and clear it for the scheduled date. Clearing it will reset the "max_tries" to 0 and set the task instance state to None, prompting the scheduler to re-run it.

Re-run options:

- Past - All instances of the task before the most recent data interval.
- Future - All instances of the task after the most recent interval.
- Upstream - The upstream tasks in the current DAG.
- Downstream - The downstream tasks in the current DAG.
- Recursive - All the tasks in the parent and child DAGs.
- Failed - Only the failed tasks in the most recent DAG Run.

You can clear tasks using CLI commands:

Ex.

    airflow tasks clear dag_id \
        --task-regex task_regex \
        --start-date START_DATE \
        --end-date END_DATE

This will clear all tasks that match the regex for the specified dag_id and time interval.

### External Triggers
You can create a DAG Run manually using the CLI:

    airflow dags trigger --exec-date logical_date run_id

You can also trigger them using the Airflow UI with: DAGs >> Links >> Trigger DAG.

### Parameterized DAGs
When triggering a DAG from the UI, API, or CLI, you can pass in configuration as a JSON blob.

Ex.

    import pendulum
    import datetime
    from airflow import DAG
    from airflow.operators.bash import BashOperator

    dag = DAG(
        dag_id = "example_parameterized_dag",
        schedule = None,
        start_date = pendulum.datetime(2025,1,1, tz = "UTC"),
        catchup - False,
    )

    parameterized_task = BashOperator(
        task_id = "parameterized_task",
        bash_command = "echo value: {{ dag_run.conf['conf1'] }}",
        dag = dag,
    )

The parameters from dag_run.conf can only be used in a template of an operator.

Using CLI:

    airflow dags trigger --conf '{ "conf1" : "value1" }' example_parameterized_dag

## Tasks
Tasks are the basic units of execution in Airflow.

There are 3 basic types of Tasks:

1. Operators - Predefined task templates that you can string together quickly to build most parts of your DAG.
2. Sensors - A subclass of Operator that waits for specific external events to happen.
3. TaskFlows - decorated @task, which is a custom Python function packaged up as a task.

Essentially, think of Operators and Sensors as templates that you call in a DAG to create tasks.

Tasks don't pass information to each other and instead run independently. If you wish to pass information from one task to another, you should instead use XComs.

### Task Instances
Just like a DAG is instantiated into a DAG Run, a Task is instantiated into a Task Instance.

Task Instances have an indicated state:

- none - The task is not queued and its dependencies are not met.
- scheduled - The scheduler has determined that the dependencies have been met and it should run.
- queued - The task has been assigned to an executor and is awaiting a worker.
- running - The task is running on a worker.
- success - The task completed without errors.
- restarting - The task was externally requested to restart while it was running.
- failed - The task encountered errors while executing.
- skipped - The task was skipped over due to branching, LatestOnly, or some other condition.
- upstream_failed - An upstream task and the Trigger Rule says we needed it to succeed.
- up_for_retry - The task failed but it has retries left and is rescheduled.
- up_for_reschedule - The task is a Sensor that is in "reschedule" mode.
- deferred - The task has been deferred to a Trigger.
- removed - The task was removed from the DAG since the Run started.

Task terminology:

- Upstream task: a task that executes before this task.
- Downstream task: a task that executes after thsi task.
- Previous task: the task in a previous DAG Run.
- Next task: the task in a future DAG Run.

### Timeouts
When creating a task from an Operator or Sensor, you can set the "execution_timeout" attribute to set a maximum allotted time for the task to complete. Use datetime.timedelta to specify a value.

Sensors specifically also have a "timeout" attribute for when it is in "reschedule" mode. When in this mode, the sensor is periodically executed and rescheduled until it succeeds.

Ex.

    sensor = SFTPSensor(
        task_id = "example_sensor",
        path = "/root",
        execution_timeout = datetime.timedelta(seconds = 60),
        timeout = 3600,
        retries = 2,
        mode = "reschedule",
    )

In the above example, the Sensor is given 60 seconds to poke the SFTP server. If it takes longer than 60 seconds, AirflowTaskTimout will be raised, and it will be allowed 2 more attempts. From the time of execution until it succeeds, it is given 3600 seconds, or 60 minutes. If it does not succeed, AirflowSensorTimeout will be raised, and it will not be allowed to retry.

### SLAs
A Service Level Agreement (SLA) is an expectation for the maximum time to complete a task relative to the DAG start_time. Unlike timeout, SLA parameters do not set a maximum limit for the task to be run, but instead it will send an "SLA miss" notification if it takes longer. Tasks that run over SLA are still allowed to complete.

Tasks that are manually trigger or tasks in an event-driven DAG will not be checked for SLA miss.

You can code your own logic in the case of an SLA miss using "sla_miss_callback".

Ex.

    def sla_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
        print(
            "The callback arguments are: ",
            {
                "dag" : dag,
                "task_list" : task_list,
                "blocking_Task_list" : blocking_task_list,
                "slas" : slas,
                "blocking_tis" : blocking_tis,
            },
        )

    @dag(
        schedule = "*/2 * * * *",
        start_date = pendulum.datetime(2025,1,1, tz = "UTC"),
        caatchup = False,
        sla_miss_callback = sla_callback,
        default_args = { "email" : "email@domain.com" }
    )
    def example_sla_dag():
        @task(sla = datetime.timedelta(seconds = 10))
        def sleep_20():
            time.sleep(20)
        
        @task
        def sleep_30():
            time.sleep(30)
    
        sleep_20() >> sleep_30()

    example_dag = example_sla_dag()

### Zombie/Undead Tasks
Task instances are expected to die every once in a while because no system is perfect.

Zombie Tasks are TaskInstances stuck in a "running" state despite their associated jobs being inactive. Airflow will find these periodically and clean them up to either retry them or fail them.

Undead Tasks are tasks that are not supposed to be running but are, usually as a result of manually editing the Task Instance in the UI. Airflow will find these periodically and terminate them.

### Executor Configuration
Some Executors allow optional per-task configuration. One example is the KubernetesExecutor, which allows you to set an image for the task to run on.

This is done using the "executor_config" argument in the Operator. The example below sets a Docker image to run a task with the KubernetesExecutor:

    MyOperator(
        executor_config = {
            "KubernetesExecutor" : { "image" : "CustomDockerImage" }
        }
    )

## Operators
An Operator is a template for a predefined Task that you can call declaratively in a DAG.

Many Operators are supported, including:

- EmptyOperator
- BashOperator - executes a bash command.
- PythonOperator - calls a Python function (it's preferred to use the @task decorator instead).
- EmailOperator - sends an email.

There are also many community-created Operators you can install:

- HttpOperator
- MySqlOperator
- OracleOperator
- JdbcOperator
- DockerOperator
- HiveOperator
- S3FileTransformOperator
- SlackAPIOperator

When using certain Operators, the executor will recognize certain suffixes of strings as references to files.

Here's an example of a BashOperator that executes a multi-line bash script from a file.

    run_script = BashOperator(
        task_id = "run_script",
        bash_command = "script.sh",
    )

If you wish to execute a bash command on that script, however, you should use the "literal" wrapper.

    from airflow.utils.template import literal

    print_script = BashOperator(
        task_id = "print_script",
        bash_command = literal("cat script.sh"),
    )

## Sensors
Sensors are Operators that wait for something to happen. This could be a manual trigger, a time-based event, or a file being read. As a result, Sensors are primarily idle.

There are two primary modes for running Sensors:

1. Poke (default) - The Sensor takes up a worker slot for its entire runtime.
2. Reschedule - The Sensor takes up a worker slot only when it is checking, and then goes to sleep for a set duration between checks.

The main difference is latency. If a task needs to be executed every second, Poke should be the chosen mode. If a task only needs to be run every few minutes, Reschedule is preferred.

Just like Operators, Airflow has many pre-built Sensors.

## TaskFlow
This is a new feature from Airflow 2.0.

The TaskFlow API allows you to write DAGs much easier with basic Python code using the "@task" decorator.

TaskFlow uses XComs to take care of moving inputs and outputs between tasks and automatically calculating dependencies. Take the below example:

    from airflow.decorators import task
    from airflow.operators.email import EmailOperator

    @task
    def get_ip():
        return my_ip_service.get_main_zip()

    @task(multiple_outputs = True)
    def compose_email(external_ip):
        return {
            'subject' : f'Server connected from {external_ip}',
            'body' :  f'Your Server executing Airflow is connected from the external ip {external_ip}.<br>'
        }

    email_info = compose_email(get_ip())

    EmailOperator(
        task_id = "send_email",
        to = "email@example.com",
        subject = email_info["subject"],
        html_content = email_info["body"]
    )

The TaskFlow will automatically determine from line 733 that "compose_email" is downstream from "get_ip". And from the EmailOperator, it will also determine that it is upstream from the "send_email" task.

### Context
You can access TaskFlow context variables by adding them as keyword arguments.

Ex.

    from airflow.models.taskinstance import TaskInstance
    from airflow.decorators import task
    from airflow.models.dagrun import DagRun

    @task
    def print_ti_info(task_instance : TaskInstance | None = None, dag_run = DagRun | None = None):
        print( f"Run ID: {task_instance.run_id}" )
        print( f"Duration: {task_instance.duration}" )
        print( f"DAG Run queued at: {dag_run.queued_at}" )

### Logging
Python's standard logging package will also work for logging TaskFlows.

    import logging

    logger = logging.getLogger("airflow.task")

### Passing Objects as Arguments
As mentioned, XComs pass variables into each task. One prerequisite, however, is that the variables used as arguments need to serializable.

Airflow supports all built-in types and any objects decorated with @dataclass or @attr.define. The below example shows a TaskFlow that uses a 'Dataset' object for storing the data from the specified link:

    import json
    import pendulum
    import requests
    from airflow import Dataset
    from airflow.decorators import task

    SRC = Dataset(
        "https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/ytd/12/1880-2022.json"
    )
    now = pendulum.now()

    @dag(dag_id = now, schedule = "@daily", catchup = False)
    def etl():
        @task()
        def retrieve(src : Dataset) -> dict:
            resp = requests.get(url = src.url)
            data = resp.json()
            return data["data"]
        
        @task()
        def to_fahrenheit(temps: dict[int, float]) -> dict[int, float]:
            ret: dict[int, float] = {}
            for year, celsius in temps.items():
                ret[year] = float(celsius) * 1.8 + 32
            
            return ret

        @task()
        def load(fahrenheit: dict[float, int]) -> Dataset:
            filename = "/tmp/fahrenheit.json"
            s = json.dumps(fahrenheit)
            f = open(filename, 'w')
            f.write(s)
            f.close()

            return Dataset(f"file:///{filename}")
        
        data = retrieve(SRC)
        fahrenheit = to_fahrenheit(data)
        load(fahrenheit)
    
    etl()

#### Passing Custom Objects
Typically, if you want to pass custom objects, you would decorate the class with @dataclasss or @attr.define.

Or, if you'd like to control serialization yourself, you can add the serialize() and deserialize() methods to the class:

    from typing import ClassVar

    class MyCustom:
        __version__: ClassVar[int] = 1

        def __init__(self, x):
            self.x = x

        def serialize():
            return dict({'x': self.x})
        
        @staticmethod
        def deserialize(data: dict, version: int):
            if version > 1:
                raise TypeError(f"version > {MyCustom.version}")
            return MyCustom(data['x'])

When diong serialization, it's a good idea to version the objects that will be serialized. Hence the code on line 822:

    __version__: ClassVar[int] = 1

## Executors
As mentioned previously, executors are what run your DAGs and task instances in Airflow. You can swap Executors based on your installation needs.

Airflow can only have one Executor configured at a time. To check which executor is currently set, you can run the following terminal command:

    airflow config get-value core executor

Airflow has executors for both local work and remote work.

Local:

- Sequential Executor (default executor, does not support parallel tasks)
- Local Executor (for small, single-machine production installations)

Remote:

- Celery Executor
- CeleryKubernetes Executor
- Kubernetes Executor
- Dask Executor
- LocalKubernetes Executor

All executors implement a common public interface, "BaseExecutor". If you want to configure a custom executor, inherit BaseExecutor.

BaseExecutor has some fundamental methods that you don't need to override:

- heartbeat
- queue_command
- get_event_buffer
- has_task
- send_callback

The following methods, however, MUST be implemented to create a custom executor:

- sync - gets called periodically during executor heartbeats
- execute_async

## Running Airflow in a Docker Container:
1. Open up a new project called 'airflow_docker'.

Note: To ensure you have enough memory (roughly 8 GB), use the following command:

    docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'

2. If you have docker installed, you can run the following command in a terminal to get the yaml file:

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'

3. Open up the yaml file and comment out any lines/blocks that apply to the 'CeleryExecutor', 'flower', or 'redis'.

4. Make new directories for keeping the logs, plugins, dags, and config:

    mkdir -p ./dags ./logs ./plugins ./config

5. Set the AIRFLOW_UID and save it in a .env file:

    echo -e "AIRFLOW_UID=$(id -u)" > .env

6. Create the docker container and initialize the database:

    docker compose up airflow-init

7. Start up the airflow processes in the container:

    docker compose up -d

8. Confirm that all the necessary processes are running. There should be a scheduler, webserver, triggerer, and postgres database:

    docker ps

9. Once you have confirmed it is running, you can go to "localhost:8080" and login using the following credentials:

    user: airflow
    password: airflow

## Cron Expressions
Instead of using the datetime library, you can use a Cron Expression for scheduling.

A Cron Expression consists of 5 fields separated by whitespace that represents a set of times. In Airflow's case, a Cron Expression can be used to indicate a schedule for task execution.

Here are some examples:

"@hourly"  = "0 * * * *"
"@daily"   = "0 0 * * *"
"@weekly"  = "0 0 * * 0"
"@monthly" = "0 0 1 * *"
"@yearly"  = "0 0 1 1 *"

The 5 positions correlate to: minute - hour - day of month - month - day of week

To find out what Cron Expression you need for your time interval, you can go to: crontab.guru

For example, you want a task to run hourly, but only on the 5th of March: "0 * 5 3 *"

Or you want this task to run at 3 PM every Monday and Thursday: "0 15 * * Mon,Thu"