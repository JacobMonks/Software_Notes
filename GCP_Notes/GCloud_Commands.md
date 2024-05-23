# GCloud Commands
These are for using Google Cloud SDK or the Cloud Shell.

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
All Compute Engine instance commands start with:

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