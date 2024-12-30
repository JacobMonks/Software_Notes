# Cloud Run and App Engine
Cloud Run and App Engine are both serverless computing services in Google Cloud. They do not require configuration of individual machines like Compute Engine, and they do not deal with cluster management like Kubernetes.

## Cloud Run
Cloud run is a fully managed service for running containerized applications. It supports scalable applications written in any language and integrates with developer tools like Cloud Build, Artifact Registry, and Docker.

There are two ways to run code using Cloud Run:
1. As a service.

    - Cloud Run services are used when your code must respond to web requests or specific events.

2. As a job.

    - Cloud Run jobs are used when your code runs until a workload is complete.
    
### Cloud Run Services
Cloud Run Services are well-suited for web applications, microservices, APIs, and stream data processing. Each Cloud Run service has an endpoint on a unique subdomain of the run.app domain. An endpoint can scale up to 1000 container instances by default, and you can request higher quotas or limit the number of containers to save on cost.

Cloud Run is used to deploy immutable versions of a service, so making any changes to the service would require a new container image to be deployed. You can run multiple different versions of the same service and route traffic between them. One use case for this is if you release a new version want to test it with a small amount of traffic.

Cloud Run services are deployed privately and require authentication to access. This is done via IAM policy, ingress settings, and Cloud Identity Aware Proxy (IAP).

- With IAM, you can grant developers permission to create new versions of a service with the run.developer role, or you can allow unathenticated access to make it publicly accessible.
- You can control access at the network level using ingress setting options. These include:
    1. Internal - only allow traffic by internal HTTP load balancers or resources within the VPC/project.
    2. Internal and Cloud Load Balancing - also allow traffic from external HTTP load balancers.
    3. All - allowed to run all requests sent to the endpoint.
- IAP is a security service that requires all traffic to come from proxies. Anybody trying to access the service must be authenticated and authorized by IAP.

#### Creating a Service
Using the Cloud Console:
1. Enable Cloud Run Admin API.
2. Navigate to the Cloud Run page and select "Create service."
3. Configure your service's settings:
    - General settings
        - Service name
        - Region
        - Deploying one revision or multiple revisions as the source repository is updated (provide a container image)
        - CPU allocation (always or only during request processing)
        - Autoscaling (minimum and maximum number of instances)
        - Ingress rules (All, Internal and Load balancing, Internal only)
    - Container settings
        - Port number
        - Container command
        - Container arguments
        - Memory and CPUs (Max 32/16 GB and 8/4 CPUs in preview/general releases)
        - Request timeout (1-60 minutes, 5 minutes default)
        - Execution Environment (1st or 2nd gen)
        - Environment variables
    - Connection settings
        - Support session affinity (routing multiple requests from a client to the same container)
        - Cloud SQL connections
        - VPC Connector
    - Security Settings
        - Specify a service account
        - Require Binary Authorization
        - Encryption    

Note: Cloud Run services are generally covered by Google Cloud SLA, but not when in preview.

### Cloud Run Jobs
Cloud Run jobs are programs that run all their tasks within a period of time. Unlike a service, which can accept requests indefinitely as long as they're active, jobs perform their tasks and then terminate, and they can be given schedules and run in parallel.

- For example, a job that loads files into storage can be parallelized to have multiple instances in different containers processing files simultaneously.

#### Creating a Job
Using Cloud Console:
1. Enable Cloud Run Admin API.
2. Navigate to Cloud Run page and select "Create job."
3. Configure Job settings:
    - General settings
        - Container image
        - Job name
        - Number of tasks
    - Container settings
        - Container command
        - Container arguments
        - Task memory capacity
        - Task timeout and retries
        - Parallelism
    - Connection settings
        - Same as Cloud Run Service
    - Security settings
        - Same as Cloud Run Service

## App Engine
App Engine is a PaaS offering that provides a platform for running scalable applications in language-specific frameworks. When using App Engine, both a Standard and Flexible environment are available.

Standard applications have 4 components:

- Application

    - An application is a high-level resource tied to the project (1 application per project), and it is specified within a region.
    
- Service

    - An app has one or multiple services. Services are comprised of the code that gets executed in the App Engine environment.

- Version

    - A service may exist in multiple versions, with newer versions having new features or bug fixes.

- Instance

    - When a version executes, an instance of that app gets created.
    
Complex applications typically have multiple atomic services, usually referred to as microservices. Services are defined by their source code and their configuration file. The combination of those files constitutes a version of the app. Having multiple versions of an app allows you to migrate and split traffic.

### Deploying an App Engine Application
Using Cloud Shell and Cloud SDK:
1. Ensure gcloud is configured to operate App Engine.
    
        gcloud components install app-engine-python
        
2. Download a sample Hello World app.

        git clone https://github.com/GoogleCloudPlatform/python-docs-samples
        
3. Change to the directory with the Hello World app.

        cd python-docs-samples/appengine/standard_python3/hello_world
        
4. These files should appear in the directory:

        app.yaml
        main.py
        main_test.py
        requirements.txt
        requirements-test.txt
        
5. Look at the YAML file.

        runtime: python27
        api_version: 1
        threadsafe: true
        
        handlers:
        - url: /.*
          script: main.app
          
6. Deploy the app.

        gcloud app deploy app.yaml
        
    - This command has some optional parameters:
        - version (specify a version ID)
        - project
        - no-promote (deploy without routing traffic)
        
7. See the output of the app by going to https://gcpace-project.appspot.com. The project URL is the project name followed by "appspot.com".

8. To stop serving versions of the app:

        gcloud app versions stop v1 v2
        
### Scaling App Engine Applications
App Engine can automatically add or remove instances based on the load to the App Engine-managed server. Instances that scale based on load are called *dynamic* instances, and they are preferable for saving on cost. To make a dynamic instance, configure scaling to "autoscaling" or "basic scaling."

You can also opt for instances that run all the time, also called *resident* instances. These are more optimal if you want to ensure users spend less time waiting. To make a resident instance, configure scaling to "manual scaling."

Scaling is done with the app.yaml file using the term "automatic_scaling." This term can have key-value pairs with multiple config options:

- target_cpu_utilization (threshold to meet before new instances are started)
- target_throughput_utilization (a number between 0.5 and 0.95)
- max_concurrent_requests (a max on concurrent requests on an instance before new insances are started. Default 10, max 80)
- max_instances
- min_instances
- max_pending_latency (maximum time a request will be in queue before being processed)
- min_pending_latency

To do basic scaling, use these parameters instead:

- idle_timeout
- max_instances

### Splitting Traffic
App Engine provides three ways to split traffic:
1. By IP address
    - A client is always routed to the same instance as long as the IP address is static.
    - This option is not always best for stateful applications because the same user might try to access from two different IP addresses.
2. By HTTP cookie
    - Useful when you want to assign users to versions.
    - A cookie named GOOGAPPUID is given a hash value as the request header.
3. By random selection
    - Creates a generally even workload distribution.
    - If there is no GOOGAPPUID cookie, traffic gets routed randomly.
    
To route traffic, use the following command:

    gcloud app services set-traffic [service-name] --splits v1=0.3,v2=0.7
    
This will split the traffic for the service between two versions, with v1 getting 30% of traffic and v2 getting 70%. The *set-traffic* command also takes these parameters:

    --migrate (migrate traffic from previous version to new version)
    --split-by (how to split traffic: ip, cookie, or random)