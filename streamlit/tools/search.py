import os
import logging
import streamlit as st
from pinecone import Pinecone
from dotenv import load_dotenv
from typing import List
import openai
import time
import boto3
import json

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenAI
openai_api_key = os.getenv("OPENAI_KEY")
MODEL_ID = "text-embedding-ada-002"

# Configuración de Pinecone
API_KEY = os.getenv("PINECONE")
INDEX_NAME = "news-idx"
DIM = 1536
pc = Pinecone(api_key=API_KEY)

# Configuracion AWS

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

bucket_name = 'factored-hackaton-2024-unlock-medallion-bucket'
catalog = 'catalog=factored_hackaton_2024'
schema = 'schema=silver'

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION 
)

def summarize_content(content):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Puedes usar "gpt-4" si tienes acceso
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": f"Please summarize the following content:\n\n{content}"}
        ],
        max_tokens=100,  # Ajusta el número de tokens para controlar la longitud del resumen
        temperature=0.7
    )
    summary = response.choices[0].message.content
    return summary

def get_json_from_s3(s3_client, bucket_name, catalog, schema, md5_id):
    
    prefix = f"{catalog}/{schema}/scraped_json/md5_id={md5_id}/"
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    json_file_key = None
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.json'):
            json_file_key = obj['Key']
            break
    
    if not json_file_key:
        raise FileNotFoundError(f"No se encontrÃ³ un archivo JSON en la carpeta con md5_id={md5_id}")
    
    json_object = s3_client.get_object(Bucket=bucket_name, Key=json_file_key)
    json_content = json_object['Body'].read().decode('utf-8')
    json_dict = [json.loads(line) for line in json_content.strip().splitlines()][0]
    return json_dict

def get_multiple_jsons(s3_client, bucket_name, catalog, schema, md5_ids):
    json_results = []
    
    for md5_id in md5_ids:
        try:
            json_data = get_json_from_s3(s3_client, bucket_name, catalog, schema, md5_id)
            json_results.append(json_data)
        except Exception as e:
            print(f"Error processing md5_id={md5_id}: {e}")
            json_results.append({})
    
    return json_results

def query(texts: List[str]) -> List[List[float]]:
    """
    Consulta el modelo de OpenAI para generar embeddings a partir de una lista de textos.

    :param texts: Lista de cadenas de texto.
    :return: Lista de embeddings, cada uno representado como una lista de números.
    """
    try:
        response = openai.embeddings.create(input=texts, model=MODEL_ID)
        embeddings = [embedding.embedding for embedding in response.data]
        logging.info("Embeddings retrieved successfully.")
        return embeddings
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return []  # Cambiado de None a lista vacía para evitar errores posteriores


def knn_pinecone(question: str, k: int):
    """
    Realiza una búsqueda de k vecinos más cercanos para la pregunta dada en el índice Pinecone.
    """
    index = pc.Index(INDEX_NAME)

    # Genera el embedding para la pregunta
    embeddings = query([question])
    # st.write("Results for:",openai_api_key )

    if not embeddings:  # Verifica si embeddings es una lista vacía
        return {
            "matches": []
        }  # Devuelve un diccionario vacío con clave "matches" para evitar errores

    embedding_question = embeddings[0]

    try:
        # Realiza la consulta en el índice
        query_results = index.query(
            namespace="ns1", vector=embedding_question, top_k=k, include_values=True
        )

        return query_results
    except Exception as e:
        raise RuntimeError(f"Failed to query the index: {e}")
    

def search_pinecone(question, k = 4):

    results = knn_pinecone(question, k)
    id_list: list= [results["matches"][i]['id'] for i in range(k)]
    return id_list



st.markdown("## Embedding Search")

title = st.text_input("🔍 Search News:")
if title:
    # st.write("Results for:", title)

    md5_ids: list = search_pinecone(title)
    with st.spinner("Searching..."):
        time.sleep(5)
        json_data_list: list = get_multiple_jsons(s3_client, bucket_name, catalog, schema, md5_ids)  # keys: (title, content, url)

    if json_data_list:
        for data in json_data_list:
            # Generar un resumen del contenido
            summary = summarize_content(data['content'][0:500])
            st.markdown(f"### [{data['title']}]({data['url']})")
            st.markdown(f"{summary}")
            # st.markdown(f"{data['content'][0:200]}") # TODO: usar la api de openai para los resumenes
            # st.markdown(f"[Read more]({data['url']})")
            st.markdown("---")  # Línea divisoria entre resultados
    else:
        st.write("No results found.")