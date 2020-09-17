# deanonymize

Deanonimize html files and convert them to pdf.

A Docker image with all software, libraries and configuration needed is provided.

## Install Docker

1. [Install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)

## Run Docker image

```sh
$ sudo docker-compose run deanonymize
```

## Deanonymize and generate pdf

### Usage

One single report:

```sh
$ python3 src/run.py --report reports/12005~202007.html --data data/sample.csv --layout layout/landscape.json --output pdf
```

All html reports on a directory:

```sh
$ python3 src/run.py --report reports --data data/sample.csv --layout layout/landscape.json --output pdf
```
