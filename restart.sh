#!/bin/bash

if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

if [ -z "$IMAGE" ]
then
	IMAGE='dnguyen99/ddocker:first'
fi

if [ -z "$NUM_WORKERS" ]
then
	NUM_WORKERS='multiprocessing.cpu_count() * 2 \+ 1'
fi

SERVICE_NAME=${PROJECT_NAME}_${HOST_PORT}

docker restart ${ENV}_${PROJECT_NAME}_${HOST_PORT}
