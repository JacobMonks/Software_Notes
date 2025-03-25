# Monitoring, Logging, and Cost Estimating
Google has a service called Cloud Operations Suite, which provides monitoring, logging, and tracing.
- Create alerts based on resource metrics.
- Creating log sinks to store logging data.
- Viewing and filtering log data.
- Price Calculator for estimating costs.

## Cloud Monitoring
This is a service for collecting performance metrics, logs, and event data from cloud resources.
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
