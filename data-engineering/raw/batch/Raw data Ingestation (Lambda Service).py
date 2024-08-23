# Databricks notebook source
from bs4 import BeautifulSoup
import requests
import datetime
import boto3
import tqdm
import re
import jmespath
import json

# COMMAND ----------

def fetch_html(url, type_):

    url = f"{url}/{type_}/index.html"
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Example usage

url = "http://data.gdeltproject.org"
type_ = "events"
html = fetch_html(url, type_)

# COMMAND ----------

print(html)

# COMMAND ----------

def extract_file_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li')

    result = []
    for item in items:
        a_tag = item.find('a')
        file_name = a_tag.text
        href = a_tag['href']
        date = file_name.split('.')[0]
        try:
            date = datetime.datetime.strptime(date, '%Y%m%d').date()
        except ValueError:
            date = None

        # Extracting the text after the A tag
        remaining_text = item.get_text().replace(file_name, "").strip()

        # Using regular expressions to extract file size and MD5 hash
        size_match = re.search(r'\(([\d\.]+[KMG]?B)\)', remaining_text)
        md5_match = re.search(r'MD5:\s*([a-fA-F0-9]{32})', remaining_text)

        file_size = size_match.group(1) if size_match else None
        md5_hash = md5_match.group(1) if md5_match else None

        result.append({
            'file_name': file_name,
            'href': href,
            'file_size': file_size,
            'md5_hash': md5_hash,
            "date": date
        })

    return result

# COMMAND ----------

file_info = extract_file_info(html)

# COMMAND ----------

file_info

# COMMAND ----------

# Define the date range (inclusive)
start_date = datetime.datetime.strptime('2023-08-13', '%Y-%m-%d').date()
end_date = datetime.datetime.strptime('2024-08-14', '%Y-%m-%d').date()

# Filter the list by the date range
filtered_data = []
for item in file_info:
    date = item['date']
    
    if date is None:
        continue
    
    data_is_in_range = (start_date <= date <= end_date)
    if data_is_in_range:
        filtered_data.append(item)

# COMMAND ----------

len(filtered_data)

# COMMAND ----------

file_names = jmespath.search('[].file_name', filtered_data)

# COMMAND ----------

chunk_size = 10
chunks = [file_names[i:i + chunk_size] for i in range(0, len(file_names), chunk_size)]
chunks = [{"file_names": chunk, "type": "events"} for chunk in chunks]

# COMMAND ----------

len(chunks)

# COMMAND ----------

# Son 376 archivos distribuidos en 37 chunks, con lo cual se mandaran a ejecutar 37 lambdas

# COMMAND ----------

lambda_client = boto3.client('lambda', region_name='us-east-1')
function_name = 'factored-hackaton-2024-unlock-downloader-lambda'
for chunk in chunks:
    payload = chunk
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',
        Payload=json.dumps(payload)
    )    
    print(f"Invocación asíncrona enviada. StatusCode: {response['StatusCode']}")

# COMMAND ----------


