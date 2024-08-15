import os
import time
import requests
import boto3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
# from botocore.exceptions import BotoCoreError, ClientError

# Retry setup for requests
retry_strategy = Retry(
    total=5,  # Total retries
    backoff_factor=1,  # Exponential backoff factor (1, 2, 4, 8, etc.)
    status_forcelist=[429, 500, 502, 503, 504],  # HTTP codes to retry
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Methods to retry
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)
http.mount("https://", adapter)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    file_name = event['file_name']
    type = event['type']

    url = f"http://data.gdeltproject.org/{type}/{file_name}"
    return {
        "statusCode": 200,
        "body": url
    }
