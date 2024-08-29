import os
import logging
import streamlit as st
from pinecone import Pinecone
from dotenv import load_dotenv
from typing import List
import openai

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


st.markdown("## Embedding Search")

title = st.text_input("🔍 Search News:")
if title:
    st.write("Results for:", title)

    # Realizar la búsqueda utilizando la función existente `knn_pinecone`
    k = 10  # Número de vecinos más cercanos a recuperar
    results = knn_pinecone(title, k)

    # Mostrar los resultados
    if results and "matches" in results and results["matches"]:
        for i in range(
            min(k, len(results["matches"]))
        ):  # Verifica el número de resultados
            st.write(f"Result {i+1}: {results['matches'][i]['id']}")
    else:
        st.write("No results found.")
