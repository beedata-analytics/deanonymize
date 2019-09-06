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

```sh
$ python src/run.py --report output/697~201905.html --data data/sample.csv --layout layout/landscape.json
```

output files `output/697~deanonymized~201905.html` and `output/697~deanonymized~201905.pdf` will be generated.