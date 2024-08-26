import os
import requests
import boto3
import json
from datetime import datetime, timedelta, timezone
from aws_lambda_powertools.utilities.parser import parse, EventBridgeModel, LambdaUrlModel

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

    file_names = event.get("file_names", file_names_default)
    return file_names


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


def download_upload_files(file_names, type):
    for file_name in file_names:
        url = f"http://data.gdeltproject.org/{type}/{file_name}"
        key = f"{type}/{file_name}"
        s3_uri = f"s3://{RAW_DATA_BUCKET_NAME}/{key}"        
        download_upload_file(url, key, file_name)


def lambda_handler(event, context):
    try:
        if 'source' in event and 'detail' in event:
            # Es un evento de EventBridge
            parsed_event = parse(event, EventBridgeModel)
            handle_eventbridge_event(parsed_event)
        elif 'requestContext' in event:
            # Es un evento de Lambda Function URL
            parsed_event = parse(event, LambdaUrlModel)
            custom_event = parsed_event.body  # Accede al evento custom
            handle_lambda_url_event(custom_event)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    print(event)
    type = event['type']
    formatted_date = get_formatted_date()
    file_names = get_file_names(formatted_date, event)
    # print(file_names)
    download_upload_files(file_names, type)
    
    return {
        "statusCode": 200
    }

def handle_eventbridge_event(event):
    # Lógica para manejar eventos de EventBridge
    print("Manejando evento de EventBridge:", event)

def handle_lambda_url_event(event):
    # Lógica para manejar eventos de Lambda URL
    print("Manejando evento de Lambda URL:", event)