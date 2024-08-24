import boto3
import os
import json

sqs = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']


def lambda_handler(event, context):
    batch_size = event.get('queryStringParameters', {}).get('batch_size', 1)
    batch_size = int(batch_size)
    batch_size = min(batch_size, 10)
    
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=batch_size,
        WaitTimeSeconds=10
    )
    
    if 'Messages' in response:
        messages = []
        for message in response['Messages']:
            receipt_handle = message['ReceiptHandle']
            body = json.loads(message['Body'])
            body["receipt_handle"] = receipt_handle
            messages.append(body)
        
        return {
            'statusCode': 200,
            'body': json.dumps(messages)
        }    
    else:
        body = json.dumps({'message': 'No messages available in the queue'})
        return {
            'statusCode': 404,
            'body': body
        }
