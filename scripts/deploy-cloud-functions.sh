#! /bin/bash
CF_NAME=$1
CF_ARG_LIST=$2

CF_DEPLOY_CMD="gcloud functions deploy $CF_NAME $CF_ARG_LIST"

exec $CF_DEPLOY_CMD

CF_NAME=$1
CF_ARG_LIST=$2

deploy_cmd="gcloud functions deploy $CF_NAME $CF_ARG_LIST"

gcloud functions \
  deploy daily_covid19_filedownload \
  --source=${SOURCE_DIR} \
  --region=us-east1 \
  --entry-point file_download \
  --env-vars-file ../env.prod.yaml \
  --runtime python37 \
  --memory=256MB \
  --timeout=300s \
  --trigger-topic abar-ps-topic-covid19-filedate \
  --allow-unauthenticated