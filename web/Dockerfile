FROM python:3.5

ARG DEBIAN_FRONTEND=noninteractive
RUN mkdir -p /usr/src/app
RUN apt-get update && apt-get install -y libgeos-dev
WORKDIR /usr/src/app

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /usr/src/app

