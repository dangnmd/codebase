#!/bin/bash
#put this script in the directory which include zip archive

#PROJECT_NAME="payment_api"
#ENV="test_env"
#HOST_PORT="8008"
#IMAGE="registry.billbros.vn/cooky_python"
#NUM_WORKERS=3
#API_URL_VAR="TEST_SERVICE_API_URL"

# get environment variables
if [ -f .env ]
then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi
#

## run from data/source/{app}
DIR=`dirname $0`

PROJECT="${PROJECT_NAME}_${HOST_PORT}"
WORK_DIR="/data/release"
ZIP_PROJECT="${PROJECT_NAME}_${HOST_PORT}_${ENV}"
API_URL_VAL="http:\/\/127.0.0.1:${HOST_PORT}"
BACKUP_DIR=$WORK_DIR/backup/${PROJECT_NAME}_${HOST_PORT}-`date +%Y%m%d_%H%M%S`
CURRENT_DIR=$WORK_DIR/${PROJECT_NAME}_${HOST_PORT}/current
CURRENT_LOG_DIR=$WORK_DIR/${PROJECT_NAME}_${HOST_PORT}/current/${PROJECT_NAME}/log
PROJECT_DIR=$WORK_DIR/${PROJECT_NAME}_${HOST_PORT}
UNZIP_DIR=$DIR/$ZIP_PROJECT

if [ ! -d $BACKUP_DIR ]
then
        echo "Create $BACKUP_DIR"
        mkdir $BACKUP_DIR
fi

if [ ! -d $CURRENT_DIR ]
then
        echo "create $CURRENT_DIR"
        mkdir -p $CURRENT_DIR
fi

if [ ! -f $DIR/$ZIP_PROJECT.zip ]
then
        echo "Archive $DIR/$ZIP_PROJECT.zip doesn't exist, deploy failed!"
        exit
fi
if [ -f "$BACKUP_DIR" ]
then
        echo "Target directory $BACKUP_DIR exists, deploy failed!"
        exit
fi
rm -Rf $DIR/$ZIP_PROJECT
unzip -q $DIR/$ZIP_PROJECT.zip -d $DIR

## replace docker-compose.yaml, gunicorn_config.py

if [ -z "$IMAGE" ]
then
	IMAGE='registry.billbros.vn/cooky_python_api:python3_mssql'
fi

if [ -z "$NUM_WORKERS" ]
then
	NUM_WORKERS='multiprocessing.cpu_count() * 2 \+ 1'
fi


DOCKER_SERVICE="${ENV}-${PROJECT_NAME}-${HOST_PORT}"
DOCKER_CONTAINER="${ENV}_${PROJECT_NAME}_${HOST_PORT}"

rm -Rf $DIR/$ZIP_PROJECT
unzip -q $DIR/$ZIP_PROJECT.zip -d $DIR
echo $PWD

sed -i "s+\[HOST_PORT\]+${HOST_PORT}+g" $ZIP_PROJECT/common/deploy/*
sed -i "s+\[NUM_WORKERS\]+${NUM_WORKERS}+g" $ZIP_PROJECT/common/deploy/*
sed -i "s+\[DOCKER_SERVICE\]+${DOCKER_SERVICE}+g" $ZIP_PROJECT/common/deploy/*

cp -rf $ZIP_PROJECT/common/deploy/* $ZIP_PROJECT/
#

rsync -a $ZIP_PROJECT/. $BACKUP_DIR
# find $BACKUP_DIR/deploy/ -name "*.sh"|xargs dos2unix
# find $BACKUP_DIR/deploy/ -name "*.sh"|xargs chmod a+x
if [[ "$RUN_ENV" = "TEST" ]]
then
        sed -i "s/^TEST_ENV[ \t]*=[ \t]*.*/TEST_ENV = RunningEnvironment.TESTING/g" $BACKUP_DIR/*/test_common.py
elif [[ "$RUN_ENV" = "STAGING" ]]
then
        sed -i "s/^TEST_ENV[ \t]*=[ \t]*.*/TEST_ENV = RunningEnvironment.STAGING/g" $BACKUP_DIR/*/test_common.py
#        sed -i "s/^PROJECT[ \t]*=[ \t]*.*/PROJECT=\"$PROJECT\"/g" $BACKUP_DIR/deploy/config.sh
#        sed -i "s/^config.init_prometheus_data_dir(.*')/config.init_prometheus_data_dir('$PROJECT')/g" $BACKUP_DIR/*/settings.py
else
        sed -i "s/^TEST_ENV[ \t]*=[ \t]*.*/TEST_ENV = RunningEnvironment.PRODUCTION/g" $BACKUP_DIR/*/test_common.py
fi
if [ ! -z "$API_URL_VAR" ]
then
        sed -i "s/^${API_URL_VAR}[ \t]*=[ \t]*.*/${API_URL_VAR} = \"$API_URL_VAL\"/g" $BACKUP_DIR/test/test_constants.py
fi
rm -rf $CURRENT_DIR/*
rsync -a $BACKUP_DIR/. $CURRENT_DIR

ln -sft $PROJECT_DIR $CURRENT_LOG_DIR

if [ ! -f ${CURRENT_DIR}/deploy.sh ]
then
        echo "Archive ${CURRENT_DIR}/deploy.sh doesn't exist, deploy failed!"
        exit
fi

cd ${CURRENT_DIR} || exit

COMPOSE_FILE='docker-compose.yml'
if [[ "$CRON_JOB" = "TRUE" ]]
then
  COMPOSE_FILE='cron-docker-compose.yml'
fi

docker-compose -f ${COMPOSE_FILE} -p ${DOCKER_CONTAINER} down
sleep 3
rm -rf *.pyc
docker-compose -f ${COMPOSE_FILE} pull
docker-compose -f ${COMPOSE_FILE} -p ${DOCKER_CONTAINER} up -d
#--build
sleep 5

if [[ "$CRON_JOB" = "TRUE" ]]
then
    sudo docker exec -t -w /opt/project/${PROJECT_NAME} "${DOCKER_CONTAINER}"  cat cron_serviced.pid
else
    sudo docker exec -t -w /opt/project "${DOCKER_CONTAINER}" python -m test.${PROJECT_NAME}_test
fi

