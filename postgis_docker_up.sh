#!/usr/bin/env bash
docker run --name has_app_postgis -e POSTGRES_PASSWORD=haspswd -e POSTGRES_DB=has_app_db -e POSTGRES_USER=has_app -p 5445:5445 -d mdillon/postgis