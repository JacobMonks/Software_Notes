# GCloud Commands
These are for using Google Cloud SDK or the Cloud Shell.

There are four maain command-line tools to use with GCP:
1. `gcloud` - used for most products, but not all.
2. `gsutil` - used for Cloud Storage, can also use `gcloud storage`.
3. `bq` - used for BigQuery.
4. `cbt` - used for Bigtable.

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


### Disk/Snapshot/Image commands:

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

## Bigtable Commands:

| Command                                    | Function               |
|:-------------------------------------------|:-----------------------|
| cbt createtable [NAME]                     | Create a table         |
| cbt ls                                     | List tables            |
| cbt createfamily [NAME]                    | Create a column family |
| cbt set [TABLE] row1 [COLFAM]:col1=[VALUE] | Set a cell value       |
| cbt read [TABLE]                           | Display table contents |