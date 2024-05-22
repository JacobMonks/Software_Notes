# Compute Engine

## Creating Virtual Machines
There are 3 options for creating VMs with Compute Engine:

1. Google Cloud Console
2. Goodle Cloud SDK
3. Google Cloud Shell

### Create a VM Instance with Cloud Console:
Google Cloud Console is a GUI for creating and managing GCP resources. It can be accessed by going to [console.cloud.google.com](https://console/cloud.google.com) and logging in. 

1. Select a project or create a new one.
2. Create a billing account if one doesn't exist, and enable billing.
3. Navigate to Compute Engine either in the menu on the left-hand side or via the search bar.
4. Click 'Create Instance' to bring up VM configuration.
5. Specify all necessary configurations (name, region and zone, machine type, opoerating system, boot disk, etc.)

    - Not all zones have the same machine types available.
    - A machine family is a set of hardware configurations designed for particular workloads (general purpose, compute optimized, memory optimized, storage optimized).
    - Machines within a family are further organized into series and generation.
    - Applications with high security would benefit from Confidential VM Service to keep data in memory encrypted.
    - You also have the option to run a container in the VM. You can use a container in the Google Container Registry or a public repository.
    - Boot Disk types:

        - Standard - HDD
        - SSD
        - Balanced - SSD with balannce of performance and cost
        - Extreme - SSD with high performance

6. Specify a Service Account and API access.
7. Advanced Options contain features like labels, deletion protection, startup scripts (Bash or Python), Availability Policies, additional Disks, Networking, and Security configurations.

    - Standard or Spot Instances.
    - On Host Maintenance to indicate if you want to allow migration to other physical servers during maintenance.
    - Automatic Restart.
    - Use SSH keys or Shielded VMs (Secure Boot, vTPM, Integrity Monitoring)
    - Deletion Rule for boot disks to be deleted with the Instance.
    - Encryption key management.
    - Read/Write or Read Only disks.
    - Adding additional network interfaces, useful when running a server to control the flow of traffic between networks.
    - Specify Sole Tenancy.

### Create a VM Instance with Cloud SDK
1. Install Cloud SDK:

    - Instructions for installing on [Linux](https://cloud.google.com/sdk/docs/install-sdk#deb), [macOS](https://cloud.google.com/sdk/docs/install-sdk#mac), or [Windows](https://cloud.google.com/sdk/docs/install-sdk#windows).

2. After installing, initialize Cloud SDK with command:

    gcloud init

3. Copy authentication link into the browser, and copy the response code from the browser into your terminal.
4. Enter name of project. This will become the default project when issuing commands through Cloud SDK.
5. Enter the following command to create a new VM Instance:

        gcloud compute instances create [NAME-OF-INSTANCE] [zone=ZONE-NAME] [--boot-disk-size SIZE] [--boot-disk-type TYPE] [--labels KEY=VALUE] [--machine-type TYPE] [--preemptible]

    Example:

        gcloud compute instances create jm-instance-n1s8 --machine-type=e2-standard-2

### Create a VM Instance with Cloud Shell
This is an alternative to using `gcloud` commands locally.

1. Go to the Cloud Console.
2. Select the Shell icon in the upper-right corner of the browser.
3. Follow the same command process as with Cloud SDK. All `gcloud` commands with Cloud SDK also work here.

## Managing Virtual Machines

### Basics

#### Starting and Stopping
VMs can be manually started and stopped in several ways.

In Cloud Console, you can see a list of instances when navigating to the Instances tab in the left-hand menu. You can check the box next to the instance you are interested and select Start if it is dormant or Stop if it is running.

In Cloud SDk or Cloud Shell, you can enter the following start and stop commands:

    gcloud compute instances start INSTANCE-NAME
    gcloud compute instances stop INSTANCE-NAME

#### Network Access to VMs
As an engineer, you might need to log into a VM to perform administration tasks. This can be done via SSH for a Linux server or RDP with a Windows server.

In the Compute Engine dashboard, next to the Instances is an SSH dropdown menu. This allows you to open a terminal in browser, custom port, or use a separate SSH client.

#### Monitoring a VM
By going to the Monitoring tab on the VM Instance Details page, you can observe the CPU, disk, and network load of a running VM.

#### VM Cost
Tracking costs is an essential and basic management procedure.

To track costs automatically, you can enable Cloud Billing and set up Billing Export to produce daily reports on VM usage and cost.

#### General Guidelines
When working with a small number of VMs, keep these good practices in mind:

- Choose a machine type with the fewest CPUs and smallest amount of memory that still meets your requirements. VMs are billed based on what type machine is being used.
- Use console for ad hoc administration, and use shell scripting for repeatable processes.
- Use startup scripts to perform software updates and other tasks to be done on startup.
- When making modifications to a machine image, consider saving it to use for making new instances.
- Use Spot VMs if unplanned interruptions are not a concern.
- Use SSH or RDP for operating-system level tasks.
- Use Cloud Console, Cloud SDK, or Cloud Shell for VM-level tasks.