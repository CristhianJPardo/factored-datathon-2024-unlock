import os
import requests
import boto3
import json
from datetime import datetime, timedelta, timezone

s3_client = boto3.client('s3')
RAW_DATA_BUCKET_NAME = os.getenv("RAW_DATA_BUCKET_NAME")

def get_file_names(formatted_date, event_type, event):
    if 'file_names' in event:
        return event['file_names']
    
    if event_type == 'events':
        return [f"{formatted_date}.export.CSV.zip"]
    elif event_type == 'gkg':
        return [
            f"{formatted_date}.gkg.csv.zip",
            f"{formatted_date}.gkgcounts.csv.zip"
        ]
    else:
        return []

def get_formatted_date():
    utc_time = datetime.now(timezone.utc)
    est_time = utc_time.astimezone(timezone(timedelta(hours=-5)))
    previous_day = est_time - timedelta(days=1)
    formatted_date = previous_day.strftime('%Y%m%d')
    return formatted_date

def download_upload_file(url, key, file_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa
        s3_client.put_object(
            Bucket=RAW_DATA_BUCKET_NAME,
            Key=key,
            Body=response.content
        )
        print(f"Successfully uploaded {file_name}!")
    except requests.RequestException as req_err:
        print(f"Failed to download {file_name} from {url}, error: {req_err}")
    except Exception as e:
        print(f"Failed to upload {file_name} to S3, error: {e}")

def download_upload_files(file_names, event_type):
    for file_name in file_names:
        url = f"http://data.gdeltproject.org/{event_type}/{file_name}"
        key = f"{event_type}/{file_name}"
        download_upload_file(url, key, file_name)

def lambda_handler(event, context):
    try:
        if 'source' in event and 'detail' in event:
            # Es un evento de EventBridge
            event_type = event['detail'].get('type')
        else:
            # Es el evento por defecto
            event_type = event.get('type')
        
        if not event_type:
            raise ValueError("El evento no contiene un tipo ('type')")

        formatted_date = get_formatted_date()
        file_names = get_file_names(formatted_date, event_type, event)
        download_upload_files(file_names, event_type)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
