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

:::note Note
`ADMIN_EMAIL` and `ADMIN_PASSWORD` can be set in `./backend/app/config/config.py` 
:::

### 5. Connect to Sample Database

Included in the running services will be a PostgreSQL database with sample data. You can use this data to give Swiple a test run.

**5.1.** After signing in, click `Data Sources` in the sidebar followed by the `+ Data Source` icon in the top right of the page.

**5.2.** Provide a name and description for the data source, then select PostgreSQL from the Engine dropdown.

Lastly, fill in the following credentials:
- **username:** postgres
- **password:** postgres
- **host:** postgres
- **port:** 5432

You are now ready to add a dataset! 👏 😎