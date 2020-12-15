import base64
import json
import os

from datetime import datetime, timedelta
from google.cloud import pubsub_v1

project_id = os.environ.get('covid19_project_id')
topic_name = os.environ.get('covid19_filedate_topic')
replay_start_date = os.environ.get('covid19_replay_startdate')
replay_end_date = os.environ.get('covid19_replay_enddate')

def filedate_event(filedate):
    event_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    event = {
        'eventType': 'abar-gcp-covid19-dataingestion',
        'eventId': 'abar-gcp-covid19-filedate',
        'eventTimestamp': event_timestamp,
        'data': {'covid19_filedate': filedate},
        }

    return event

def publish_filedate_event(filedate):
    message = filedate_event(filedate)

    print('Publishing filedate event to topic ' + topic_name + ' ...')

    # Instantiates a Pub/Sub client
    publisher = pubsub_v1.PublisherClient()
    # References an existing topic
    topic_path = publisher.topic_path(project_id, topic_name)

    message_json = json.dumps(message)
    message_bytes = message_json.encode('utf-8')

    # Publishes the message
    publish_future = publisher.publish(topic_path, data=message_bytes)
    publish_future.result()  # Verify the publish succeeded
    print('filedate ' + filedate + ' event successfully published!')    

# Publishes the filedate event to a Cloud Pub/Sub topic.
def replay_filedates_event(request):
    start_date = datetime.strptime(replay_start_date, "%m-%d-%Y")

    if replay_end_date and replay_end_date.strip():
        end_date = datetime.strptime(replay_end_date, "%m-%d-%Y")
    else:
        end_date = datetime.strptime(replay_start_date, "%m-%d-%Y")
    
    delta = end_date - start_date # as timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        publish_filedate_event(day.strftime("%m-%d-%Y"))
