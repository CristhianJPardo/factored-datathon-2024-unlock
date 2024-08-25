import os
import requests
import logging
from retry import retry
from requests.exceptions import HTTPError, Timeout
from typing import List
from dotenv import load_dotenv
import openai

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
openai.api_key = os.getenv("OPENAI_KEY")
MODEL_ID = "text-embedding-ada-002"

@retry(tries=3, delay=10)
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

if __name__ == "__main__":
    from json_cleaner_and_converter import json_to_dataframe

    try:
        # Cargar y procesar el DataFrame
        df = json_to_dataframe('web-scrapping/scraper/extraction/*.json')
        logging.info("DataFrame loaded successfully.")

        # Obtener embeddings para el contenido
        embeddings = query(df["content"].tolist())
        if embeddings:
            df["embedding"] = embeddings  # Agregar embeddings al DataFrame
            logging.info("Embeddings successfully added to the DataFrame.")
        else:
            logging.error("Failed to retrieve embeddings.")

        print(df)
    except Exception as e:
        logging.error(f"An error occurred while processing the DataFrame: {e}")
