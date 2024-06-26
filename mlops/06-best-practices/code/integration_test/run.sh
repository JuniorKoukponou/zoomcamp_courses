#!/usr/bin/env bash


cd "$(dirname "$0")"

# LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`

# export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} .
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi


export PREDICTION_STREAM_NAME="ride_predictions"

docker build -t ${LOCAL_IMAGE_NAME} ..

docker-compose up -d

sleep 2

aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ${PREDICTION_STREAM_NAME} \
    --shard-count 1

pipenv run python test_kinesis.py


ERROR_CODE=$?

if [ ${ERROR_CODE}  != 0]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down
