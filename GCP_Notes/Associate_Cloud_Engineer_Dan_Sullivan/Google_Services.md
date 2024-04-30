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
Like computing, storage solutions vary in use cases. Some users want to prioritize quick access while others want dependeable long-term archival.

### Cloud Storage
Cloud Storage is Google's general-purpose object storage system. Objects can be any type of file or binary large object (blob). Objects are organized into buckets which act similar to directories in a filesystem. Cloud Storage is not part of a VM, and it can be accessed by containers, VMs, and any network-connected device with proper privileges.

Any object stored in a bucket is uniquely addressable by a URL. This URL allows users to read and write objects to a bucket if they have been granted permission.

Cloud Storage is useful for storing objects as single units of data, like images or soundclips, and it can be accessed independently of servers that may or may not be running. GCS also has settings for different scopes of availability. Objects with regional availability will be accessible throughout an entire region at low latency.

Multi-region availability means the data will be more widely accessible, but generally at lower latency. One way to decrease latency is when the application that uses the data is distributed across the region.

When you want to store objects for long periods of time, consider nearline (30 days), coldline (90 days), or archive (1 year) storage. The access to these objects is limited, but the cost of storage is considerably lower and it is highly durable.

GCS allows you to create lifecycle management policies that dictate how objects are stored after certain periods of time. For example, you could have objects in a specific bucket automatically enter nearline storage if they are at least 60 days old.

### Persistent Disk
Persistent Disks are storage services that are attached to VMs that provide block storage on SSDs or HDDs. SSDs are useful for low latency applications where performance is a priority, but HDDs are cheaper.

The advantage of Persistent Disks is that they support multiple readers with no dip in performance, and the Disks can be resized at a moment's notice without restarting the VM.

The storage limit of Disks is typically 64 TB.

### Cloud Storage for Firebase
Cloud Storage for Firebase is an object storage option that is designed secure transmissions with recovery mechanisms in the case of faulty connections. This makes it a good choice for mobile applications since phones will not always have strong connectivity.

### Cloud Filestore
Filestore is a storage service that implements the Network File System (NFS) protocol. It provides a shared filesystem for use with Compute Engine and Kubernetes Engine. It is capable of a high amount of input-output operations per second (IOPS) and variable capacity.

### Cloud SQL
Cloud SQL is Google's Relational Database that allows users to set up MySQL, PostgreSQL, and SQL Server databases on VMs. Replication management and automatic failover makes this option highly available. Being a relational database also makes it the ideal solution for applications that require very consistent data structure requirements.

### Cloud Bigtable
Bigtable is a highly scalable NoSQL database that is built with the wide-column data model. It has incredibly low latency reads and writes, allowing for millions of operations per second and managing billions of rows.

It integrates well with other Google services and APIs like HBase for Hadoop and other open-source tools.

### Cloud Spanner
Cloud Spanner is a globally distributed storage solution. It has the consistency of a relational database with the scalability of a NoSQL database. It is ideal for enterprise applications that demand highly scalable and available services and strong security encryption.

### Cloud Firestore
Firestore, formerly known as Datastore, is a document-based NoSQL database. Documents are collections of key-value pairs that allow schemas to be highly flexible. Keys do not have to be defined prior to use, which makes document-based NoSQL databases appealing for applications that must accomodate a wide range of attributes.

Firestore can be accessed by applications in Compute Engine, Kubernetes Engine, and App Engine via REST API.

Firestore scales automatically and shards its data into partitions for performance. It is a managed service, meaning the user does not need to keep track of replication, backups, or general administration.

Despite being non-relational, Firestore supports transactions, indexes, and SQL-like queries.

### Cloud Memorystore
Memorystore is an in-memory cache service. It is used for caching frequently used data in memory, but is not ideal for large volumes of data. It is primarily intended to reduce the runtime of queries on the most accessed information.

## Networking
Google Cloud provides several means configuring virtual networks, link with on-premise data centers, and secure your resources.

Networking will be discussed more in depth in [Chapter 14](./Associate_Cloud_Engineer_Dan_Sullivan/Networking.md) and [Chapter 15](./Associate_Cloud_Engineer_Dan_Sullivan/Networking.md#dns).

### Virtual Private Cloud
Virtual Private Clouds (VPC) are a way to ensure that an enterprise's resources are logically isolated from those of another enterprise usinng the same cloud service. An advantage of VPCs is that they can span the globe without relying on the public Internet. This allows back-end servers to access Google services with no need for a public IP address.

Using Internet Protocol Security (IPSec), you can link your VPC to on-premises VPNs.

### Load Balancing
Load balancing is a way to distribute workloads across your cloud infrastructure. Cloud Load Balancing can manage HTTP, HTTPS, TCP, SSL, and UDP traffic.

### Cloud CDN
Content Delivery Networks (CDN) allow users to request content from distributed systems with low-latency responses. There are more than 100 CDN endpoint locations globally. They are used effectively when you have large amounts of static content that must be globally accessible, such as news sites.

### Cloud Interconnect
Cloud Interconnect is a convenient way to connect your existing networks to the Google network, and it can do this via interconnects and peering.

1. Interconnects

    - A direct network connection is maintained between an on-premises data center and one of Google's colocation facilities.
    - This can also be done through a third party, known as Partner Interconnect, and it is the recommended way of establishing a network conenction.

2. Peering

    - Does not use Google Cloud resources and gives access to Google Workspace applications.

### DNS
Cloud DNS is a domain name service in Google Cloud. It is a low-latency and highly available service for mapping domain names to IP addresses. It scales automatically, so customers can have thousands of addresses without needing to worry about infrastructure.

### Identity Management and Security
Google Cloud Identity and Access Managenet (IAM) gives users the ability to create restrictions on access to cloud resources.

Users are individuals who have specific permissions. To grant permissions to many users at once in a convenient way, you can create roles. Roles will have a selection of permissions, such as creating, updating, and deleting VMs.

### Development Tools
There are also a multitude of general-purpose development tools.

- Cloud SDK for command-line interface.
- Container Registry for deploying applications to containers.
- Cloud Tools for IntelliJ, Powershell, Visual Studio, Eclipse
- App Engine Plugins for Gradle and Maven.

## Additional Tools

### Management and Observability

- Cloud Monitoring
- Cloud Logging
- Error Reporting
- Cloud Trace
- Cloud Debugger
- Cloud Profiler

### Data Analytics

- BigQuery
- Dataflow
- Dataproc
- Dataprep

### AI and ML

- AutoML
- Translation AI
- Natural Language
- Vision AI
- Recommendations AI