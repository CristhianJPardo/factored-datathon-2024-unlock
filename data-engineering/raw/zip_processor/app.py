import boto3
import os
import zipfile
import io

s3_client = boto3.client('s3')
UNZIPPED_BUCKET_NAME = os.environ['UNZIPPED_BUCKET_NAME']

def lambda_handler(event, context):
    print(event)
    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    zip_key = event['Records'][0]['s3']['object']['key']
    folder = zip_key.split("/")[0]
    
    zip_obj = s3_client.get_object(Bucket=raw_bucket, Key=zip_key)
    buffer = io.BytesIO(zip_obj["Body"].read())
    
    with zipfile.ZipFile(buffer, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            extracted_file = zip_ref.open(file_name)
            s3_client.upload_fileobj(
                extracted_file,
                UNZIPPED_BUCKET_NAME,
                f"{folder}/{file_name}"
            )
    
    return {
        'statusCode': 200,
        'body': f'Successfully extracted and uploaded files'
    }
