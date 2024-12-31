# Cloud Functions
Cloud Functions is a serverless compute service for running short-lived functions. It is ideal for event-driven processing.

- Up to 60 minutes for HTTP functions.
- Up to 10 minutes for event-driven functions.

There are two generations of Cloud Functions. The second generation offers expanded capability due to larger instances, greater concurrency, traffic management, and support for Eventarc, which is a service that manages event workflow in microservices architectures.

## Events, Triggers, and Functions
*Events* are actions that occur in the cloud, such as files being uploaded or databases being updated.

First generation Cloud Functions supported events from:
- HTTP
- Cloud SQL
- Cloud Pub/Sub
- Cloud Firestore
- Cloud Firebase

Second generation Cloud Functions uses Eventarc triggers, which has support for:
- Cloud Task
- Cloud DNS
- Cloud Dataproc
- Network Management
- OAuth 2.0

A *trigger* is a way to respond to an event taking place. These triggers have an associated *function* that will execute in response.

## Runtime Environments
Each instance of a function runs in its own environment, completely isolated from each other. If you need to coordinate functions to share or aggregate data, you should consider using a database or a file in storage for keeping track of that information.

Google supports these runtime environments:
- Python
- Go
- Node.js
- Ruby
- Java
- .NET
- PHP

See the [docs](https://cloud.google.com/functions) for more information on supported languages and versions.

## Receiving Events from Storage
Several actions in Cloud Storage can be used as a trigger for running functions. These include files being finalized, deleted, archived, or having updated metadata.

### Deploying in Cloud Console
Steps:
1. Enable Cloud Functions API if not done already.
2. Go to Cloud Functions console, select "Create Function," and enter the following information:
    - Function Name
    - Region
    - Trigger (Cloud Storage)
    - Bucket
3. Continue down and fill in these settings:
    - Memory Allocated (128 MB to 16 GB)
    - Source Code
    - Runtime
    - Function
    - Encryption
4. View your created fucntion in the console.

### Deploying in Cloud SDK and Cloud Shell
Steps:
1. Ensure you have the latest *gcloud* commands installed:

        gcloud components update
        gcloud components install beta (optional)
    
2. Enter the function you want to create using *gcloud functions deploy* command:

        gcloud functions deploy storage_test \
                --runtime python39 \
                --trigger-resource [bucket_name] \
                --trigger-event google.storage.object.[finalize, delete, archive, metadataUpdate]
                
3. When finished, delete the function:

        gcloud functions delete storage_test

## Receiving Events from Pub/Sub
You can also create Functions that respond to messages being published to a Pub/Sub queue. When messages are sent via Pub/Sub, they are encoded to allow for binary data in place of text. As a result, when your function reads these messages in, you should use binary decoding before reading the message. E.g.

    def pub_sub_reader(event_data, event_context):
        import base64
        print(f'Event Type: {event_context.event_type}')
        if 'name' in event_data:
            name = base64.b64decode(event_data['name']).decode('utf-8')
            print(f'Message Name: {event_data[name]}')
            

### Deploying in Cloud Console
Steps:
1. Navigate to Cloud Functions console and select "Create Function."
2. Enter the following information:
    - Function Name
    - Region
    - Trigger (Pub/Sub)
    - Topic (select or create a new one)
    - Encryption

### Deploying in Cloud SDK and Cloud Shell
Steps:
1. Enter the command:

        gcloud functions deploy pub_sub_reader \
                -- runtime python39 \
                --trigger-topic [topic_name]
                
2. When finished with the function, delete it.

        gcloud functions delete pub_sub_reader