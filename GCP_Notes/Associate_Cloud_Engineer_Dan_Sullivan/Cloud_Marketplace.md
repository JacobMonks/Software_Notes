# Cloud Marketplace
Cloud Marketplace is a repository of applications and data sets that can be deployed to your Google Cloud environment. You can deploy applications with the necessary storage, compute, and network resources without needing to configure them manually.

The main page of Marketplace shows some featured solutions. From there, you can either search or browse by filter for the solution you want.
- Filters include the category of solution, such as big data, analytics, machine learning, etc.

You can select an available operating system in the Marketplace. These OSs can have different license types. They can be free, pay-per-use, or BYOL (bring your own license).

Some developer tools in Marketplace include WordPress, Joomla, and Alfresco. Clicking on these will display an overview of the tool's capabilities, pricing details, and where the resources will reside in Google Cloud. You may also get links to documentation for the tool.

## Deploying Cloud Marketplace Solutions
Once you find a solution that fits your specifications, you can launch it by navigating to the solution's overview page in Marketplace and selecting `Launch`.
- You may be prompted to enable one or more APIs in order to launch the solution.

You will specify a name for the deployment, a zone, and the machine type. You can choose the type and size of a persistent disk. In the Networking section, you can specify the network and subnet along with firewall rules.

When you are satisfied with your selections, click `deploy` to launch it and open the Deployment Manager, which shows the progress of the deployment. Once the launch completes, you will see a summary about the deployment a button to launch the admin panel.

## Building Infrastructure
You can create your own solution configuration files so that users can launch preconfigured solutions using Deploymen Manager configuration files as well as Terraform-based specifications.
- Terraform is an open-source tool for specifying infrastructure as code.

### Deployment Manager
Deployment Manager config files are written in YAML syntax, starting with the word `resources`, then resource entities which have 3 fields:
- name
- type
- properties

For example, this YAML file defines a VM:

    resources:
    - type: compute.v1.instance
      name: ace-exam-deployment-vm
      properties:
        machineType: www.googleapis.com/compute/v1/projects/[PROJECT_ID]/zones/us-central1-f/machineTypes/f1-micro
        disks:
        - deviceName: boot
          type: PERSISTENT
          boot: true
          autoDelete: true
          initializeParams:
            sourceImage: www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/[FAMILY_NAME]
          networkInterfaces:
          - network: www.googleapis.com/compute/v1/projects/[MY_PROJECT]/global/networks/default
            accessConfigs:
            - name: External NAT
              type: ONE_TO_ONE_NAT
              
With more complicated Deployment configurations, use a deployment template.
- A text file used to define resources and import them into configuration files.
- Python and Jinja2 are recommended for creating template files.

You can launch a deployment template with:

    gcloud deployment-manager deployments create quickstart-deployment -config=vm.yaml
    
    
### Cloud Foundation Toolkit
Cloud Foundation Toolkit is an open-source service used for streamlining the deployment of infrastructure as code using Deployment Manager and Terraform templates. The toolkit includes blueprints, which are packages of deployable config specifications and policies. Blueprints are available for Terraform and Kubernetes.

Example blueprints can be found [here](https://github.com/docs/terraform/blueprints/terraform-blueprints).

### Config Connector
Config Connector is a Kubernetes add-on that allows you to manage Google Cloud resources through Kubernetes.

To install Config Connector:

    gcloud container clusters create ace-gk1-cluster1 \
        -- addons ConfigConnector
        --workload-pool=ace-project-dw1
        --logging=SYSTEM
        --monitoring=SYSTEM
        
To use ConfigConnector, you will need to enable Workload Identity to link IAM identities to Kubernetes identities.
