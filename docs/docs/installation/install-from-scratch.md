---
sidebar_position: 2
---

# Install From Scratch


## 1. Setup Docker Engine and Docker Compose

Complete steps 1 & 2 of [Running Locally With Docker](../../docs/installation/run-locally-with-docker) guide.

## 2. Install `make`

`make` allows us to bundle multiple commands into one making development easier.

**Mac OSX**

If you don't have Homebrew, [follow the steps on their homepage](https://brew.sh/).

Install `make` on Mac with Homebrew:
```bash
brew install make
```


**Window**




## 3. Setup Python Virtual Environment

:::note Note
Swiple has only been tested using **Python 3.9**. If you do not have Python virtual environments setup, please follow [Setup with Anaconda](#setup-with-anaconda)
:::

### Setup with Anaconda ###

I use Anaconda to manage my Python versions. To use Anaconda too, follow [Anaconda's installation guide](https://docs.anaconda.com/anaconda/install/).

Once Anaconda is installed, run the following:

```bash
# Create Python 3.9 Environment named swiple
conda create --name swiple python=3.9 -y

# Activate Environment
conda activate swiple

# Install Python Dependencies
pip install -r ./backend/requirements.txt
```

### Setup with `virtualenv` ###


**Mac OSX**
```bash
# Create Virtual Environment
python3 -m venv ./backend/venv

# Activate `venv` Environment
source ./backend/venv/bin/activate

# Install Dependencies
pip install -r ./backend/requirements.txt
```

**Windows**
```bash
# Create Virtual Environment
python3 -m venv ./backend/venv

# Activate `venv` Environment
./backend/Scripts/activate.bat

# Install Dependencies
pip install -r ./backend/requirements.txt
```

## 4. Set `ADMIN_EMAIL` and `ADMIN_PASSWORD`

The user/password authentication method is used by default but it cannot be integrated with your organization's current auth system. For production use cases, it is recommended to use OAuth. 

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `./backend/app/config/config.py`

```python
ADMIN_EMAIL = "email@something.com"
ADMIN_PASSWORD = "---Redacted---"
```

The admin user is created/updated in the `setup` docker container. Changing `ADMIN_EMAIL` will result in another admin user being created.

[See Authentication to use OAuth.](../configuration/authentication.md)

## 5. Generate and set `SECRET_KEY`

Run the following snippet to create a Fernet Key and set `SECRET_KEY` to it.
```python
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # your fernet_key, keep it in secured place!
```

:::note Note
At this time, changing `SECRET_KEY` after data sources have been added will cause connections to them to fail. Secret rotation is on the roadmap.
:::


## 6. Setup Swiple UI
```bash
# Install Dependecies
npm install --prefix ./frontend/
```


## 7. Run Docker Containers

Run Opensearch, Opensearch Dashboards, Setup, and Postgres docker containers with the following:

```bash
make bundled_dev
```

## 8. Start Swiple API
Update `OPENSEARCH_HOST` in `./backend/app/config/config.py` from 

```python
OPENSEARCH_HOST = "opensearch-node1"
```
to
```python
OPENSEARCH_HOST = "localhost"
```

Start Swiple API.
```bash
python3 ./backend/main.py
```

## 9. Start Swiple UI

```bash
npm start --preifx ./frontend/
```

## 10. Navigate to [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)

:::note Note
Please do not open Swiple on `localhost`. You will encounter errors.
:::