---
title: How to get alerts/notifications
---

Alerts/notifications can be setup in two steps. First, you will create a `Destination` followed by an `Action`.

A `Destination` is where you would like to send the alert/notification to. For example, Email, OpsGenie, PagerDuty, Microsoft Teams, 
or Slack. The `Destination` is reusable and only contains the bare minimum information to send the alert/notification. 
![](/img/filled-destination-example.png)


An `Action` contains the event you would like get notified on such as `validation`, whether to trigger on `success`, `failure`, or `both`,
and additional `Destination` details such as `Priority` in the case of `OpsGenie`.
![](/img/filled-action-example.png)


To configure a `Destination` and `Action`, follow any of the guides below
* [OpsGenie](opsgenie)
* [Slack](slack)
* [PagerDuty](pagerduty)
* [Microsoft Teams](microsoft-teams)
* [Email](email)
