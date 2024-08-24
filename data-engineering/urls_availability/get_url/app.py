import boto3
import os
import json

sqs = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        body = json.loads(message['Body'])
        body["receipt_handle"] = receipt_handle
        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'No messages available in the queue'})
        }
