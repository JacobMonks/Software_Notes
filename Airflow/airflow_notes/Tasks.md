# Airflow Tasks

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

## Cron Expressions
When scheduling a task, instead of using the datetime library, you can use a Cron Expression for scheduling.

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