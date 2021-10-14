FROM ubuntu:16.04

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

# Install dependencies
RUN apt-get install -y build-essential xorg libxrender-dev wget
RUN apt-get update && apt-get install -y --no-install-recommends xvfb libfontconfig fontconfig libjpeg-turbo8 xfonts-75dpi

# Download and install wkhtmltopdf
RUN wget --no-check-certificate https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.xenial_amd64.deb
RUN dpkg -i --force-depends wkhtmltox_0.12.6-1*.deb
RUN ln -s /usr/local/bin/wkhtml* /usr/bin
RUN rm wkhtmltox_0.12.6-1.*.deb

# Install required libraries

COPY . /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run bash

CMD ["/bin/bash"]
