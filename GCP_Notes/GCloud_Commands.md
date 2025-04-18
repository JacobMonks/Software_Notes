# GCloud Commands
These are for using Google Cloud SDK or the Cloud Shell.

There are four maain command-line tools to use with GCP:
1. `gcloud` - used for most products, but not all.
2. `gsutil` - used for Cloud Storage, can also use `gcloud storage`.
3. `bq` - used for BigQuery.
4. `cbt` - used for Bigtable.
5. `kubectl` - used for Kubernetes Clusters.

## GCloud-Wide Flags
These are flags that can be added to any gcloud command if applicable.

| Flag            | Function                                                            |
| :-------------- | :------------------------------------------------------------------ |
| --account       | Specifies an account to override default account.                   |
| --configuration | Uses named configuration file with key-value pairs.                 |
| --flatten       | Generates separate key-value records for keys with multiple values. |
| --format        | Specifies output format (csv, json, yaml, text, etc.)               |
| --help          | Displays detailed help messages.                                    |
| --project       | Specified a project to override the default project.                |
| --quiet         | Disables interactive prompts and uses defaults.                     |
| --verbosity     | Specifies the level of outpu messages (debug, warning, or error).   |
| --zone          | Specifies a zone to override the default zone.                      |

## Compute Engine Commands
All Compute Engine commands start with:

    gcloud compute


### Instance Commands
For making commands regarding instances:

    gcloud compute instances


| Command/Flag                | Function                                                            |
| :-------------------------- | :------------------------------------------------------------------ |
| start [names]               | Starts instance(s).                                                 |
| --async                     | Returns immediately without waiting for operations to complete.     |
| zones list                  | Shows the list of zones.                                            |
| stop  [names]               | Stops instance(s).                                                  |
| delete [names]              | Deletes instance(s).                                                |
| --delete-disks=VALUE        | Deletes the disk when the VM is deleted (all, boot, data).          |
| --keep-disks=VALUE          | Saves disks when the VM is deleted (all, boot, data).               |
| list [--filter="zone:ZONE"] | Lists all instances [in a specified ZONE].                          |
| --limit                     | Limit the number of VMs listed.                                     |
| --sort-by                   | Reorder the list of VMs by specifying a resource field.             |
| describe                    | See all resource fields.                                            |


### Disk/Snapshot/Image Commands

| Command/Flag                                            | Function                                |
| :------------------------------------------------------ | :-------------------------------------- |
| disks snapshot DISK_NAME --snapshot-names NAMES         | Create a snapshot of a disk.            |
| snapshots list                                          | View list of snapshots.                 |
| snapshots describe SNAPSHOT_NAME                        | View details about a snapshot.          |
| disks create DISK_NAME --source-snapshot=SNAPSHOT_NAME  | Create a disk.                          |
| --size=SIZE                                             | Specify disk size.                      |
| --type=TYPE                                             | Specify disk type.                      |
| images create IMAGE_NAME                                | Create a new image.                     |
| --source-disk/image/image-family/snapshot/uri=SOURCE    | Specify a source file for the image.    |
| images delete IMAGE_NAME                                | Delete an image.                        |
| images export --destination-uri=URI --image=IMAGE_NAME  | Store an image to Cloud Storage.        |


### Instance Group Commands

| Command/Flag                                      | Function                                                                 |
| :------------------------------------------------ | :----------------------------------------------------------------------- |
| instance-templates create INSTANCE                | Create an instance template.                                             |
| --source-instance=NAME                            | Use an existing Instance as a source for creating an instance template.  |
| instance-templates delete NAME                    | Delete an instance template.                                             |
| instance-templates list                           | List all instance templates.                                             |
| instance-groups managed list-instances            | Lists all instance groups.                                               |
| instance-groups managed list-instances GROUP_NAME | List all instances in an instance group.                                 |

## Kubernetes Engine Commands
The basic command for Kubernetes Engine clusters:

    gcloud container

| Command                                                                    | Function                                                    |
|:---------------------------------------------------------------------------|:------------------------------------------------------------|
| gcloud container clusters create cluster1 --num=nodes=3 --region=[REGION]  | Create a Standard Mode cluster                              |
| gcloud container clusters create-auto                                      | Create an Autopilot cluster                                 |
| gcloud container clusters list                                             | List the names and basic info of all clusters               |
| gcloud container clusters describe --zone=[ZONE] standard-cluster-1        | View the details of a cluster                               |
| gcloud container clusters get-credentials --zone=[ZONE] standard-cluster-1 | Configure the kubeconfig file and fetch authentication data |
| gcloud container images list                                               | List the container images                                   |
| gcloud container images describe                                           | Get details about an image                                  |
| gcloud container clusters resize standard-cluster-1 --node-pool default-pool -num-nodes # --region=us-central1 | Increase the size of a node pool |
| gcloud container clusters update standard-cluster-1 --enable-autoscaling --min-nodes 1 --max-nodes 5 --zone us-central1-a --node-pool default-pool | Update a cluster to enable autoscaling |

The command for managing Kubernetes Containers:

    kubectl

| Command                                                                | Function                                                  |
|:-----------------------------------------------------------------------|:----------------------------------------------------------|
| kubectl run                                                            | Create a deployment on a cluster                          |
| kubectl scale deployment app-deploy1 --replicas=#                      | Scale up the number of replicas in a deployment           |
| kubectl get nodes                                                      | List all nodes                                            |
| kubectl get pods                                                       | List all pods                                             |
| kubectl describe nodes                                                 | Show more details about nodes                             |
| kubectl describe pods                                                  | Show more details about pods                              |
| kubectl get deployments                                                | List deployments                                          |
| kubectl autoscale deployment nginx-1 --max 10 --min 1 --cpu-percent 80 | Autoscale a deployment up to a max number of pods based on CPU usage |
| kubectl delete deployment nginx-1                                      | Remove a deployment                                       |
| kubectl get services                                                   | List all services                                         |
| kubectl create deployment app-deploy1 --image=app1 --port=8080         | Start a service and make it accessible on port 8080       |
| kubectl expose deployment app-deploy1 --type="LoadBalancer"            | Expose a deployment to be accessible to outside resources |
| kubectl delete service app-deploy1                                     | Remove a service                                          |

## Cloud Storage Commands

| Command                                                   | Function                                        |
|:----------------------------------------------------------|:------------------------------------------------|
| gsutil mb [NAME]                                          | Create a bucket                                 |
| gsutil cp [LOCAL_OBJECT] gs://[DESTINATION_BUCKET]/       | Copy object from local device to bucket         |
| gsutil cp gs://[OBJECT_LOCATION] [LOCAL_DESTINATION]/     | Copy file from bucket to local spot (or VM)     |
| gsutil mv gs://[OBJECT_LOCATION] gs://[DESTINATION]/      | Move object from one bucket/location to another |
| gsutil acl get gs://[BUCKET]/[FILE]                       | Get the permissions on a bucket or object       |
| gsutil acl set gs://[BUCKET]/[FILE]                       | Set the permissions on a bucket or object       |
| gsutil acl ch -u [USER]:[PERMISSION] gs://[BUCKET]/[FILE] | Change permissions on a bucket or object        |

## Cloud SQL Commands

| Command                                                                     | Function                        |
|:----------------------------------------------------------------------------|:--------------------------------|
| gcloud sql instances describe [INSTANCE]                                    | Show details about instance     |
| gcloud sql export sql [INSTANCE] gs://[BUCKET]/[FILE].sql --database=[DATABASE] | Export a database to a file |
| gcloud sql import sql [INSTANCE] gs://[BUCEKT]/[FILE] --database=[DATABASE] | Import data from a file         |

## Cloud Firestore Commands

| Command                                                                      | Function                   |
|:-----------------------------------------------------------------------------|:---------------------------|
| gcloud firestore export gs://$[BUCKET]                                       | Export data in Native Mode |
| gcloud datastore export --namespace=[NAME] gs://$[BUCKET]                    | Export in Datastore Mode   |
| gcloud datastore import gs://$[BUCKET]/[PATH]/[FILE].overall_export_metadata | Import data into Firestore |

## BigQuery Commands

| Command | Function |
|:--------|:---------|
| bq extract --destination_format [FORMAT] --compression [TYPE] --field_delimiter [DELIMTIER] --print_header [BOOLEAN] [PROJECT]:[DATASET].[TABLE] gs://[BUCKET]/[FILENAME] | Export data from BQ |
| bq load --autodetect --source_format=[FORMAT] [DATASET].[TABLE] [PATH_TO_SOURCE] | Load data from source file |

## Bigtable Commands

| Command                                    | Function               |
|:-------------------------------------------|:-----------------------|
| cbt createtable [NAME]                     | Create a table         |
| cbt ls                                     | List tables            |
| cbt createfamily [NAME]                    | Create a column family |
| cbt set [TABLE] row1 [COLFAM]:col1=[VALUE] | Set a cell value       |
| cbt read [TABLE]                           | Display table contents |

## Dataproc Commands

| Command                                                                     | Function                     |
|:----------------------------------------------------------------------------|:-----------------------------|
| gcloud dataproc clusters export [CLUSTER_NAME] --destination=[PATH_TO_FILE] | Export cluster configuration |
| gcloud dataproc clusters import gs://[SOURCE_FILE]                          | Import cluster configuration |

## Cloud Pub/Sub Commands

| Command                                                                     | Function               |
|:----------------------------------------------------------------------------|:-----------------------|
| gcloud pubsub topics create                                                 | Create a new topic     |
| gcloud pubsub subscriptions create [SUBSCRIPTION_NAME] --topic [TOPIC_NAME] | Create a subscription  |
| gcloud pubsub topics publish [TOPIC_NAME] --message [MESSAGE]               | Send data to a topic   |
| gcloud pubsub topics pull --auto-ack [SUBSCRIPTION_NAME]                    | Read data from a topic |