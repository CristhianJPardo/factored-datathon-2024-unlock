import pandas as pd
from glob import glob
import embedding_generator
from pinecone_vector_database import save_embeddings
import time



# Configuración de Pinecone
INDEX_NAME = "news-idx"
DIM = 1536
WAIT_TIME = 60  # Tiempo en segundos para esperar entre los lotes

def process_file(file_path: str):
    """
    Carga el archivo JSON, genera embeddings y guarda en el índice de Pinecone.
    """
    try:
        # Lee el archivo JSON y crea un DataFrame
        df = pd.read_json(file_path)
        
        # Verifica que la columna 'content' exista en el DataFrame
        if 'content' not in df.columns:
            raise ValueError(f"El archivo {file_path} no contiene la columna 'content'")

        # Genera embeddings para el contenido del DataFrame
        embeddings = embedding_generator.query(df["content"].tolist())
        df["embedding"] = embeddings

        # Guarda los embeddings en el índice de Pinecone
        save_embeddings(df, INDEX_NAME, DIM)
        
        print(f"Embeddings guardados exitosamente para {file_path}")

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")

def main():
    # Encuentra todos los archivos JSON en el directorio
    dir_files = glob('data/batch_*.json')
    print("Inicio para la generacion de embeddings y guardado\n")
    # Procesa cada archivo JSON
    for idx_batch,data in enumerate(dir_files):
        process_file(data)
        time.sleep(WAIT_TIME)  # Espera entre lotes para evitar sobrecargar el servicio
        print(f"\tbatch numero: {idx_batch}")

if __name__ == "__main__":
    main()
