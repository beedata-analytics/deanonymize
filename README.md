# deanonymize

## Docker

A Docker image with all software, libraries and configuration needed is provided. To build the Docker image run

```sh
$ sudo docker-compose build deanonymize
```

Then run the Docker image.

```sh
$ sudo docker-compose run deanonymize
```

## Deanonymize and generate pdf

### Usage

One single report:

```sh
$ python src/run.py --report reports/697~201905.html --data data/sample.csv --layout layout/landscape.json --output pdf
```

All html reports on a directory:

```sh
$ python src/run.py --report reports --data data/sample.csv --layout layout/landscape.json --output pdf
```
