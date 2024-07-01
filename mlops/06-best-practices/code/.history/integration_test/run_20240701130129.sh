#!/usr/bin/env bash

cd "$(dirname "$0")"

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

docker build -t ${LOCAL_IMAGE_NAME} ..

docker-compose up -d

sleep 2

pipenv run python test_docker.py

docker-compose down