---
sidebar_position: 2
---

# Start Developing Locally


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

### 3. Install `make`

`make` allows us to bundle multiple commands into one making development easier.

**Mac OSX**

If you don't have Homebrew, [follow the steps on their homepage](https://brew.sh/).

Install `make` on Mac with Homebrew:
```bash
brew install make
```


**Windows**

If you don't have Chocolatey, [follow the steps here](https://chocolatey.org/install#individual).

Install `make` on Windows with Chocolatey:
```bash
choco install make
```


### 4. Setup Python Virtual Environment

:::note Note
Swiple has only been tested using **Python 3.9**.

If you are running on **Apple Silicon** run:
```bash
brew install postgresql
```
:::
### Install Poetry

Follow Poetry's `Installation` instructions [here](https://python-poetry.org/docs/#installation).

```bash
# Create virtualenv in project
poetry config virtualenvs.in-project true
```

### Install Dependencies
```bash
cd backend
poetry install --with postgres,redshift,mysql,trino,athena,snowflake,aws-secrets,gcp,azure-secrets,dev
cd ..
```

### 5. Setup Swiple UI

If you don't have Node, [follow the steps here](https://nodejs.org/en/download/).

**Mac OSX**
```bash
npm install --prefix ./frontend/
```

**Windows**
```bash
cd frontend
npm install
cd ..
```


### 6. Run Docker Containers

Run docker containers. Changes made to code will trigger a reload.

```bash
make
```

Running `make` does the following for you:
1. Builds the Docker Images for `swiple-api` and `swiple-ui`.
2. Runs `docker-compose up`, starting all services needed to run Swiple.

Changes made to code will trigger a reload of the API or UI.


### 7. Sign in to Swiple at [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)
![](/img/login.png)

Nice work! 👏 😎

:::note Note
`ADMIN_EMAIL` and `ADMIN_PASSWORD` can be set in `docker/.env`

To avoid authentication issues during local development, `AUTH_COOKIE_SECURE` is set to `False` in your `docker/.env`.
:::

<br/>

### Good next step:
1. [Tutorials > Start monitoring your data](../tutorials/start-monitoring-your-data)

