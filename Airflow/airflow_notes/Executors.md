# Airflow Configuration and APIS

## Executors
Executors are what run your DAGs and task instances in Airflow. You can swap Executors based on your installation needs.

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

### Executor Configuration
Some Executors allow optional per-task configuration. One example is the KubernetesExecutor, which allows you to set an image for the task to run on.

This is done using the "executor_config" argument in the Operator. The example below sets a Docker image to run a task with the KubernetesExecutor:

    MyOperator(
        executor_config = {
            "KubernetesExecutor" : { "image" : "CustomDockerImage" }
        }
    )

