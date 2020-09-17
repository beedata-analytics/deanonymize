FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

ENV PYTHONPATH=/app

RUN apt-get update \
	&& apt-get upgrade -y \
    && apt-get install -y \
    curl \
    gnupg \
	locales \
	locales-all \
	python3-pip

# Download and install wkhtmltopdf
RUN apt-get install -y build-essential xorg libssl1.0-dev libxrender-dev wget

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends xvfb libfontconfig

RUN wget --no-check-certificate https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar vxf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wk* /usr/local/bin/
RUN rm -rf wkhtmltox
RUN rm wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

# Install required libraries

COPY . /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Run bash

CMD ["/bin/bash"]
