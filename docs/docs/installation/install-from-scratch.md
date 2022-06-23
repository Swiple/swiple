---
sidebar_position: 2
---

# Install From Scratch


### 1. Setup Docker Engine and Docker Compose

Complete steps 1 & 2 of [Running Locally With Docker](../../docs/installation/run-locally-with-docker) guide.

### 2. Install `make`

`make` allows us to bundle multiple commands into one making development easier.

**Mac OSX**

If you don't have Homebrew, [follow the steps on their homepage](https://brew.sh/).

Install `make` on Mac with Homebrew:
```bash
brew install make
```


**Windows**




### 3. Setup Python Virtual Environment

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


### 4. Setup Swiple UI
```bash
# Install Dependecies
npm install --prefix ./frontend/
```


### 5. Run Docker Containers

Run docker containers. Changes made to code will trigger a reload.

```bash
make
```

Running `make` does the following for you:
1. Builds the Docker Images for `swiple-api` and `swiple-ui`.
2. Runs `docker-compose up`, starting all services needed to run Swiple.

:::note Note
Changes to `requirements.txt` and `node_modules will require stopping containers and re-running step 5.
:::


### 4. Sign in to Swiple at [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login)
Sign in with the following credentials:
- **Username**: admin@email.com
- **Password**: admin

:::note Note
`ADMIN_EMAIL` and `ADMIN_PASSWORD` can be set in `./backend/app/config/config.py` 
:::
