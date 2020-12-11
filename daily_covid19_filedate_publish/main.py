import base64
import json
import os

from datetime import datetime, timedelta
from google.cloud import pubsub_v1

project_id = os.environ.get('covid19_project_id')
topic_name = os.environ.get('covid19_filedate_topic')

def filedate_event(filedate):
    event_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    event = {
        'eventType': 'abar-gcp-covid19-dataingestion',
        'eventId': 'abar-gcp-covid19-filedate',
        'eventTimestamp': event_timestamp,
        'data': {'covid19_filedate': filedate},
        }

    return event

# Publishes the filedate event to a Cloud Pub/Sub topic.
def publish_filedate_event(request):
    
    # date - 2 to account for delay in availability of data set in john hopkins github
    filedate = (datetime.now() - timedelta(2)).strftime("%m-%d-%Y")
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