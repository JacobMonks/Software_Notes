# Google Cloud Platform

#### Online Test Prep:
[Wiley Test Prep](https://app.efficientlearning.com/pv5/v8/5/app/google/871446googleclceacesg2e.html?#welcome)
User: jacobmonks0408@gmail.com
Pass: WileCoyote1970!

#### Register for the Exam:
[Associate Cloud Engineer](https://cloud.google.com/learn/certification/guides/cloud-engineer)

## Google Cloud Overview
Public Cloud Services are used by both startups and large enterprises. They can save costs on infrastructure, networking, and scaling as the company grows in employees and customers.

The services they offer fall in a few categories:

- Compute Resources
- Storage
- Networking
- Specialized Services like Machine Learning

### Compute Resources
These come in many forms.

#### Virtual Machines
Google Cloud allows you to set up VMs and gives full control to the user including what will run on it, who will have access to it, what storage it will have, and any operating system configurations. There are many pre-configured settings, but you can also fully customize it.

If your application will have a large amount of traffic, you can also configure load balancing for high availability or auto-scaling so you aren't charged for more resources than you are using and you won't run into issues with high traffic.

#### Managed Kubernetes Clusters
Managed Clusters are a good option for cloud users who don't want to spend time keeping servers up and running.

Managed Clusters operate with containers. You can specify the number of servers you want to run and what containers will run on them.

The health of the containers is monitored automatically in a managed cluster. If a container fails, the cluster will spin up a replacement.

Containers are useful when running applications that rely on multiple microservices in your environment running at once.

#### Serverless Computing
Serverless computing adds further abstraction so the user does not need to configure VMs or clusters.

Google has 3 options for serverless computing:

- App Engine
- Cloud Run
- Cloud Functions

### Storage
Storage in the cloud can be done via several methods:

- object storage
- file storage
- block storage
- caches

#### Object Storage
In Object Storage, files are stored as blobs in buckets. Similar to a file system, objects are accessible by a unique URL. Google's object storage service is called simply Google Cloud Storage.

This storage is also done serverless, so a VM is not necessary for storing objects.

#### File Storage
When an application requires operating-system-like file access, Google Filestore maintains the hierarchical structure of filesystems like a typical computer, and it exists independently of VMs or applications that access those files.

#### Block Storage
Blocks are fixed-size data structures. Using block storage allows you to install file systems on top of the block storage, or you can access blocks directly in applications.

Linux systems will typically use 4 KB blocks. Relational databases also sometimes write to blocks of larger size.

Block storage is available on disks that are attached to VMs, and it can either be ephemeral or persistent. Access to block storage is also commonly faster than object storage.

#### Caches
Caches are in-memory data stores that are very fast to access, with latency under a millisecond. Though incredibly quick, memory is more expensive than SSD or disk storage, and it is not persistent in case of reboots or failures.

### Networking
Every network-accessible device or service has an IP address. These are needed for networking between your cloud services and also if you wish to network with on-premise systems.

Devices in Google Cloud have both an Internal and an External address. Internal is accessible only by services in your internal network, or Virtual Private Cloud (VPC). External addresses are accessible from the Internet.

You may also want to set Firewall rules to determine what devices and servicecs have access to resources.

### Specialized Services
These services have more specific functions as a part of your workflow or a building block of a larger application. They have some common characteristics:

- They are usually serverless.
- They provide a very specific function.
- They provide an API to access its functionality.
- You are charged based on your usage.

Some examples of specialized services in Google Cloud include:

- AutoML
- Cloud Natural Language
- Cloud Composer
- Vertex AI
- Speech-to-Text
