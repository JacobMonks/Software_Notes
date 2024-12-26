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



## Standard Mode Clusters

