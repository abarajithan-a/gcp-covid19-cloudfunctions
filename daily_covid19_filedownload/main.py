import os
import wget
import base64
import json

from google.cloud import storage

url = os.environ.get('covid19_dataset_url')
bucket_name = os.environ.get('covid19_dataset_bucket')

def file_download(event, context):
	
	message = json.loads(str(base64.b64decode(event['data']).decode('utf-8')))

	file_name = message['data']['covid19_filedate'] + ".csv"

	temp_file_path = '/tmp/{}'.format(file_name)

	# set storage client
	client = storage.Client()

	# get bucket
	bucket = client.get_bucket(bucket_name)

	# download the file to Cloud Function's tmp directory
	wget.download(url + file_name, out=temp_file_path)

	print("COVID19 Daily Data File " + file_name + " downloaded successfully!")

	# set Blob
	blob = storage.Blob(file_name, bucket)
 
	# upload the file to GCS
	blob.upload_from_filename(temp_file_path)

	print("COVID19 Daily Data File " + file_name + " saved successfully in cloud storage bucket!")