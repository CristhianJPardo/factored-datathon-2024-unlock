import boto3

s3_client = boto3.client('s3')

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
    bucket = "factored-hackaton-2024-unlock-medallion-bucket"
    key = f"catalog=factored_hackaton_2024/schema=gold/{id}"
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