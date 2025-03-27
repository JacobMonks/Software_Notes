# Monitoring, Logging, and Cost Estimating
Google has a service called Cloud Operations Suite, which provides monitoring, logging, and tracing.
- Create alerts based on resource metrics.
- Creating log sinks to store logging data.
- Viewing and filtering log data.
- Price Calculator for estimating costs.

## Cloud Monitoring
Cloud Monitoring is a service for collecting performance metrics, logs, and event data from cloud resources.
- CPU utilization
- Number of bytes written
- Execution times
- CPU load

Cloud Monitoring works in hybrid environments and has support for GCP, AWS, and on-premises resources.

Suppose you are working with a VM with Apache Server and PHP. The VM will collect basic logs and metrics, but you can install the Ops Agent on the VM to get more detailed data:

    curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
    sudo bash add-google-cloud-ops-agent-repo.sh --also-install
    
A VM with Ops Agent installed will send any data to Cloud Logging and Cloud Monitoring.

When navigating to Cloud Monitoring, you will see some information on any health check incidents, relevant blog information, and a list of available dashboards. Some default dashboards include App Engine, BigQuery, Cloud Storage, Firewalls, and VPN.

You can create a custom dashboard to show the metrics you are most interested in, with various chart types to choose from.

### Metric Explorer
Metric Explorer is a feature that lets you select from a wide variety of different metrics to track on your dashboard. Metric Explorer can be very useful if you are investigating an issue and need to view a variety of metrics.

### Create Alerts
Alerts will automatically notify you when some metric crosses a defined threshold. The Alerting page in Cloud Monitoring shows a summary of the incidents firing, incidents responded to, and alert policies.

E.g. a policy that alerts you when there are 5 minutes or more of backlogged Pub/Sub messages on a given topic.

To set an alert, create a policy for a metric:
- Condition type (metric data threshold or metric data absence)
- Alert trigger:
    - Any Time Series Violates
    - Percent Of Time Series Violates
    - Number Of Time Series Violates
    - All Time Series Violates
- Notification channel
    - Email
    - Slack
    - SMS
    - Cloud Pub/Sub
    - PagerDuty
    - Webhooks
- Auto-close time
- Labels
- Documentation
    
Do not create too many alerts, this can create *alert fatigue*, where engineers receive so many alerts they stop responding to them. Use Alerts for incidents that are not likely to resolve on their own, and set thresholds that are long enough to ignore small spikes that go away quickly.

## Cloud Logging
Cloud Logging is a service for collecing, storing, filtering, and viewing log and event data. It is a managed service, so no server configuration is necessary.
- Configure log routers
- Configure log sinks
- View and filter logs
- view message details

### Log Routers and Sinks
Log data ingested by Logging API is routed to one of three types of sinks:
1. Required Log Sink
    - Holds admin activity, system events, and access transparency logs and stores them for 400 days (not configurable).
2. Default Log Sink
    - Holds any log messages that don't get sent to Required log sink, messages are stored for 30 days by default.
3. User-Defined Log Sink
    - Can be created in a Cloud Storage bucket, and the retention policy is customizable

Sinks are associated to a billing account, project, folder, or organization. Each of these resource has a Required and a Default log sink created automatically by Google.

Log Router is a service that applies filters to incoming logs to direct them to the proper log sink(s).

Cloud Logging also supports log metrics. If a log message meets some log metric pattern, it can be reflected in Cloud Monitoring.

You can also send logs to Cloud Storage, Pub/Sub, and BigQuery for analysis or gaining insights.

### Viewing and Filtering Logs
Navigate to Cloud Logging in the console and use the Log Explorer. This allows you to view messages and filter them based on time, resource type, severity level, and log query.

When viewing message details, each log appears as a single line that can be expanded to show *insertId*, *logName*, *receiveTimestamp*, *protoPayload*, and *resource*.
- The protoPayload can be expanded to view *authenticationInfo*, *authorizationInfo*, *requestMetadata*, *methodName*, *resourceName*, *response*, etc.

## Cloud Trace
Cloud Trace is a distributed system for collecting latency data from a running application. This is good for finding performance degradation.

A "trace" is generated when developers specifically call Cloud Trace from their applications. You can see all traces in a project and create reports using the Cloud Trace console.

## Google Cloud Status
The [Google Cloud Status Dashboard](https://status.cloud.google.com) allows you to see the status of Google Cloud services in different regions. It will show 3 states:
1. Available
2. Service Disruption
3. Service Outage

## Price Calculator
To get an idea of the cost of configuring different Google Cloud services, you can use the [Price Calculator](https://cloud.google.com/products/calculator). You can select which service you'd like to evaluate and enter the configuration details like storage capacity, number of instances, machine type, average use time, and OS. Different services will require different parameters to come to an estimate.