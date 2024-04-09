# Installing Python Packages in Airflow
There are two ways to install Python packages for Airflow when using a Docker container:

### Extend the docker image
1. Create a new text file in the directory called 'requirements.txt'.
2. Fill the requirements file with the list of packages (with version numbers if necessary) versions. For example:

    scikit-learn==1.3.2
    matplotlib

3. Create a Dockerfile in the directory to extend the image.

    FROM apache/airflow:2.8.3
    COPY requirements.txt /requirements.txt
    RUN pip install --user --upgrade pip
    RUN pip install --no-cache-dir --user -r /requirements.txt

4. Using the terminal, input the command to build the container:

    docker build . --tag extending_airflow:latest

5. Edit the .yaml file and change the image name to the new tag you just created.

    image: ${AIRFLOW_IMAGE_NAME:-extending_airflow:latest}

6. Run the container with the new image:

    docker compose up -d --no-deps --build airflow-webserver airflow-scheduler

### Customize the image
1. Clone the Airflow source code from the Github. Then go to the directory called 'docker-context-files' and add the requirements.txt.

2. You can build the container with the following command:

    docker build . --build-arg AIRFLOW_VERSION='2.8.3' --tag customizing_airflow:latest

3. Just like extending the image, edit the .yaml file with the new image name:

    image: ${AIRFLOW_IMAGE_NAME:-customizing_airflow:latest}

4. Run the container with the new image:

    docker compose up -d --no-deps --build airflow-webserver airflow-scheduler