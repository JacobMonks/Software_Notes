# GCP Storage Technologies
Many factors should be taken into account when selecting the storage solution for your use case. This includes, but is not limited to, short- vs long-term storage, cost, availability, the data structure, and the amount of data needed to be stored. Data engineers will likely need to consider stream vs batch processing and scalability, which are necessary things to consider when working with machine learning models.

## Business Requirements
The data lifecycle stages:

1. Ingest
2. Store
3. Process/Analyze
4. Explore/Visualize

### Ingestion
Three main modes of data ingestion - Application, streaming, and batch data.

**Application Data**

This is the data that is generated while an application is running. User-generated data, event data, and log data are some examples. It can be ingested by services running in Compute Engine, Kubernetes, App Engine, etc. and can be written to a managed database like Cloud SQL or to Stackdriver Logging.

**Streaming Data**

This data is typically transferred continuously in small messages from a data source. Examples include sensor data from IoT hardware or monitoring data from a VM. It usually includes a timestamp to indicate the time of being generated, and it may also include process time which denotes when the data arrived at the beginning of the ingestion pipeline. Time data can be useful when running an application that depends on data being in the proper sequence, which means some buffering and processing will need to be done for date that arrives late. Cloud Pub/Sub is designed specifically for ingesting streaming data, with options to buffer the data as needed.

**Batch Data**

This describes data intended to be ingested in bulk, and it is usually stored in files. An example could be data that is collected by applications and stored in a database that is then exported. Google Cloud Storage is GCP's object storage system and is often used as a data lake with batch data. Some other solutions like Cloud Transfer Service and Transfer Appliance could help with transferring large quantities of data.

### Storage
This step of the data lifecycle focuses on making the data available for processing and analysis. Key things to consider are:

- How data is being accessed
- Access control
- The length of storage time
- How the data is structured

**Data Access Patterns**

A transaction processing application would need row-based access to get specific records, so something like Cloud SQL or Cloud Datastore could be a good fit.

A machine learning pipeline needs to grab large volumes of training data in bulk, so Cloud Storage might be the ideal solution.

Cloud Filestore allows you to access files as though it was a traditional file system.

**Access Control**

Relational Databases provide tools to restrict acces on the table and view level. Permissions can be granted to allow users to view, update, and/or write data, or any combination thereof, and you can use views to restrict which data they can see in a table. This is known as fine-grained security.

Cloud Storage has more broad access control. Permissions exist on the bucket level and the object level, but any data stored in that object can be accessed since objects are all treated as atomic units, regardless of the amount of data stored therin. This would be coarse-grained security.

There are examples of services that don't follow these basic patterns. BigQuery is an analytical database used for data warehousing and analytics. It only supports access controls on the dataset level, but you can create authorized views in a dataset that reference tables from a more restricted dataset.

**Time to Store**

Data that you only need temporarily while running an application on a Compute Engine instance could simply use a local SSD.

A lot of data is needed for longer than one VM instance. Cloud Storage is reliable, long-term, and offers multiple storage lifecycle policies to help optimize costs for data that is not accessed very frequently, such as Nearline and Coldline storage. Data needed long-term for analytics is best stored in BigQuery.

Data that is frequently accessed and/or updated should be in a relational or NoSQL database. As data in a database grows older and becomes less necessary for applications, it makes sense to export and store it in Cloud Storage.

### Processing and Analysis
In this step, data is transformed and prepared to make it readily available for querying and analysis.

**Data Processing**

Data cleansing is the process of identifying and dealing with erroneous data. This could be as simple as deleting rows or substituting the incorrect information with a 0 or NULL. It may also require applying business logic to the data, which can vary greatly depending on the use case. For example, a person's credit card cannot be charged with an amount that is larger than the credit line allows, so any data for that kind of transaction should be dealt with accordingly.

Whether to delete or keep problematic data depends on the use case. Important business transactions like customer orders should probably be kept and corrected, but for sensor data that is aggregated every hour, it is less important to keep individual rows.

Data transformation may also entail normalizing and/or standardizing data. Phone numbers, zipcodes, and other information can be written in a variety of different ways, and the system should be able to accommodate when people exclude an area code or have no hyphens. Cloud Dataflow is a good tool for processing both streamed and batch data.

**Data Analysis**

When analyzing data, there are many techniques one can use to extract meaningful information. Statistical analysis can give the mean, median, mode, standard deviation, and any outliers of numerical data. You can also produce correlations between multiple variables, make regression models for estimation or prediction, and cluster data to identify demographic or behavioral trends.

Tools for data analysis in GCP include Dataflow, Dataproc, BigQuery, and ML Engine.

### Exploration and Visualization
When you need to test a hypothesis or gain deeper insight from the data, you may need to use tools to explore the data. Cloud Datalab is a tool for analyzing and visualizing datasets with support for popular data science libraries like pandas, TensorFlow, and scikit-learn.

Google Data Studio allows you to create tables, charts, etc. and requires little to no knowledge of programming.

## Data Qualities
After narrowing down business requirements, it's important to understand the technical qualities of data.

- Volume
- Velocity
- Variation in structure
- Data Access patterns
- Security requirements

**Volume**

Some services are optimized for large volumes of data, while others are better suited for smaller amounts.

- Memorystore
    - Depends on system choice (Redis, Redis Cluster, Valkey, Memcached)
    - Redis: 16 databases per instance, 1 TB per region
    - Redis cluster and Valkey: 1 database per instance, up to 64,000 client connections
    - Memcached: 100 nodes per region, 65,000 client connections per node, 10 TB per region
- Cloud Storage
    - Objects can be 5 TB
    - No I/O limit
- Cloud Bigtable
    - 16 TB per HDD node, or 5 TB per SSD node
    - 1000 tables per instance
- BigQuery
    - No limit on number of tables
    - 4000 partitions per table
- Compute Engine
    - Attached disks can have up to 64 TB
- Cloud SQL
    - 100 instances of old SQL architecture per project
    - 1000 instances of new SQL architecture per project
    - Dedicated core instances 64 TB, shared instances 3 TB
    - MySQL 16 TB max table size, PostgreSQL 32 TB
    - Good for relational database needs in a single region
- Cloud Firestore
    - 1 MB per document
    - 100 databases per project

**Velocity**

Velocity describes the rate at which data is transferred and processed. User-generated data sush as personal data from mobile apps and web apps tend to be low-velocity, while machine-generated data like from an IoT device can be very high velocity.