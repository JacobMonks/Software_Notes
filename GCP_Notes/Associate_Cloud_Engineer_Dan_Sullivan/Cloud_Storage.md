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
There are 4 main categories for modeling data:
1. Object storage (Cloud Storage)
2. Relational (Cloud SQL and Cloud Spanner)
3. Analytical (BigQuery)
4. NoSQL (Cloud Firestore and Bigtable)

#### Object Storage
Object Storage is a good solution when you don't need fine-grained access to data within the objects being stored. The way to do this in Google Cloud is Cloud Storage.

#### Relational
Relational databases support frequent querying transactions, and they are ideal for when users need a consistent view of the data. The primary GCP services for relational databases are Cloud SQL and Cloud Spanner.

Cloud SQL is a managed database service that provides MySQL, SQL Server, and PostgreSQL databases. These databases do not scale horizontally, but vertically.

Cloud Spanner is a service for storing large volumes of relational data and ensuring it is widely available and consistent. This would be useful for global supply chains and financial service applications, whereas Cloud SQL is better for web applications and e-commerce.

*Configuring Cloud SQL*
1. Navigate to Cloud SQL in the console and select "Create Instance."
2. Select the desired version of SQL (MySQL, PostgreSQL, SQL Server).
3. Input setup information: name, root password, region, zone.
4. Input instance configs: connectivity (public or private), machine type, automatic backups, failover replicas, database flags, maintenance windows.

*Configuring Cloud Spanner*
1. Navigate to Cloud Spanner in the console and select "Create Instance."
2. Provide instance name and instance ID.
3. Determine if regional or multi-regional.
4. Input the number of nodes.

#### Analytical
Google Cloud's service for Analytical data storage is Google BigQuery (GBQ). It is designed for data warehouse and analytical applications that can store petabytes of data, but it is not meant to be used for transaction-oriented applications like e-commerce or interactive web apps.

BigQuery is serverless and provides storage, querying, statistical, and machine learning analysis tools.

*Configuring BigQuery*
1. Navigate to Bigquery in the console.
2. Select "Create Dataset."
3. Specify the name and region.

#### NoSQL
NoSQL databases are ideal for storing data that doesn't have a defined or consistent structure. GCP has two types of NoSQL databases:
- Document-based (Cloud Firestore or Cloud Datastore)
- Wide-column (Bigtable)

Firestore is a document-based NoSQL database. Data is stored and organized into a structure called a document, which is made up of key-value pairs. A set of key-value pairs that makes up one entry is called an *entity*. Entities may have common properties, but because Firestore is schema-less, that doesn't have to be the case.

Firestore is a managed database that automatically partitions and scales data. It is used for nonanalytic, nonrelational storage, such as product catalogs, user profiles, etc. It supports transactions and indexing like a relational database, but does not have joining or aggregating data from multiple tables.

*Configuring Firestore*
1. Choose between Native Mode and Datastore Mode.
    - Native automatically scales to millions of clients and provides document-based storage.
    - Datastore automatically scales to millions of writes per second.
2. Choose storage location (single or multi-region).
3. After configuring, create entities.
    - Specify namespace (like a dataset), kind (like a table), and a key.
    - Add one or more properties that have names, types, and values.

Bigtable is another NoSQL database, but it is wide-column based instead of document-based. You can store tables with a large number of columns, but not all rows need to use every column, so the schemas are not fixed. It is designed for petabyte-scale databases for use cases like IoT data storage, data science applications, and analytics. High-volume and high-velocity are key features, and it has a latency in the range of low-milliseconds. It runs in clusters and scales horizontally.

*Configuring Bigtable*
1. Provide an instance name and instance ID.
2. Choose Production Mode or Development Mode.
    - Production clusters are highly avaialble and must be minimum 3 nodes.
    - Development clusters are low-cost without replication or high availability.
3. Choose SSD or HDD persistent disk.

### Choosing a Storage Solution
Different solutions are best for different use cases, and a full enterprise application may need multiple storage products to support everything it needs to accomplish.

Key Considerations:
1. Read and Write Patterns
    - Applications with frequent reads and writes of structured data should use Cloud SQL or Cloud Spanner if global.
    - Applications with large volumes of writes shold use Bigtable.
    - Applications that store data in files should use Cloud Storage.
2. Consistency
    - Applications that require strong consistency should use Cloud SQL or Cloud Spanner.
    - Applications that focus less on consistency should consider a NoSQL solution like Firestore and Bigtable.
3. Transaction Support
    - Applications that need atomic transactions should use Cloud SQL, Cloud Spanner, and Firestore.
    - Applications that don't need transactions can use Cloud Storage, Bigquery, or Bigtable.
4. Cost
    - Consider storage solutions that require VMs, since those also incur a cost.
5. Latency
    - Low-latency applications might use Bigtable.
    - Applications that can tolerate latency might use Cloud Spanner.

## Deploying Storage

### Cloud SQL
Create data in Cloud SQL:
1. Create a MySQL instance of Cloud SQL.
2. Start a Cloud Shell and connect to the database:

        gcloud sql connect ace-exam-mysql -user=root
        
3. From here, you can use MySQL commands to create databases and tables or to load and query data.

        CREATE DATABASE ace_exam_book;
        USE ace_exam_book;
        CREATE TABLE books (entity_id INT NOT NULL AUTO_INCREMENT, title VARCHAR(255), author VARCHAR(255), PRIMARY KEY(entity_id));
        INSERT INTO books (title, author) VALUES ('The Hobbit', 'J.R.R. Tolkien');
        INSERT INTO books (title, author) VALUES ('A Tale of Two Cities', 'Charles Dickens');
        INSERT INTO books (title, author) VALUES ('The Adventures of Huckleberry Finn', 'Mark Twain');
        SELECT * FROM books;

You can backup Cloud SQL data automatically or on-demand. To create an on-demand backup, go to the Instances page of Cloud SQL Console, select the instance, then click on the Backups menu to see options. You can also use the command:

    gcloud sql backups create --async --instance ace-exam-mysql
    
To have Cloud SQL create backups automatically, select the instance on the Instances page and click `Edit Instance`. There is an option called `Enable Auto Backups` where you can fill in details for when backups will be created and whether to enable binary logging (used for point-in-time recovery). You can also do this via command:

    gcloud sql instances patch ace-exam-mysql -backup-start-time 06:00
    
### Firestore
Firestore has two modes: Native and Datastore mode. Native mode has the benefits of real-time updates and mobile and webclient libraries. Datastore mode supports GQL (Graph Query Language) and can scale to millions of writes per second, so it is a good option when you don't need real-time or mobile features.

To add data to Firestore in Native Mode:
1. Go to Firestore Console and select `Start Collection`.
2. Create entities by filling in the form that appears.
    - provide entity IDs and documents (key-value pairs).

To back up a Firestore database:
1. Create a Cloud Storage bucket to hold the file.
2. Grant appropriate permissions to users performing the backup.
    - datastore.databases.export
    - datastore.databases.import
3. Create a backup with this command:

        gcloud firestore export gs://ace-exam-backups

4. To import a backup file:

        gcloud firestore import gs://ace-exam-backups
        
### BigQuery
BigQuery is a fully managed service, so a Cloud Engineer only has a few basic administrative tasks: estimating the cost of queries and checking job status.

To estimate the cost of a query:
1. Go to BigQuery in the console and enter a query in the Query Editor.
2. In the upper-right corner, BigQuery shows how much data will be scanned.
    - You can also do this in the command line:

            bq --location=[LOCATION] query --use_legacy_sql=false --dry-run [SQL_QUERY]

3. Go to the [Pricing Calculator](https://cloud.google.com/products/calculator), select BigQuery, and enter the name of the table, set the storage size to 0, and give the size of the query.

You can also view the status of jobs in BigQuery by going to the console and clicking `Personal History` or `Project History`. A job that has been completed will have a check mark next to it. A job that failed will have an exclamation point. You can also check job status in the command line:

    bq --location=US show -j gcpace-project:[JOB_ID]
    
### Cloud Spanner
Create and use a Cloud Spanner Instance:
1. Navigate to Cloud Spanner page in console and click `Create Instance`.
2. Click `Create Database` in the instance and give it a name.
3. Define the schema of the database:
    - Use DDL to define table structures.
4. Click `Create`.

### Cloud Pub/Sub
Deploy a Pub/Sub message queue:
1. Navigate to Pub/Sub page in console and click `Create a Topic`.
2. Go to the Topics page and select the three dots next to the topic and select `Create Subscription`.
3. Specify a subscription name and the delivery type (pull for reading, push for writing)

Once a message is read, the application readnig the message acknowledges that it received the message, and Pub/Sub will wait for a period of time specified in the Acknowledgement Deadline (10-600 seconds).

You can also specify a retention period for messages that couldn't be delivered.

Creating topics and subscriptions can also be done with gcloud commands:

    gcloud pubsub topics create [TOPIC_NAME]
    gcloud pubsub subscriptions create [SUBCRIPTION_NAME] --topic [TOPIC_NAME]
    
### Bigtable


## Loading Into Storage