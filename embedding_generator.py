import os
import requests
import logging
from retry import retry
from requests.exceptions import HTTPError, Timeout
from typing import List

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración del modelo y API token
model_id = os.getenv("MODEL_ID", "sentence-transformers/all-MiniLM-L6-v2") # Este modelo genera embeddings de dimension 384
hf_token = os.getenv("HF_TOKEN", "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")

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

@retry(tries=3, delay=10)
def query(texts) ->List[list]:
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": texts})
        response.raise_for_status()  # Levanta un error en caso de un status 4XX/5XX
        result = response.json()

        if isinstance(result, list):
            return result
        elif "error" in result:
            raise RuntimeError("The model is currently loading, please re-run the query.")
        else:
            logging.error("Unexpected response format: %s", result)
            return None
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
        df = json_to_dataframe('web-scrapping/scraper/extraction/*.json')
        embeddings = query(df["content"].tolist())

        if embeddings is not None:
            df["embedding"] = embeddings  # type of embedding List[int]
            logging.info("Embeddings successfully added to the DataFrame.")
        else:
            logging.error("Failed to retrieve embeddings.")

        print(df)
    except Exception as e:
        logging.error("An error occurred while processing the DataFrame: %s", e)
