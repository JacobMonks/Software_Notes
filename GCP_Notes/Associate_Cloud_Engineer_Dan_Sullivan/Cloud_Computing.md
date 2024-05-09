# Computing in Google Cloud
Google Cloud offers a variety of computing services, but learning when and how to use them comes with degrees of nuance.

## Compute Engine
Compute Engine is a service that provides VMs that run on Google Cloud. Using Compute Engine involves managing one or more instances.

Instances run images. An image is a set of characteristics of a VM or container which might include operating system, libraries, prewritten code, etc. Google Cloud allows you to create VMs using public images for Linux or Windows, and there are other images provided by 3rd party vendors and open-source projects.

Public images can support many operating systems, including CentOS, Debian, Ubuntu and more. But if none of them match your particular needs, you can create a custom image.

Each VM has an associated service account that will be assigned roles for operating the instance. You can also configure your instance to have GPUs for graphics processing, add the Confidential VM Service for high-security applications, add and configure boot disks and their encryption, or limit traffic to HTTP, HTTPS, FTP, TCP, etc.

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


## Compute Engine Virtual Machines

## Managing Virtual Machines

