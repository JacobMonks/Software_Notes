# Configuring Access and Security
Assigning permissions in Google Cloud can be done in two ways:
1. Using IAM (recommended).
2. Basic roles and scopes.

Basic roles were used before IAM, but they have more permissions than you may want a user to have.

## Identity and Access Management
Some common tasks:
- Viewing account IAM assignments
- Assigning IAM roles
- Defining custom roles

### Viewing Account IAM Assignments
Navigate to `IAM & Admin` section and select `IAM` to show a list of identities and their assinged roles.

There are 3 Basic roles: 'Owner', 'Editor', and 'Viewer'.
- Viewers perform read-only operations.
- Editors have viewer permissions and can modify an entity.
- Owners have editor permissions, can manage roles and permissions on an entity, and can set up billing.

IAM roles are collections of permissions tailored to provide identities with just the permissions they need to perform their tasks and nothing more. To see a list of users assigned a role, click the `Roles` tab on the IAM page. To do this in Cloud SDK, use the following command:

    gcloud projects get-iam-policy ace-exam-project
    

Each service in Google Cloud will have predefined roles. For example, App Engine has 5 predefined roles:
1. App Engine Admin
    - grants read/write/modify permissions (roles/appengine.appAdmin).
2. App Engine Service Admin
    - grants read-only access to configuration settings and write access to module-level and version-level settings (roles/appengine.serviceAdmin).
3. App Engine Deployer
    - grants read-only access to application configuration and settings and write access for creating new versions. Cannot modify or delete existing versions (roles/appengine.deployer).
4. App Engine Viewer
    - grants read-only access to application configuration (roles/appengine.appViewer).
5. App Engine Code Viewer
    - grants read-only access to application configuration, settings, and deployed source code. (roles/appengine.codeViewer)

### Assigning Roles
*Cloud Console*
1. Navigate to the `IAM & Admin` section of the console and select `IAM` from the menu.
2. Click the `Add` button on the top of the page.
3. Specify name of a user or group in the `New Principals` field.
4. Click `Select a role` to view a list of services and their associated roles. Choose the roles you wish to assign.

To view which fine-grained permissions are associated to a role in Cloud Console, go to the `Roles` and click the check box next to a role to display its permissions.

*Cloud SDK*
The following command will assign a role to a member in a project:

    gcloud projects add-iam-policy-binding [RESOURCE_NAME] --member=user:[USER-EMAIL] --role=[ROLE-ID]
    
Example:

    gcloud projects add-iam-policy-binding ace-exam-project --member=user:june@aceexam.com --role='roles/editor'

To view which fine-grained permissions are associated to a role in Cloud SDK:

    gcloud iam roles describe [ROLE_NAME]
    

When assigning roles, follow the Principle of Least Privilege and maintain a separation of duties between your users so that no single user has a potentially risky combination of permissions. This, for example, is why writing and deploying code are two separate permissions.

### Define Custom Roles
Define custom roles when the predefined roles do not suit your specific needs.

*Cloud Console*
1. Navigate to `IAM and Admin` and select `Roles`.
2. Click `Create Role` at the top of the page.
3. Specify a name, description, idenifier, launch stage, and set of permissions for the role.
    - Launch Stage options are: Alpha, Beta, General Availability, and Disabled.
    
Note: Not all permissions are available for custom roles.

Custom roles can have a maximum of 3000 permissions, and the total size of the title, description, and permission names must be no more than 64 KB.


*Cloud SDK*
Define custom role:

    gcloud iam roles create [ROLE-ID] --project [PROJECT-ID] \
            --title=[ROLE-TITLE] --description=[ROLE-DESCRIPTION] \
            --permissions=[PERMISSIONS-LIST] --stage=[LAUNCH-STAGE]

Example:

    gcloud iam roles create customAppEngine1 --project ace-exam-project \
            --title='Custom Update App Engine' --description='Custom Update' \
            --permissions=appengine.applications.update --stage=alpha
            

## Managing Service Accounts
Sercice Accounts provide an identity independent of human users. They are assigned to VMs, and those VMs can use the permissions associated with that service account.

Cloud Engineers will be expected to know how to:
1. Work with scopes.
2. Assign Service Accounts to a VM.
3. Grant access to a service account to another project.

### Service Accounts and Scopes
Scopes are permissions granted to a VM to perform specific operations. They authorize access to API methods. To configure access controls for a VM, you must configure both IAM roles and scopes.

A scope is identified by a URL starting with 'www.googleapis.com/auth' and followed by a permission on a resource.
- For example: 
    - This scope allows a VM to insert data into BigQuery: `www.googleapis.com/auth/bigquery.insertdata`
    - This scope allows a VM to view Cloud Storage data: `www.googleapis.com/auth/devstorage.read_only`
    - This scope allows a VM to write to Compute Engine logs: `www.googleapis/auth/logging.write`
    
An instance can only perform an operation if it is allowed by both the assigned IAM roles and the scopes defined on the instance.

#### Setting Scopes

*Cloud Console*
1. Navigate to the VM Instance page Cloud Console.
2. Stop the instance (if it is running), go to Instance Details and click `Edit`.
3. Scroll down to the `Access Scopes` section and select a scope:
    - Allow Default Access
    - Allow Full Access to All Cloud APIs
    - Set Access for Each API

*Cloud SDK*
This command will set a scope on a VM:

    gcloud compute instances set-service-account [INSTANCE_NAME] \
            [--service-account [SERVICE_ACCOUNT_EMAIL] | --no-service-account] \
            [--scopes [SCOPES,...] | --no-scopes]
            
Example:

    gcloud compute instances set-service-account ace-instance \
            --service-acount examadmin@ace-exam-project.iam.gserviceaccount.com \
            --scopes compute-rw,storage-ro
            
### Assigning a Service Account to a VM

*Cloud Console*
1. Navigate to the Service Accounts section of `IAM & Admin` in the Console.
2. Click `Create Service Account`.
3. Specify the name, ID, and a description then click `Create and Continue`.
4. Assign roles using either Cloud Console or SDK.
5. Navigate to the VM Instances page in Compute Engine, select a VM Instance and click `Edit`.
6. Scroll down to `Service Account` and select the newly created Service Account.

*Cloud SDK*
You can assign a service account when you create a VM:

    gcloud compute instances create [INSTANCE_NAME] \
            --service-account [SERVICE_ACCOUNT_EMAIL]
            
### Grant Access to Projects
Navigate to the IAM page of Cloud Console and add a member and supply the service account email.

### Audit Logs
Navigate to Cloud Logging in Cloud Console. Here you can select the resources, types of logs to diplay, the log level, and period of time.
