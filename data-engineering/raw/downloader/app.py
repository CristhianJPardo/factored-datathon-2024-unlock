import os
import requests
import boto3

s3_client = boto3.client('s3')
RAW_DATA_BUCKET_NAME = os.getenv("RAW_DATA_BUCKET_NAME")

def lambda_handler(event, context):
    file_name = event['file_name']
    type = event['type']
    url = f"http://data.gdeltproject.org/{type}/{file_name}"
    key = f"{type}/{file_name}"
    s3_uri = f"s3://{RAW_DATA_BUCKET_NAME}/{key}"
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
    
    return {
        "statusCode": 200,
        "url": url,
        "s3_uri": s3_uri
    }
