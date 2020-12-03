#! /bin/bash
CF_NAME=$1
CF_ARG_LIST=$2

CF_DEPLOY_CMD="gcloud functions deploy $CF_NAME $CF_ARG_LIST"

exec $CF_DEPLOY_CMD