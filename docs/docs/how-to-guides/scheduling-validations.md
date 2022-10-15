---
sidebar_position: 1
title: How to schedule validations
---
Schedules allow you to run data validations on a specific date or at certain time intervals. You can create a schedule by using one of the schedule types. `Date`, `Interval` or `Cron`.

### When to use which schedule type?

#### Date
The date schedule type should be used to validate data once on a specific date and time. For example, `2022-10-01 8:00:00`

#### Interval
The interval schedule type should be used to validate data on some fixed period of time. For example, every 15 minutes, every 6 hours, every week.

#### Cron
Cron offers detailed schedule control. For example, run Monday - Friday at 8am or run every 2 hours Monday - Friday between 8am and 5pm.

### Steps to create a schedule
1. Navigate to the datasets tab
![](/img/creating_a_schedule/navigate-to-datasets.png)

2. Click the dataset you would like to create a schedule for
![](/img/creating_a_schedule/select-dataset.png)

3. Click the `Schedules` tab and then click `+ Schedule` button 
![](/img/creating_a_schedule/select-schedules-tab.png)

4. Select the schedule type and fill in the details of the schedule
![](/img/creating_a_schedule/fill-in-schedule.png)

5. Before clicking `Create`, review the `Next 10 trigger dates` to confirm that the schedule will run when you expect it to run.
![](/img/creating_a_schedule/note-next-runs.png)

6. You should see your new schedule 🎉
![](/img/creating_a_schedule/schedule-list.png)


:::caution Caution
When running the scheduler API, there can only ever by one instance of the API. If there is more than one instance, duplicate schedules will be created.
:::