---
sidebar_position: 1
---

# Run Locally With Docker Compose

The fastest way to try Swiple locally is using Docker and Docker Compose.

### 1. Install Docker Engine and Docker Compose
**Mac OSX**

[Install Docker for Mac](https://docs.docker.com/desktop/mac/install/), and follow steps.


**Window**

[Install Docker for Windows](https://docs.docker.com/desktop/windows/install/), and follow steps.

### 2. Clone Swiple's Github Repository 
Clone [Swiple's repo](https://github.com/Swiple/swiple.git) in your terminal with the following command:

```bash
git clone https://github.com/Swiple/swiple.git
```
Once the command completes successfully, you should see a new `swiple` folder in your current directory, navigate to it.

```bash
cd swiple
```

### 3. Set `ADMIN_EMAIL` and `ADMIN_PASSWORD`

The user/password authentication method is used by default but it cannot be integrated with your organization's current auth system. For production use cases, it is recommended to use OAuth. 

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `./backend/app/config/config.py`

```python
ADMIN_EMAIL = "email@something.com"
ADMIN_PASSWORD = "---Redacted---"
```

The admin user is created/updated in the `setup` docker container. Changing `ADMIN_EMAIL` will result in another admin user being created.

[See Authentication to use OAuth.](../configuration/authentication.md)

### 4. Generate and set `SECRET_KEY`

Run the following snippet to create a Fernet Key and set `SECRET_KEY` to it.
```python
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # your fernet_key, keep it in secured place!
```

:::note Note
At this time, changing `SECRET_KEY` after data sources have been added will cause connections to them to fail. Secret rotation is on the roadmap.
:::

### 5. Launch Swiple Through Docker Compose

When working on the `main` branch, run the following commands:

```bash
make
```
You should start to see a wall of logging output from the containers being launched on your machine. Once the output slows, you can navigate to [https://127.0.0.1:3000/login](https://127.0.0.1:3000/login) to see the app running.

Running `make` does the following for you:
1. Build the Docker Images for `swiple-api` and `swiple-ui`.
2. Run `docker-compose up`, starting all services needed to run Swiple.

<br/>

:::note Note
This will bring up Swiple in a non-dev mode, changes to the codebase will only be reflected by stopping the containers and re-running `make`.
:::


### 6. Sign in to Swiple at [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)
Sign in using the `ADMIN_EMAIL` and `ADMIN_PASSWORD` you provided in **step 3**.

:::note Note
Please do not open Swiple on `localhost`. You will encounter errors.
:::

### 7. Connect to Sample Database

Included in the running services will be a PostgreSQL database with sample data. You can use this data to give Swiple a test run.

**7.1.** After signing in, click `Data Sources` in the sidebar followed by the `+ Data Source` icon in the top right of the page.

**7.2.** Provide a name and description for the data source, then select PostgreSQL from the Engine dropdown.

Lastly, fill in the following credentials:
- **username:** postgres
- **password:** postgres
- **host:** postgres
- **port:** 5432

You are now ready to add a dataset! 👏 😎