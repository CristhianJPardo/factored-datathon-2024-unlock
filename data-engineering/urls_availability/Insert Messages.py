# Databricks notebook source
import boto3
import json

# Configurar SQS y la URL de la cola
sqs = boto3.client(
    'sqs',
    region_name='us-east-1'
)
queue_url = 'https://sqs.us-east-1.amazonaws.com/738012852934/factored-hackaton-2024-unlock-url-queue'            

messages = []
for i in range(4, 10):
    msg =  {"id": f"{i}", "url": f"www.url{i}.com"}
    messages.append(msg)
    # JSON con los mensajes
    
# Enviar mensajes a la cola
for message in messages:
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message)
    )
    print(f"Message sent with ID: {response['MessageId']}")


# COMMAND ----------

messages

# COMMAND ----------

import requests

# URL del endpoint API Gateway para get_url
get_url_endpoint = 'https://nhe9he1426.execute-api.us-east-1.amazonaws.com/Prod/get_url/'

# Hacer una solicitud GET para obtener un mensaje de la cola
response = requests.get(get_url_endpoint)

# Imprimir la respuesta
if response.status_code == 200:
    print("Received message:", response.json())
else:
    print("Failed to retrieve message:", response.text)

# COMMAND ----------

import requests
import json

# URL del endpoint API Gateway para post_url
post_url_endpoint = 'https://nhe9he1426.execute-api.us-east-1.amazonaws.com/Prod/post_url/'

# Ejemplo de cuerpo que recibirías de la solicitud GET
received_message = {'id': '2', 'url': 'www.url2.com', 'receipt_handle': 'AQEB49Xgp59wsD3pDMJH1hbQ0wW4YRk/e2qKHZITppxTrT8XoCbdoE6IxkWlaiUuicx2ME0cYaXdgV0gUr3FelEqy4EUcnu+5cW7PEVzP3nWQI+1kyB0Mq8Nfi4LutXpeR1xcLNnDZPiZU+eHbV5D7yroj1XZ//9jEftJUURtLwg/23mgPc8YuOnDL/Ds3NdDh+4WFamxx2/Zw5LdUwRj7I02w/WXV63ScHkSTZOMPXu1v0VF0lXAafdDNz8WT6QDnvPxzhOlIBVz9fJ2C/95fWkwnEkpd4AS651QR6wT90uxD261CEvX/ev1YvU2OKSFwvIrLXbRFi7bT7xUM0lvp1/qMh3Qk971h7sQXH5T3HI2z/iZwZL+UHE8sRZkd9T6Rkd87sG2KwcgFoUZpgiuVu+Ra4Szx7eEaCu9SnCVCHbKi0='}

# Hacer una solicitud POST para eliminar el mensaje de la cola
response = requests.post(post_url_endpoint, data=json.dumps(received_message))

# Imprimir la respuesta
if response.status_code == 200:
    print("Message deleted:", response.json())
else:
    print("Failed to delete message:", response.text)

