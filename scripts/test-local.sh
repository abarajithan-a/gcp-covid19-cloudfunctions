#! /bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}/.env.local"

TEST_EVENT_PATH=$1

EVENT_PAYLOAD=$(cat ${TEST_EVENT_PATH})

curl -X POST \
  -H'Content-type: application/json' \
  -d "${EVENT_PAYLOAD}" \
  "http://localhost:${FN_PORT_PUBSUB_FILEDOWNLOAD}"

echo