from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
import requests
import logging
from requests.exceptions import HTTPError, Timeout
import openai


# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
openai.api_key = os.getenv("OPENAI_KEY")
MODEL_ID = "text-embedding-ada-002"

def query(texts: List[str]) -> List[List[float]]:
    """
    Consulta el modelo de OpenAI para generar embeddings a partir de una lista de textos.

    :param texts: Lista de cadenas de texto.
    :return: Lista de embeddings, cada uno representado como una lista de números.
    """
    try:
        response = openai.embeddings.create(
            input=texts,
            model=MODEL_ID
        )
        embeddings = [embedding.embedding for embedding in response.data]
        logging.info("Embeddings retrieved successfully.")

        return embeddings
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        logging.error(f"Request timed out: {timeout_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    return None

############################################################## PINECONE

# Configuración de Pinecone
API_KEY = os.getenv('PINECONE')
INDEX_NAME = "news-idx"
DIM = 1536

pc = Pinecone(api_key=API_KEY)

    
def knn_pinecone(question: str, k: int):
    """
    Realiza una búsqueda de k vecinos más cercanos para la pregunta dada en el índice Pinecone.
    """
    index = pc.Index(INDEX_NAME)
    
    # Genera el embedding para la pregunta
    embedding_question = query(question)

    try:
        # Realiza la consulta en el índice
        query_results = index.query(
            namespace="ns1",
            vector=embedding_question,
            top_k=k,
            include_values=True
        )
            
        return query_results
    except Exception as e:
        raise RuntimeError(f"Failed to query the index: {e}")





# Interfaz de Streamlit
st.markdown("## Embedding Search")

title = st.text_input("Search News:")
if title:
    st.write("Your results for:", title)
    
    # Realizar la búsqueda utilizando la función existente `knn_pinecone`
    k = 10  # Número de vecinos más cercanos a recuperar
    results = knn_pinecone(title, k)
    
    # Mostrar los resultados
    for i in range(k):
        st.write(f"Result {i+1}: {results['matches'][i]['id']}")
