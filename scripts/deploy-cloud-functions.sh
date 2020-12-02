#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_DIR="${DIR}/../daily_covid19_filedownload"

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