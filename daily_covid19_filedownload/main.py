import os
import wget
import base64
import json
import pandas
import re
from datetime import datetime

from google.cloud import storage

url = os.environ.get('covid19_dataset_url')
bucket_name = os.environ.get('covid19_dataset_bucket')

def add_columns(file_path):

	with open(file_path) as inputcsvfile:
		df = pandas.read_csv(inputcsvfile, delimiter=',')

	# Add Incidence rate column if it doesnt exist in the file
	if not any(re.search(".*inciden.*rate.*", col.lower()) for col in df.columns):
		df['incident_rate'] = ''

	# Add case fatality ratio column if it doesnt exist in the file
	if not any(re.search(".*case.*fatal.*ratio.*", col.lower()) for col in df.columns):
		df['case_fatality_ratio'] = ''

	df['ingestion_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	df['file_name'] = file_path.strip('/tmp/')

	return df

def file_download(event, context):
	
	message = json.loads(str(base64.b64decode(event['data']).decode('utf-8')))

	file_name = message['data']['covid19_filedate'] + '.csv'
	temp_file_path = '/tmp/{}'.format(file_name)

	# download the file to Cloud Function's tmp directory
	wget.download(url + file_name, out=temp_file_path)
	print('COVID19 Daily Data File ' + file_name + ' downloaded successfully!')

	# Add the etl metadata columns
	df = add_columns(temp_file_path)
	df.to_csv(temp_file_path, index=False)

	# set storage client
	client = storage.Client()
	# get bucket
	bucket = client.get_bucket(bucket_name)
	# set Blob
	blob = storage.Blob(file_name, bucket)
	# upload the file to GCS
	blob.upload_from_filename(temp_file_path)

	print('COVID19 Daily Data File ' + file_name + ' saved successfully in cloud storage bucket!')