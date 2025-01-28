# Projects, Service Accounts, and Billing

## Organizing Google Cloud Projects
When you start using multiple different services in Google Cloud, it becomes important to be able to organize and conveniently track resources. A resource hierarchy is Google Cloud's abstraction for managing cloud resources.

Hierarchy:

- Organization
    - Folder
        - Project
    
### Organization
An organization is the root of the hierarchy and is usually mutually exclusive with a single company. If your company uses Google Workspace (Docs, Gmail, Drive, etc.), you can also create an Organization in the Google Cloud hierarchy, otherwise you can also use Cloud Identity.

A single cloud identity is exclusive to one company. A cloud identity will have one or more super admins, and the super admins assign the role of Organization Administrator Identity and Access Management (IAM) to users who manage the organization. Google will automatically grant all users in the domain the IAM roles of Project Creator and Billing Account Creator, allowing all users to create new projects and enable billing for resources.

Users with Organization Administrator IAM roles are responsible for:

1. Defining the structure of the resource hierarchy.
2. Defining IAM policies.
3. Delegating other management roles to users.

### Folders
An Organization will contain Projects and Folders of Projects. Folders enable a multi-layer hierarchy, and they are useful for organizing the services provided by different cloud resources and the policies that govern them.

For example, a company's software department will have different rules for development, testing, staging, and production, so it makes sense for each of those environments to exist in a different Folder.

### Projects
A Project in Google Cloud is the primary way to manage our work in the cloud. By making a Project, the user can create resources, manage permissions, oversee billing, and use the many services that Google Cloud provides.

As mentioned, when an Organization is created, all users in that domain are given Project Creator and Billing Account Creator roles, which enables all users to create new Projects. An Organization has a quota of Projects it can create, and if it wants to exceed that quota, it must request an increase.

## Organization Policies
In addition to IAM, Google also provides an Organization Policy Service. While IAM manages the permissions of users to work with resources, Organization Policy puts restrictions on how those resources can be used. It does this using Constraints, which can come in List form or Boolean form.

- List Constraints are lists of values that are allowed or denied for a resource.
- Boolean Constraints are True or False values, and they determine whether or not a constraint is applied.

Organization Policies can be applied individually to each resource, like denying serial port access on all VMs, but a more convenient method is to set the policy on the whole organization, since all folders and projects in the organization will inherit that policy by default.

## Create a Project
1. Navigate to the [Google Cloud console](https://console.cloud.google.com) and log in.
2. Using the menu in the upper-left corner, select 'IAM & Admin,' and then select 'Manage Resources.'
3. Click 'Create Project.' Enter the project name and the organization. Your remaining quota of projects is displayed.

## Roles and Identities
A role is a collection of permissions granted to users. There are 3 types of roles:

1. Basic (Primitive) role

    - Includes Owner, Editor, and Viewer privileges, which provide a broad range of privileges that may not always be needed.

2. Predefined role

    - Provides more specific access to resources, such as appengine.appAdmin, appengine.ServiceAdmin, or appengine.appViewer.

3. Custom role

    - Allow cloud managers to create and administer their own roles using permissions defined in IAM.

After creating roles, you can assign them to users using the IAM console. General best practice is to follow the principle of least privilege.

## Service Accounts
Service Accounts are an extra layer of abstraction for users when you don't wish to grant them access using roles. A service account acts as its own user with its own roles, and it can be called in an application when the permissions in those roles are required.

For example, you don't want any individual user to have direct read/write access to a database, but you still need that database to be manipulated for business operations. By creating a service account, you can load the credentials for the service account in the application which will allow the database to be accessed by the application.

There are 2 types:

1. User-managed Service Accounts
2. Google-managed Service Accounts

Users can create up to 100 service accounts per project.

Service accounts are created automatically when resources are created, such as VMs.

## Billing
Using Google Cloud resources usually incurs a fee, so it would be wise to set up a Billing Account using the Google Cloud Billing API.

A Billing Account stores all the information for making payments for any resources you use in a project or group of projects. All projects must be associated with a Billing Account unless they only use free services.

You can set up one or multiple Billing Accounts in an organization, and they can be structured similarly to the resource hierarchy. If your company has finance, legal, and marketing departments that pull from the same budget, they can be covered under one Billing Account, while the software department can have their own Billing Account.

There are two types of Billing Accounts:

1. Self-service

    - Paid for using a credit/debit card associated with a bank account.
    - Charged automatically.

2. Invoiced

    - Bills are sent to customers to be paid.
    - Good for large enterprises.

There are 4 Billing Roles to be familiar with:

1. Billing Account Creator can create new self-service accounts. Very few people will have this role.
2. Billing Account Administrator manages accounts but can't create them. Cloud admins will likely have this role.
3. Billing Account User enables a user to link projects to accounts. Any user who creates projects will have this role.
4. Billing Account Viewer enables a user to view account cost and transactions. This is useful for auditors who need to be able to read billing information without changing it.

### Billing Budgets and Alerts
Google Cloud Billing allows you to define a budget and set billing alerts. You can do this by going to the main console menu, selecting 'Billing', then selecting 'Budgets and Alerts.'

When filling out the billing form, you can specify which billing account to monitor, and it will notify you when certain percentages of your defined budget has been spent in a given period of time. By default, it will send notifications at 50, 90, and 100 percent, but you can change those thresholds and the number of alerts.

A neat feature is that the billing alerts can be sent in Pub/Sub, so you can respond to the alerts programmatically.

### Exporting Billing Data
Billing data can also be exported to BigQuery for analysis. You will need to create a data set in BigQuery.

Previously, you could also export billing information to Cloud Storage, but that is no longer supported.

## Enabling APIs
Google Cloud uses APIs to make their services programmatically accessible. By default, most services have their APIs disabled, and you will need to actively enable them. To do so, you can select 'APIs & Services' in the main console menu, which will display a dashboard and a list of services that you can enable.
