from pinecone import Pinecone, ServerlessSpec
import embedding_generator
from typing import List, Dict
import pandas as pd
import os

# Configuración de Pinecone
API_KEY = os.getenv("PINECONE")
INDEX_NAME = "news-idx"
DIM = 1536

pc = Pinecone(api_key=API_KEY)


def create_index_if_not_exists(index_name: str, dimension: int):
    """
    Crea el índice en Pinecone si no existe.
    """
    if index_name not in pc.list_indexes().names():
        try:
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            print(f"Index '{index_name}' created successfully.\n")
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {e}")


def save_embeddings(df: pd.DataFrame, index_name: str, dimension: int):
    """
    Guarda embeddings en el índice Pinecone.
    """
    # Verifica que el DataFrame tenga las columnas necesarias
    if "title" not in df.columns or "embedding" not in df.columns:
        raise ValueError("DataFrame must contain 'title' and 'embedding' columns")

    # Crea el índice si no existe
    create_index_if_not_exists(index_name, dimension)

    index = pc.Index(index_name)
    print(index.describe_index_stats())

    # Prepara los embeddings para la inserción en el índice
    title_embeddings: List[Dict[str, List[int]]] = [
        {"id": idx, "values": embedding}
        for idx, embedding in zip(df["md5_id"].tolist(), df["embedding"].tolist())
    ]

    try:
        # Carga embeddings en el índice
        index.upsert(title_embeddings, namespace="ns1")
        print("Embeddings upserted successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to upsert embeddings: {e}")

    try:
        # Imprime estadísticas del índice
        stats = index.describe_index_stats()
        print("Index stats:", stats)
    except Exception as e:
        raise RuntimeError(f"Failed to describe index stats: {e}")


def knn_pinecone(question: str, k: int):
    """
    Realiza una búsqueda de k vecinos más cercanos para la pregunta dada en el índice Pinecone.
    """
    index = pc.Index(INDEX_NAME)

    # Genera el embedding para la pregunta
    embedding_question = embedding_generator.query(question)

    try:
        # Realiza la consulta en el índice
        query_results = index.query(
            namespace="ns1", vector=embedding_question, top_k=k, include_values=True
        )

        return query_results
    except Exception as e:
        raise RuntimeError(f"Failed to query the index: {e}")


if __name__ == "__main__":
    from x import json_to_dataframe

    # Carga el DataFrame desde archivos JSON
    df = json_to_dataframe("web-scrapping/scraper/extraction/*.json")

    # Genera embeddings para el contenido del DataFrame
    embeddings = embedding_generator.query(df["content"].tolist())
    df["embedding"] = embeddings

    # Guarda los embeddings en el índice de Pinecone
    save_embeddings(df, INDEX_NAME, DIM)
    # Realiza una búsqueda de ejemplo
    question = "news about turkey"
    k = 10  # Número de vecinos más cercanos a recuperar
    results = knn_pinecone(question, k)
    for i in range(k):
        print(f"\n{results["matches"][i]['id']}")
