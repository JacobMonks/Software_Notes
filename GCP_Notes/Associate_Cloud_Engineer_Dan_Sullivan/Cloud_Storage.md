# Cloud Storage
This section will cover the different storage solutions in Google Cloud and how to go about planning, configuring, deploying, and loading storage.

## Planning Storage
Google Cloud has numerous storage solutions that vary in their capabilities. The most important measures to consider when choosing a storage option are:
- Time to access data
- The data model
- Consistency
- Availability
- Persistence
- Transactional support

The time to access data can range from 0.5 nanoseconds to several hours depending on the tools being used and what kind of data is being accessed.

### Types of Storage systems
GCP offers multiple models for storing data.
- Caching based on Redis and Memcached.
- Persistent Disk storage for use with VMs.
- Object storage for shared access across resources.
- Archival storage for long-term, infrequent access requirements.

#### Cache
*Cache* is in-memory storage with extreme low-latency, designed for providing data in less than a millisecond. The main limitations are the amount of memory available and the fact that the storage is ephemeral and will be lost if a shutdown occurs.

Caching is most useful for applications that cannot tolerate long latency. A common use case is to retrieve data from a database and store that in cache memory so that the query does not need to run everytim the data is needed.

*Memorystore* is a cache-based storage solution usable by Compute Engine, App Engine, and Kubernetes Engine. It is compatible with Redis and Memcached, which are some of the most widely used open source cache systems. Any application designed to work with Redis and Memcached can work with Memorystore.

Redis instances can contain up to 300 GB of memory and create failover replicas when configured for high availability. Memcached instances are comprised of up to 20 nodes, each with up to 256 GB.

Memorystore can be accessed from the console, and you can create Redis or Memcached instances with the following specifications:
- Instance ID
- Display name
- Redis/Memcached version
- Standard or Basic instance (Standard supports high availability, Basic is lower cost)
- Cluster configuration (if using Memcached)
- Region and zone
- Memory allocated
- Assign labels and IP range (optional)

#### Persistent Disk Storage
Persistent Disks provide durable block storage that are useful for creating filesystems. When configuring a VM via Compute Engine or Kubernetes Engine, you can attach a persistent disk or a local SSD to the VM. However, the persistent disk exists independetly of the VM and will continue to exist after the VM is terminated, which is not the case for the local SSD.

Persistent disks are available as Solid-State Drives (SSD) or Hard Disk Drives (HDD).
- SSD is good for high throughput and consistent performance.
- HDD has longer latencies but costs less, good for storing large amounts of data for batch operations.

Persistent Disks in GCP have these availability options:
- Zonal standard (reliable use within a single zone)
- Regional standard (like Zonal but has replicas across 2 zones in a region)
- Zonal balanced (cost effective and reliable)
- Regional balanced
- Zonal SSD (fast and reliable storage within a zone)
- Regional SSD
- Zonal extreme (highest performance block storage)

Google Cloud offers local SSDs with high performance local block storage, but they have no redundancy. Persistent Disks are capped at 64 TB (both SSD and HHD), and local SSDs have a fixed capacity at 375 GB.

Persistent Disks can be attached to multiple VMs, and snapshots can be made within minutes so additional copies can be distributed for use by other VMs. It is also possible to resize a persistent disk while mounted to a VM. Persistent disks automatically encrypt the data.

You can create and configure persistent disks in the Compute Engine dashboard by selecting "Disks" and inserting these values:
- Name of disk
- standard or SSD
- region and/or zone
- an image to create a persistent boot disk
- a snapshot to create a replica of another disk
- encryption option

#### Object Storage
Object storage is a good way to store large amounts of data that can be shared widely. GCP's service for this is called simply Cloud Storage.

Files stored as objects are treated as atomic units, so you cannot operate on only parts of an object. As a result, you cannot manipulate subcomponents of a file in object storage. Furthermore, Cloud Storage doesn't support concurrency or locking.

Cloud Storage is well suited for storing large volumes of data that don't follow a specific structure. You can store any type of data as objects in a bucket. A bucket is an abstraction in Cloud Storage for organizing data, and each bucket is in the global namespace, so its name must be globally unique.

Cloud Storage does not provide a filesystem and does not support subdirectories. However, Cloud Storage Fuse is an open source project that provides a way to mount buckets on Linux and Mac as a filesystem.

There are 4 classes of object storage:
1. Standard
    - Best option for data that is accessed frequently.
    - Supports dual- and multi-region access with up to 99.95% availability.
    - Single-region storage has 99.9% availability.
2. Nearline
    - Good for infrequently accessed data (less than once per month).
    - 99.95% availability for multi-region and 99.9% for single region.
    - SLAs are 99.9% for multi-region and 99.0% for single region and are lower cost.
    - A retrieval charge is incurred.
3. Coldline
    - All the same features of Nearline, but accessed only once per 90 days and 90 days minimum storage period.
4. Archive
    - Designed for long-term storage for archiving, disaster recovery, etc.
    - Must be stored for minimum 365 days, only accessed once per year.
    - Same SLAa and availability as Nearline.
    
For availability, a bucket can be single-region, dual-region, or multi-region. Single region means a specific geographic location, e.g. Chicago. Dual-region is a pair of regions. Multi-region is a large geographic area, e.g. United States. Multi-regional is the best option if your users are globally dispersed and must access synchronized data.

Buckets can be configured to retain versions of objects when they are deleted or changed. The latest version of an object is called the *live* version. This feature is useful when you want to minimize risk of changes and keep a history of changes.

You can also apply Lifecycle Management Policies to automatically move objects in a bucket from one storage class to another (standard > nearline > coldline > archive). Once an object reaches a certain age, you can move it to a lower-cost storage class. You can also set conditions for the number of versions, whether the object is the live version, or for the date it was created. You choose a lifecycle policy when you create a bucket.

If a live version of a file is deleted, the object instead gets archived. If the archived version is deleted, the file is gone permanently.

### Data Models

## Deploying Storage

## Loading Into Storage