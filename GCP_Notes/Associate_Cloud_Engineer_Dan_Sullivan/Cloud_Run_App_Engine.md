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
App Engine is a PaaS offering that provides a platform for running scalable applications in language-specific frameworks.