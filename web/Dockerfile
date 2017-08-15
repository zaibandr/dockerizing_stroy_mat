FROM python:3.5

RUN apt update && apt install -y libgeos-dev
RUN apt install -y libgdal-dev libgdal1h
RUN apt install nano

RUN mkdir -p /usr/src/web
WORKDIR /usr/src/web

ADD __init__.py /usr/src/
ADD requirements.txt /usr/src/web/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /usr/src/web