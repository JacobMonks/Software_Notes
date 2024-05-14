# Computing in Google Cloud
Google Cloud offers a variety of computing services, but learning when and how to use them comes with degrees of nuance.

## Compute Engine
Compute Engine is a service that provides VMs that run on Google Cloud. Using Compute Engine involves managing one or more instances.

Instances run images. An image is a set of characteristics of a VM or container which might include operating system, libraries, prewritten code, etc. Google Cloud allows you to create VMs using public images for Linux or Windows, and there are other images provided by 3rd party vendors and open-source projects.

Public images can support many operating systems, including CentOS, Debian, Ubuntu and more. But if none of them match your particular needs, you can create a custom image.

Each VM has an associated service account that will be assigned roles for operating the instance. You can also configure your instance to have GPUs for graphics processing, add the Confidential VM Service for high-security applications, and add configure boot disks and their encryption, or limit traffic to HTTP, HTTPS, FTP, TCP, etc.

When creating an instance, you can control its actions using Access Scopes, but these have largely been eclipsed by IAM.

Compute Engine can be run and managed by different means.

- Types of instances:

    - Preemptible Instance : cheaper but can be shut down at any time by Google.
    - Spot VMs : also a bit cheaper, but will last at least 24 hours.
    - Sole Tenancy : reserves a server for the VM and any VMs you wish to be attached to it.

- Types of Encryption:

    - Google-managed encryption : Google creates and manages encryption keys.
    - Customer-managed encryption : User creates but Google manages encryption keys.
    - Customer-supplied encryption : User creates and manages encryption keys.

A convenient feature of Compute Engine is the ability to create instance templates that allow you to describe a VM configuration and apply it to multiple instances. You can also create instances by supplying a machine image.

VM Instances are project-specific and region-specific. You may want to choose particular regions when creating an instance for any of the following reasons:

- Cost can vary between regions.
- Data locality regulations may require you to have instances close to their users.
- High availability when distributing instances in different regions.
- Latency is lower when the instance is closer geographically to its user.
- Some regions support specific hardware that others don't.
- Some regions produce more carbon to power their data centers.

### Compute Engine Privileges
For users to create and access VM instances, they must be a member of the project and have the necessary permissions. Compute Engine has some predefined roles that encompass a group of permissions. These include:

- Compute Admin : full control over Compute Engine instances
- Compute Network Admin : create, modify, and delete networking resources with read-only access to firewall rules and SSL certifications.
- Compute Security Admin : create, modify, and delete SSL certifications and firewall rules.
- Compute Viewer : get and list data from Compute engine resources but cannot read data from those resources.

You can also apply IAM policies to resources directly, meaning you don't have to create new permissions with each new VM.

### Preemptible VMs
These are short-lived instances designed to run particular types of workloads.

- financial modeling
- rendering
- big data
- continuous integration
- web crawling

Any application that is fault-tolerant and can withstand some degree of interruptions is a good use case for preemptible VMs because they will save money.

Some things to note about Preemptible VMs:

- They will last at most 24 hours.
- They may not always be available in a given region or zone.
- They cannot migrate to a regular VM.
- They aren't covered by Service Level Agreements (SLAs).

### Custom Machine Images
Compute Engine offers a range of configurations for CPU and memory, but perhaps it would be more cost-effective if you could specify exactly how much you need for your application. This is where custom machine images come in handy, where you can adjust the number of CPUs and the amount of memory using sliders.

### Compute Engine Use Cases
Compute Engine is a good choice when you want maximum control over your computing.

- Choosing specific images to run on the instance.
- Install software packages or custom libraries.
- Have fine-grained control over permissions.
- Have control over SSL certifications and firewall rules.

## App Engine
App Engine provides a managed PaaS for running applications. Rather than configuring VMs, you outline some basic resource requirements and the application that you will run on it, and Google will manage the necessary resources.

App Engine is for users who want to worry less about managing and more about running their applications, but it offers less control as a result.

### App Engine Structure
App Engine applications consist of services, and each service proveides a specific function. Services can have different versions running on different instances at the same time. Those instances are managed by App Engine.

With dynamic instances, Google can add or shut down instances depending on the need. This can make it difficult to keep track of costs, so Google Cloud gives the user the ability to set spending limits and alarms.

### Standard vs Flexible Environments
App Engine provides two types of runtime environments:

1. Standard

    - Has a pre-configured, language-specific environment.
        - Python 2, 3
        - Java 8, 11, 17
        - PHP 5, 7, 8
        - Go 1.11+
        - Node.js
        - Ruby
    - Second Generation standard environment also supports extensions for other languages and gives full network access compared to the more limited first generation.
    - Scaling options (basic, automatic, manual) make it very cost-effective because it can scale down to zero instances if there is no traffic.

2. Flexible

    - A more customizable environment for users who want PaaS benefits without the restrictions of the standard environment.
    - Uses Docker for containerization, so users can configure their containers with dockerfiles.
    - Very similar to Kubernetes Engine but requires less managing by the user.

### App Engine Use Cases
App Engine relieves the user of administration tasks so they can focus on developing and running applications.

If your application is written in one of the supported languages, the standard environment is more cost-effective.

If the services that make up your application can be containerized, the flexible environment is preferred.

### Kubernetes Engine
Kubernetes is an open-source container orchestration service created by Google that allows users to do the following:

- Create clusters of VMs that run Kubernetes software for containers.
- Deploy containerized applications to the cluster.
- Administer the cluster.
- Specify policies such as auto-scaling.
- Monitor cluster health.

Kubernetes Engine allows you to manage many instances as a single resource called a cluster. This is helpful if you have many different microservices that require different configurations. Kubernetes Engine gives you the benefits of Kubernetes without the administrative overhead.

It supports two modes:

1. GKE Standard

    - Pay-per-node.
    - User is responsible for configuring and managing nodes.

2. GKE Autopilot

    - Pey-per-pod.
    - GKE manages the configuration and infrastructure.

Kubernetes is different from other cluster management platforms because it is designed to run a variety of applications instead of running one application over multiple servers like Spark.

Google Kubernetes Engine provides some useful functions:

- Load Balancing across Compute Engine VMs deployed in a Kubernetes cluster.
- Auto-scaling for nodes in the cluster.
- Automatic upgrading of cluster software.
- Node monitoring.
- Logging.
- Support for node pools, collections of nodes with the same configuration.

### Kubernetes Architecture
A Kubernetes cluster consists of a cluster control plane and one or more worker nodes. The control plane manages the cluster and is where cluster services (Kubernetes API server, resource controllers, schedulers) are run.

The Kubernetes API Server coordinates all communications to the cluster while the control plane determines the containers and workloads on the each worker node.

Kubernetes deploys containers in units called pods. A pod consists of one or more containers that share storage, network resources, an IP address, and port space.

### Kubernetes Use Cases
Kubernetes is a good choice for large-scale applications that require high availability and high reliability. Being able to manage services as a single unit makes it useful when an application has multiple different services like a user interface, data manipulation, and networking.

### Anthos
Anthos is a managed service for centrally configuring and managing deployed services. You can manage multiple GKE clusters and clusters running in other clouds or on-premises. It also allows you to enforce policies across multiple environments.

## Cloud Run

## Cloud Function

## Compute Engine Virtual Machines

## Managing Virtual Machines

