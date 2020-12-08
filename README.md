# gcp-covid19-cloudfunctions
Repository for COVID19 data engineering using Cloud Functions in Google Cloud Platform(GCP)

1. **daily_covid19_filedownload** - The trigger is Pub/Sub topic. This function reads the COVID19 filedate event from Pub/Sub topic, parses the file date from the message and then downloads the CSV file from John Hopkins "CSSEGISandData/COVID-19" GitHub repository. The downloaded file is then saved onto the Cloud Storage Bucket.

