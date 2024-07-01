#!/usr/bin/env bash

cd "$(dirname "$0")"

docker build -t stream-model-duration:v2 .


pipenv run python test_docker.py