# mlops-final

# Setup 

Preapared to run on uvbuntu 22.04 environment

## Install pyenv

```bash
# setup dependencies
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev \
        libxmlsec1-dev libffi-dev liblzma-dev docker-compose docker.io
# Install pyenv
curl -fsSL https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc

source ~/.bashrc
# Install pyenv for local testing
pyenv install 3.12
```

## Build base images
Dagster build use a base image, so it needs to be built before the rest of the service

```bash
docker-compose build dagster-base-image
docker-compose build 
```

## Airbyte

Install airbyte

```bash
# Install abctl
curl -LsfS https://get.airbyte.com | bash

# Disable credentials 
# Run instalation
abctl local install --values=./airbyte/values.yml
rm values.yml
```

## .env file

Store secrets in local `.env` file

```bash
# Same user for postgres db asset and dagster internal DB
POSTGRES_USER=auser
POSTGRES_PASSWORD=some_password
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=another_password
# The IP address of the host where airbyte is running
# You cannot use localhost.
AIRBYTE_HOST=10.10.10.10
```

# Run 

## Airbyte 

The installation keep Airbyte running

## Rest of components

Run docker compose to build all the components

```bash
docker-compose up -d
docker-compose logs -f 
```

## Test DBT
Once that dbt is running you can run dbt using docker exec

```bash
docker-compose exec -w /code/films_preparation dbt dbt run --full-refresh  
```