---
sidebar_position: 1
title: Start monitoring your data
---

### We will accomplish the following in this tutorial:

1. Setup with Docker Compose
2. Connect to a datasource
3. Create a dataset to monitor
4. Generate expectations
5. Validate our dataset


### 1. Clone Swiple GitHub Repository 
Clone [Swiple GitHub Repository](https://github.com/Swiple/swiple.git) in your terminal with the following command:

```bash
git clone https://github.com/Swiple/swiple.git
# or
git clone git@github.com:Swiple/swiple.git
```
Once the command completes successfully, you should see a new `swiple` folder in your current directory, navigate to it.

```bash
cd swiple
```

### 2. Launch Swiple with Docker Compose

When working on the `main` branch, run the following commands:

```bash
docker compose -f docker-compose-non-dev.yaml pull
docker compose -f docker-compose-non-dev.yaml up
```
This will start the following services:
1. Swiple API
2. Swiple UI
3. Swiple Scheduler
4. Swiple Setup
5. OpenSearch Cluster
6. PostgreSQL (Sample Data)
7. Redis

You should start to see a wall of logging output from the containers being launched on your machine. Once the output slows, you can navigate to [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login) to see the app running.

### 3. Sign in to Swiple at [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)

![](/img/login.png)

### 4. Connect to Sample Database

Included in the running services will be a PostgreSQL database with sample data. You can use this data to give Swiple a test run.

**4.1.** Click `Data Sources` in the sidebar followed by the `+ Data Source` button.
![](/img/datasources-create-datasource.png)

**4.2.** Fill in the details of the datasource as shown below then click `Create`

![](/img/fill-in-and-create-datasource.png)

You should see your new datasource in the table of data sources! 👏 😎

![](/img/datasource-list.png)

### 5. Create a Dataset

**5.1.** Click `Datasets` in the sidebar followed by the `+ Dataset` button.
![](/img/datasets-and-create-dataset.png)

**5.2.** Fill in the details of the data as shown below then click `Create`

![](/img/fill-in-query-dataset-and-create-dataset.png)

You should see your new dataset in the table of dataset! 👏 😎


### 6. Generate and Add Expectations

**6.1.** Click on **"v_orders"** to navigate to the dataset view.
![](/img/dataset-list.png)

**6.2.** Click on the **"Suggestions"** tab, then click on **"Generate Suggestions"**.
![](/img/suggestions-tab-generate.png)

The dataset you have selected will be analyzed and expectations will be suggested.

**6.3.** Once a list of suggestions appear, enable the first 4 suggestions. 
![](/img/suggestions-enable.png)




### 7. Validate Data
**7.1.** Navigate to the **"Expectations"** tab, then click **"Run Expectations"**.
![](/img/expectations-tab-and-run.png)

At this point, you should see the list of expectations you enabled, whether they passed or failed validation, the history of all validation runs, and the documentation for each expectation! 👏 😎

#### Good next steps:
1. [How to schedule validations](../how-to-guides/scheduling-validations)
2. [How to get alerts/notifications](../how-to-guides/actions)