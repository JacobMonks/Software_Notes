# GCP Cloud Composer

Cloud Composer is a fully managed workflow orchestration service built on top of Apache Airflow.

- Create, schedule, and observe end-to-end pipelines in multi-cloud and hybrid environments.
- Provides an easy way to transition to the cloud and create a unified data environment.
- Airflow is open-source, offering integration with a wide and ever-expanding variety of platforms.
- One-click deployment and multiple options for graphical representations, making troubleshooting easy.

### IAM Permissions:

1. Composer Administrator

- Provides full cnotrol over all Composer functions and resources.

2. Composer User

- Provides the necessary permissions to list and get Composer environments and operations.

## Create a Composer Environment

1. Select composer type (Composer 1 or Composer 2).

- The only difference is Composer 2 has auto-scaling and Composer 1 does not.

2. Give a name and location.

3. Choose the Image version.

- This creates the environment with the designated version of Airflow with pre-installed Python packages.

4. Select service account.

- By default it will use the Compute Engine service account. This is fine for demos.
- In production environments, you should use a dedicated service account or create a new one and grant it IAM permissions.

5. Give the environment labels (if desired).

6. Select the size of environment resources.

- It will list all the resources below including the number of schedulers, number of workers, and amount of memory.

7. You can optionally customize the VPC configuration, data encryption, and the maintenance schedule.

8. When all settings are to your liking, click "Create." The creation process may take some time because the server is executing a lot of processes.

## Navigating Cloud Composer Environment
Once your environment has been created, you will see options for DAGs, Logs, and Airflow webserver.

### Environment Details
You can see all the settings of the Environment by clicking on the blue hypertext link on the environment name.

Here, you can see and edit many details including:

- Environment Configuration
- Logs
- DAGs
- Airflow Configuration Overrides
- Environment Variables
- Installed PyPI Packages
- Labels

### DAGs
This is where you will deploy your finished Python DAG files. There should be one example DAG that exists after your environment is created.

### Webserver
This is where you can see all your available DAGs and can manually trigger or monitor their execution.

