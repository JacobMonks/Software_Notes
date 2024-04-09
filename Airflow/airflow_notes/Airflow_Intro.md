# Apache Airflow
more info: https://airflow.apache.org/docs/

## What is Airflow?

Airflow is an open-source tool that allows us to create, schedule, and monitor a workflow. It is very useful when you have multiple tasks that must be executed regularly and in a specific order.

Airflow operates using Directed Acyclic Graphing (DAG), which is a way of breaking down jobs into tasks and assigning them a schedule and the necessary resources to complete them.

### Installing and Setting up Airflow

#### Option 1: Using Python Virtual Environment

1. Create and open a new Python project called 'airflow_tutorial'. Using a WSL terminal, navigate to the correct directory and start a virtual environment:

    py -m venv py_env

2. Activate the virtual environment:

    source py_env/bin/activate

3. Go to: https://github.com/apache/airflow?tab=readme-ov-file OR search for "Apache Airflow official GitHub repository".

4. Scroll down and click the link: "Installing from PyPI".

5. Copy the command:

    sudo pip install 'apache-airflow==2.8.3' \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.3/constraints-3.8.txt"

6. Change the name of the constraints text file so that it matches your version of Python.

7. Set the project folder as the Airflow Home directory:

    export AIRFLOW_HOME=~/airflow

8. Set up the Airflow database using the following command:

    airflow db init

9. Create a new user with a memorable password:

    airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com

10. Then start the Airflow webserver:

    airflow webserver -p 8080

Now you can see the Airflow dashboard when you go to "http://localhost:8080" and login.

11. Open a new WSL terminal, locate the project directory, and enter the following commands:

    export AIRFLOW_HOME=~/airflow
    airflow scheduler

#### Option 2: Using a Docker Container

1. Create a new project called 'airflow_docker' and open it up. If you don't have Docker, you can install it at: 
https://docs.docker.com/desktop/install/windows-install/

2. If you have docker installed, you can run the following command in a terminal to get the yaml file:

    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.3/docker-compose.yaml'

Note: To ensure you have enough memory (roughly 8 GB), use the following command:

    docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
    
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

