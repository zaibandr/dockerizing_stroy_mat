#!/usr/bin/env bash
#git pull https://github.com/zaibandr/dockerizing_stroy_mat
docker-compose down
#docker volume rm webdata_app
docker-compose build
docker-compose up -d
docker exec -it dockerizingstroymat_web_1 bash
#apt update && apt install -y libgeos-dev