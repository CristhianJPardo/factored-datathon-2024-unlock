import boto3
import json

s3_client = boto3.client('s3')
bucket = "factored-hackaton-2024-unlock-medallion-bucket"
folder_name = "catalog=factored_hackaton_2024/schema=gold"


def get_data_from_datalake_by_key(bucket, key):

    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        return data
    except s3_client.exceptions.NoSuchKey:
        print(f"No se encontró la clave: {key} en el bucket: {bucket}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al obtener el objeto de S3: {str(e)}")
        return None


def get_data_from_datalake_by_id(id: str):
    key = f"{folder_name}/{id}"
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        return data
    except s3_client.exceptions.NoSuchKey:
        print(f"No se encontró la clave: {key} en el bucket: {bucket}")
        return None
    except Exception as e:
        print(f"Ocurrió un error al obtener el objeto de S3: {str(e)}")
        return None


def list_data_from_folder_name_and_return_json_content(folder_name):
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_name)
    json_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.json')]
    
    if not json_files:
        return {
            'statusCode': 404,
            'body': json.dumps('No JSON files found in the specified folder.')
        }
    
    first_json_key = json_files[0]
    json_content = s3_client.get_object(Bucket=bucket, Key=first_json_key)['Body'].read().decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': json_content
    }


def get_folder_name_from_id(id):
    folder_name = f"{folder_name}/{id}"
    return folder_name
