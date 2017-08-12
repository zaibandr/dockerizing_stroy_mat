FROM python:3.5

RUN apt update && apt install -y libgeos-dev
RUN apt-get install -y libgdal-dev libgdal1h

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /usr/src/app