# deanonymize

![Python application](https://github.com/beedata-analytics/deanonymize/workflows/Python%20application/badge.svg)

Deanonymize html files and convert them to pdf.

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
$ python3 src/run.py
  --report reports/00001~202009.html
  --data data/sample.csv
  --layout layout/portrait.json
  --output pdf
  --batch-month 202010
  --batch-number 1
  --delimiter ','
  --processes 16
  --id id

```

All html reports on a directory:

```sh
$ python3 src/run.py
  --report reports
  --data data/sample.csv
  --layout layout/portrait.json
  --output pdf
  --batch-month 202010
  --batch-number 1
  --delimiter ','
  --processes 16
  --id id
```
