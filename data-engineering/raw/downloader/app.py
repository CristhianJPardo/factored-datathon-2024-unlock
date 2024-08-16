import os
import requests
import boto3
from datetime import datetime, timedelta, timezone

s3_client = boto3.client('s3')
RAW_DATA_BUCKET_NAME = os.getenv("RAW_DATA_BUCKET_NAME")


def get_file_names(formatted_date, event):
    type = event['type']
    if type == 'events':
        file_names_default = [
            f"{formatted_date}.export.CSV.zip"
        ]

    elif type == 'gkg':
        file_names_default = [
            f"{formatted_date}.gkg.csv.zip",
            f"{formatted_date}.gkgcounts.csv.zip"
        ]

    else:
        file_names_default = []

    return file_names_default


def get_formatted_date():
    utc_time = datetime.now(timezone.utc)
    est_time = utc_time.astimezone(timezone(timedelta(hours=-5)))  
    
    previous_day = est_time - timedelta(days=1)    
    formatted_date = previous_day.strftime('%Y%m%d')
    return formatted_date


def download_upload_file(url, key, file_name):
    try:
        response = requests.get(url)
        try:
            s3_client.put_object(
                Bucket=RAW_DATA_BUCKET_NAME,
                Key=key,
                Body=response.content
            )
            print("Successfully uploaded!")
            
        except Exception as e:
            print(f"Failed, error: {e}")
    except Exception as e:
        print(f"Failed to download {file_name} from {url}, error: {e}")


def download_upload_files(file_names):
    for file_name in file_names:
        url = f"http://data.gdeltproject.org/{type}/{file_name}"
        key = f"{type}/{file_name}"
        s3_uri = f"s3://{RAW_DATA_BUCKET_NAME}/{key}"        
        download_upload_file(url, key, file_name)


def lambda_handler(event, context):
    
    formatted_date = get_formatted_date()
    file_names = get_file_names(formatted_date, event)
    download_upload_files(file_names)
    
    return {
        "statusCode": 200
    }
