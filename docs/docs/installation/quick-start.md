---
sidebar_position: 1
---

# Quickstart with Docker Compose

The fastest way to try Swiple locally is using Docker and Docker Compose.

### 1. Install Docker Engine and Docker Compose
**Mac OSX**

[Install Docker for Mac](https://docs.docker.com/desktop/mac/install/).


**Window**

[Install Docker for Windows](https://docs.docker.com/desktop/windows/install/).

### 2. Clone Swiple GitHub Repository 
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

### 3. Launch Swiple Through Docker Compose

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

:::note Note
This will bring up Swiple in a non-dev mode, changes to the codebase will not be reflected. If you would like to run Swiple in dev mode to test local changes, follow the steps in [Start Developing](./start-developing).
:::

### 4. Sign in to Swiple at [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)
Sign in with the following credentials:
- **Username**: admin@email.com
- **Password**: admin

:::info Important
Before deploying to production, make the following changes to `docker/.env-non-dev` 

1. Update `ADMIN_EMAIL` and `ADMIN_PASSWORD`.
2. Set `AUTH_COOKIE_SECURE` to `True`.
3. Generate a new `SECRET_KEY` as shown in [How to Update SECRET_KEY](../configuration/how-to-update-SECRET_KEY.md).  
:::

### 5. Connect to Sample Database

Included in the running services will be a PostgreSQL database with sample data. You can use this data to give Swiple a test run.

**5.1.** After signing in, click `Data Sources` in the sidebar followed by the `+ Data Source` icon in the top right of the page.

**5.2.** Provide a name and description for the data source, then select PostgreSQL from the Engine dropdown.

Fill in the following credentials:
- **username:** postgres
- **password:** postgres
- **database:** postgres
- **host:** postgres
- **port:** 5432

Lastly, click **"Create"** and you should see your new data source in the table of data sources! 👏 😎

### 6. Create a Dataset

**6.1.** Click **"Datasets"** in the left sidebar.

**6.2.** Click `+ Dataset` icon in the top right of the page.

**6.3.** From the **Data Source** dropdown, select the data source you created in step 5, **"postgres"**.

**6.4.** From the **Schema** dropdown, select the schema **"sample_data"**.

**6.5.**
#### Option 1: Table
1. From the **"Table"** dropdown select **"orders"** then click **"Create"**.

#### Option 2: Query
1. For **"Dataset Name"** input **"v_orders"**
2. For **"Query"** input:
```sql
select * from sample_data.orders
```
3. Click **"Create"**.

You should see your new dataset in the table of datasets! 👏 😎

### 7. Generate and Add Expectations

**7.1.** Click on **"orders"** or **"v_orders"** to navigate to the dataset view.

**7.2.** Click on the **"Suggestions"** tab, then click on **"Generate Suggestions"**.

The dataset you have selected will be analyzed and expectations will be suggested.

**7.3.** Once a list of suggestions appear, enable the suggestions you consider valuable by clicking **"Enable"**. 

** The following are a good starting point:**
* expect_table_row_count_to_be_between
* expect_table_columns_to_match_ordered_list
* expect_column_values_to_not_be_null
* expect_column_values_to_be_in_set

Navigate to the **"Expectations"** tab to see the enabled suggestions.

### 8. Validate Data
**8.1.** While on the **"Expectations"** tab, click **"Run Expectations"** to the right of the page.

At this point, you should see the list of expectations you enabled, whether they passed or failed validation, the history of all validation runs, and the documentation for each expectation! 👏 😎


