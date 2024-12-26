# Kubernetes
Kubernetes is an open-source container orchestration system created by Google. Kubernetes Engine (sometimes abbreviated GKE) is a managed Kubernetes service in Google Cloud where users can create and maintain their own clusters without needing to manage the Kubernetes platform.

Kubernetes runs containers on clusters of VMs, monitors the health of containers, and manages the lifecycle of VM instances.

A GKE cluster is similar to an Instance Group in Compute Engine, but there are some differences, mostly by virtue of the fact that Kubernetes manages containers. Containers offer a portable and lightweight means of distributing and scaling workloads. They have much smaller start/stop times and use fewer resources than a VM. You can configure Instance Group monitoring, but Kubernetes is generally more flexible with maintenance.

## Kubernetes Architecture
A cluster consists of a control plane and one or more worker nodes. The control plane can be replicated and distributed for purposes of availability and fault tolerance.

The control plane manages controllers, schedulers, and the Kubernetes API which handles all cluster interactions. The control plane is what issues commands to perform an action on a node. Users can interact with a cluster using the 'kubectl' command.

Kubernetes has several fundamental components:

- API Server - part of the control plane that exposes the Kubernetes API.
- Scheduler - part of the control plane that assigns pods to nodes.
- Controller Manager - part of the control plane that manages resource controllers (e.g. node controller, job controller, service account controller).
- etcd - a highly available key-value store.
- Kubelet - an agent that runs on each node in the cluster.
- Container Runtime - the software that runs containers.
- Kube-proxy - a network proxy that runs on each node in the cluster.

Nodes are primarily controllerd by the control plane, but some commands can be run manually. The nodes run an agent called 'kubelet' that communicates with the control plane.

## Kubernetes Objects
Workloads are distributed across the nodes in the cluster. To understand how work is distributed, it is necessary to understand the basic Kubernetes terms:

- Pods
- Services
- Deployments
- ReplicaSets
- StatefulSets
- Jobs
- Volumes
- Namespaces
- Node Pools

### Pods
Pods are instances of a running process in a cluster that contain and run at least one container. Multiple containers are used when two or more containers share resources or are tightly coupled. Pods use shared networking and storage across containers, which means each Pod gets a unique IP address and a set of ports for the containers to connect. When connected, the containers can talk to each other on localhost.

Pods are useful if your application becomes very popular and you need more processing power to be able to handle the load. In this case, it would be useful for another instance of your application (a new pod) to be provisioned. Kubernetes can be configured to perform this replication automatically. Even when not under a heavy load, having multiple instances is good for adding fault tolerance to the system.

Pods allow you to deploy multiple instances of one application or instances of different applications on the same node or on different nodes without needing to change their configuration. For management purposes, pods treat multiple containers as a single entity.

Pods are usually created in multiples and are managed as a unit. They support auto-scaling and are ephemeral.

### Services
Since pods are ephemeral, other services that depend on pods should not be tightly coupled to particular pods. If an application is looking for a specific IP address of a running pod, that pod might be terminated and cause issues with that application. For this reason, Kubernetes provides a level of indirection between applications in pods and other applications that call them. These are called services.

A service is an object that provides API endpoints with a stable IP address that allow applications to discover pods running a particulaar application. They maintain an up-to-date list of pods that are running an application.

### Deployments
Deployments are sets of identical pods all running the same application. These pods are created using a pod template. In the pod specification, you can set the minimum number of pods that should be in the deployment, and then if any pods get terminated additional pods can be added by calling on a ReplicaSet.

### ReplicaSet
A ReplicaSet is a controller used by a deployment that ensures the correct number of identical pods are running. When a pod gets terminated, the ReplicaSet will notice if not enough pods for that workload are running and will create another. ReplicaSets also update and delete pods. It is generally recommended to use deployments and not ReplicaSets unless you require custom update orchestration or do not expect to update at all.

### StatefulSets
Deployments are well suited to stateless applications. An application that calls an API to perform some operation on its input may reach a different pod each time it makes a call. But there are times when it is better to have a single pod respond to all calls for a client during a single session. StatefulSets are like deployments, but they assign unique identifiers to pods. This enables Kubernetes to track which pod is used by which client and keep them together. StatefulSets are used when an application needs a unique network identifier or stable persistent storage.

### Jobs
A job is an abstraction about a workload. Jobs create pods and run them until the application completes a workload.

### Volumes
Volumes are storage mechanisms that store data independent of the pod's lifecycle. If a pod fails and is restarted, the contents of a volume attached to that pod will continue to exist.

### Namespaces
A namespace is a logical abstraction for separating groups of resources in a cluster. They are used when clusters host a variety of projects, teams, or other groups that may use different policies for using cluster resources. GKE includes a default namespace to be used for objects with no other namespace defined.

### Node Pools
A node pool is a collection of nodes in a cluster that all have the same configuration. When a cluster is first created, all nodes are in the same node pool. Node pools are useful for grouping nodes with similar features.

## Creating a Cluster
Like with Compute Engine and other services, you can manage Kubernetes resources via Cloud Console, Cloud SDK, and Cloud Shell.

### Using Cloud Console
Steps:

1. Enable Kubernetes API
2. Choose Standard or Autopilot Mode

    - Standard Mode: pay for the resources you provision, manage infrastructure, and configure nodes as desired.
    - Autopilot Mode (Recommended): GKE manages cluster resources and node infrastructure for you, pay only for what is used while applications are running. Uses preconfigured and optimized configuration settings.
    
3. Specify cluster name, region, availability (private or public).

    - You can choose Zonal or Regional cluster. Regional clusters by default have nodes in 3 zones.

4. Make other configurations.

    - When using Autopilot cluster, you can block nontrusted non-GCP source IP addresses from accessing the control plane. You can also specify timing windows for running routine maintenance operations.
    
5. Click "Create."
    
### Using Cloud Shell and Cloud SDK
The basic command for Google Kubernetes Engine is:

    gcloud container
    
There are a number of other parameters for this command:

- project
- zone
- machine type
- image type
- disk type
- disk size
- number of nodes

Sample command for creating a Standard Mode cluster:

    gcloud container clusters create cluster1 --num-nodes=3 --region=us-central1
    
Using Autopilot Mode:

    gcloud container clusters create-auto

## Deploying Application Pods
Steps:

1. From the 'Clusters' page of Kubernetes Engine on Cloud Console, select 'Create Deployment.'
2. Specify the following:

    - container image
    - environment variables
    - initial command
    - application name
    - namespace
    - labels
    - cluster
    
3. Once configurations are set, you may look at the accompanying YAML configuration for the deployment.

    - Sample YAML configuration:
    
            apiVersion: "apps/v1"
            kind: "Deployment"
            metadata:
                name: "nginx-1"
                namespace: "default"
                labels:
                    app: "nginx-1"
            spec:
                replicas: 3
                selector:
                    matchLabels:
                        app: "nginx-1"
                template:
                    metadata:
                        lavels:
                            app: "nginx-1"
                    spec:
                        containers:
                        - name: "ninx-1"
                          image: "nginx:latest"
            ---
            apiVersion: "autoscaling/v2beta1"
            kind: "HorizontalPodAutoscaler"
            metadata:
                name: "nginx-1-hpa-5fkn"
                namespace: "default"
                labels:
                    app: "nginx-1"
            spec:
                scaleTargetRef:
                    kind: "Deployment"
                    name: "nginx-1"
                    apiVersion: "apps/v1"
                minReplicas: 1
                maxReplicas: 5
                metrics:
                - type: "Resource"
                  resource:
                      name: "cpu"
                      targetAverageUtilization: 80

    - At minimum, a YAML configuration for Kubernetes requires apiVersion, kind, metadata, and spec
    
    
4. Ensure both Cloud SDK and kubectl is installed:

        gcloud components install kubectl
        
5. Use kubectl to run a Docker image.

        kubectl run
        
   To run a container within a deployment:
    
        kubectl create deployment app-deploy1 --image=app1 --port=8080
        
   This will run a Docker image called "app1" with a network accessible via port 8080.
    
6. If you wish to scale up the number of replicas in the deployment:

        kubectl scale deployment app-deploy1 --replicas=5
        
## Monitoring Kubernetes
Google Cloud offers a comprehensive monitoring, logging, and alerting product called Cloud Operations Suite.

- Includes Cloud Monitoring and Cloud Logging services, which can be used to monitor Kubernetes clusters.
- provides multiple methods for analyzing system an performance metrics.
    
    - System Metrics: describes low-level cluster resources (CPU, memory, storage)
    - Prometheus: open-source system for collecting performance metrics.
    
When creating a cluster, you can tell Google Cloud to send metrics to these monitoring and logging apps.

## Managing Standard Mode Clusters

### Viewing Cluster Status

#### Using Cloud Console

In the Cloud Console for Kubernetes Engine, you will see a list of running clusters. You can click the name of the cluster you are interested in and find various details. This includes the cluster configuration, the details of any nodes or node pools, and the persistent volumes and storage classes used by the cluster. A storage class is a type of storage with specific policies that describe the service, backups, and provisioner.

There is also an "Observability" tab in the cluster menu that gives metrics on performance and a "Logs" tab that displays any log messages.

When you click on a node, you will see details like CPU usage, memory consumption, and a list of pods running on the node. Clicking on a pod will show when the pod was created, assigned labels, links to logs, and the status. At the bottom of the pod display is the containers that are running in that pod.

#### Using Cloud SDK and Cloud Shell
The 'gcloud container' command is used to view details of clusters.

The following command will list all the names and basic info of each cluster:

    gcloud container clusters list
    
To view the details of a specific cluster:

    gcloud container clusters describe --zone zone-name cluster-name

The 'kubectl' command is used to view details of nodes, pods, deployments, and other cluster objects. Ensure you have a proper 'kubeconfig' file. This is necessary to communicate with the cluster API.

The following command will configure a kubeconfig file on the named cluster:

    gcloud container clusters get-credentials --zone zone-name cluster-name
    
List the nodes in a cluster:

    kubectl get nodes
    
List the pods:

    kubectl get pods
    

### Adding, Modifying, and Removing Nodes
In the Cloud Console, you can view the details of nodes and node pools by selecting a cluster and going to the "Nodes" tab. Select a node you wish the change and click "Edit." Here, you can increase or decrease the number of nodes in a node pool.

Adding or modifying nodes using the Cloud SDK or Cloud Shell takes 3 parameters:

1. cluster name
2. node pool name
3. cluster size

Example: Use this command to increase the number of nodes in the node pool from 3 to 5:

    gcloud container clusters resize cluster-name --node-pool default-pool -num-nodes 5 --region=us-central1
    
If this is a regional cluster, this will resize for each zone the node pool is in.

To modify a cluster that's already created:

    gcloud containers update cluster-name [--enable-autoscaling] [--min-nodes 1] [--max_nodes 5] --zone us-central1-a --node-pool default-pool
    
    
### Adding, Modifying, and Removing Pods
It is normally best practice to not manipulate pods directly. GKE will maintain the number of pods specified for a deployment, so you should instead change the deployment configuration.

From Cloud Console, select "Workloads" option from the left navigation menu to show a list of deployments. Click the name of the deployment you'd like to modify. You should see a list of managed pods. You can click on these and edit and delete them individually, but this is not recommended.

Select the "Actions" option from the 3 dots, and then select "Scale" to open up a box where you can input a new size for a workload. You can also choose "Autoscale" and set a minimum and maximum number of replicas.

To edit pods in Cloud SDK or Cloud Shell, the 'kubectl' command is once again necessary.

To list deployments:

    kubectl get deployments
    
To add and remove pods, change the deployment configuration:

    kubectl scale deployment deployment-name --replicas 5
    
You can set up autoscaling to meet demands according to CPU usage. The following command will add or remove pods as necessary. If CPU usage exceeds 80 percent, up to 10 replicas will be added.

    kubectl autoscale deployment deployment-name --max 10 --min 1 --cpu-percent 80
    
To remove a deployment:

    kubectl delete deployment deployment-name


### Adding, Modifying, and Removing Services
Like with pods, Services are added in the "Workloads" menu. Click "Deploy" at the top of the menu to create a new deployment. Here, you can specify the image being used, labels, initial command, and the name of the application.

When you click on a Deployment, you will see the list of Services. Clicking the name of a Service shows the Detail menu of the Service, where you can see a "Delete" option.

In Cloud SDK or Cloud Shell, use the following command to list Services:

    kubectl get services
    
To start a new Service:

    kubectl create deployment service-name --image=image-URL --port 8080
    
Deployments need to be exposed to be accessible to resources outside the cluster. This can be done with the following command:

    kubectl expose deployment service-name --type="LoadBalancer"
    
To remove a Service:

    kubectl delete service service-name
    

### Creating Repositories in the Artifact Registry
Artifact Registry is a Google Cloud service for storing container images. You can create registries, push images to it, and view the contents of the registry and image details. This can be done via Cloud Console, Cloud SDK, and Cloud Shell.

In Cloud Console, select "Artifact Registry" from the navigation menu to display example registries. To create a registry, click the "+" icon. Artifact Registry can contain many different types of registries:

- Docker
- Maven
- npm
- Python
- Apt
- Yum

Kubernetes Engine makes use of images stored in a Docker repository.
