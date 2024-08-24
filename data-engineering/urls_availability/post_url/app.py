import boto3
import os
import json

sqs = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    body = json.loads(event['body'])

    # We expect the body to be a list of dictionaries, each with a
    # receipt_handle
    for message in body:
        receipt_handle = message['receipt_handle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Messages deleted successfully'})
    }
