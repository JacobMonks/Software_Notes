# Google Cloud Computing Services
Google Cloud has many services that vary in use cases, accessibility, and cost.

## Computing Resources
There are two primary ways to go about cloud computing:

1. IaaS (Infrastructure as a Service):

    - This model gives the user substantial control over their usage.
    - Choose the OS, package installations, and maintenance rules.
    - Good for users who want to manage their applications for maximum efficiency.

2. PaaS (Platform as a Service):

    - This model removes a lot of the overhead that IaaS requires.
    - Provides a runtime environment for running applications without managing servers, storage, or networking.
    - Good for users who just want to start developing without needing to worry about infrastructure.

### Compute Engine
Compute Engine is Google's IaaS product. Users create and configure VMs and attach persistent storage to them.

A VM is an emulation of a physical server that provides CPU, memory, storage, and other resources that you could find on a computer. VMs run within a low-level service called a hypervisor. Google uses a more secure version of the Kernel Virtual Machine (KVM) hypervisor to provide virtualization on Linux x86 systems. Hypervisors can run multiple guest operating systems and keep the activities of each isolated from the others.

When configuring a VM, you are given many options, including, but not limited to:

- Operating system
- Storage size
- Whether to use GPUs
- Whether to make it preemptible

For more on Compute Engine, refer to [Chapter 4](./Associate_Cloud_Engineer_Dan_Sullivan/Cloud_Computing.md).

### Kubernetes Engine
Kubernetes Engine is a computing service that allows users to easily manage and run containerized applications on a cluster. Like a VM, a container is a way to isolate computing processing and resources. Unlike a VM, a container does not use a hypervisor, but instead uses a container manager. The container manager uses the functionality of the host OS to coordinate containers and isolate services.

With Kubernetes Engine, users can describe the resources that they need to run their services, and Kubernetes will provision them. It also monitors the health of servers in the cluster and has failsafes in place in case of server failures.

Anthos clusters extend GKE for hybrid and multi-cloud environments. Some advantages of Anthos include:

- Centralized management of configuration as code.
- Ability to roll back deployments with Git.
- A single view of cluster infrastructure and applications.
- Centralized, auditable workflows.
- Instrumentation of code.
- Anthos Service Mesh for authorization and routing.

For more on Kubernetes Engine, refer to [Chapter 7](./Associate_Cloud_Engineer_Dan_Sullivan/Kubernetes.md).

### App Engine
App Engine is a PaaS product that allows developers to create applications in popular programming language and deploy it them to a serverless environment. It is well-suited for web and mobile back-end applications.

App Engine has two different environments:

1. Standard

    - Run applications in a language-specific sandbox, isolated from the server OS and other applications on the server. This is ideal for applications written in one language without the need for added OS packages or additional software.

2. Flexible

    - Run containerized applications in the App Engine environment. This works well when your application relies on additional libraries or 3rd-party software. This configuration also allows you to write to a local disk.

For more on App Engine, refer to [Chapter 9](./Associate_Cloud_Engineer_Dan_Sullivan/Cloud_Run_App_Engine.md).

### Cloud Run
Cloud Run is a service for running stateless containers and it does not restrict what programming languages you can use. Cloud Run services have regional availability.

### Cloud Functions
Cloud Functions is a lightweight computing option that works well with event-driven processing. It can run code in response to specific actions, such as files being uploaded to a bucket in Cloud Storage or a message being written to a messaging queue. It is serverless and supports auto-scaling.

Cloud Functions is not designed to run highly intensive or long-running code, but it can call other services such as third-party applications or other Google Cloud services.

For more on Cloud Functions, refer to [Chapter 10](./Associate_Cloud_Engineer_Dan_Sullivan/Cloud_Functions.md).

## Storage Solutions
