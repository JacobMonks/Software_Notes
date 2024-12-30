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

See [the docs](https://cloud.google.com/functions) for more information on supported languages and versions.

## Receiving Events from Storage
