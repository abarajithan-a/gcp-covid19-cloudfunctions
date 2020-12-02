#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_FILEDOWNLOAD="${DIR}/../daily_covid19_filedownload/main.py"

source "${DIR}/.env.local"

functions-framework \
  --source=${SOURCE_FILEDOWNLOAD} \
  --target=${FN_NAME_FILEDOWNLOAD} \
  --signature-type=event \
  --port=${FN_PORT_PUBSUB_FILEDOWNLOAD} \
  --debug