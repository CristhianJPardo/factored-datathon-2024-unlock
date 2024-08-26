import glob
import json
import pandas as pd
from typing import List, Dict, Union
import re
import unicodedata

def clean_text(content: Union[str, List[str]]) -> str:
    """
    Une elementos de una lista en un solo string si es necesario y limpia el texto eliminando saltos de línea
    y espacios en blanco innecesarios.

    :param content: Texto en forma de lista de strings o un solo string.
    :return: Texto limpio en un solo string.
    """
    if isinstance(content, list):
        cleaned_text = " ".join(content)
    else:
        cleaned_text = content

    # Eliminar saltos de línea y tabs, y reducir múltiples espacios a uno solo
    cleaned_text = " ".join(cleaned_text.replace("\r\n", " ")
                                          .replace("\n", " ")
                                          .replace("\r", " ")
                                          .replace("\t", " ")
                                          .split())
    return cleaned_text

def clean_id(text: str) -> str:
    """
    Limpia el texto para usarlo como un ID válido en Pinecone, asegurando que solo contenga caracteres ASCII
    y que conserve los espacios.

    :param text: Texto para limpiar y convertir en un ID válido.
    :return: ID limpio y válido.
    """
    # Normaliza el texto para eliminar acentos y convierte a ASCII
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    
    # Reemplaza caracteres no permitidos excepto espacios
    text = re.sub(r'[^a-zA-Z0-9-_ ]', '', text)  # Permite caracteres alfanuméricos, guiones y espacios
    
    # Elimina espacios extra al principio o al final del texto
    text = text.strip()
    
    return text[:255]  # Limita el ID a 255 caracteres para evitar problemas con Pinecone


def load_json_files(path_pattern: str) -> List[Dict[str, list]]:
    """
    Carga múltiples archivos JSON de una ruta especificada y los devuelve como una lista de diccionarios.

    :param path_pattern: Patrón de ruta para buscar los archivos JSON.
    :return: Lista de diccionarios con los datos de los archivos JSON.
    """
    files = glob.glob(path_pattern)
    data = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data.append(json.load(f))
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al cargar el archivo {file}: {e}")
    return data


def json_to_dataframe(path_pattern: str) -> pd.DataFrame:
    """
    Convierte una colección de archivos JSON a un DataFrame de pandas, limpiando previamente el contenido.

    :param path_pattern: Patrón de ruta para buscar los archivos JSON.
    :return: DataFrame de pandas con los datos de los JSON.
    """
    data = load_json_files(path_pattern)
    for row in data:
        row["title"] = clean_id(clean_text(row.get("title", "")))
        row["content"] = clean_text(row.get("content", ""))
    
    return pd.DataFrame(data)


def test_transform_data():
    """
    Función de prueba para cargar datos desde JSON, transformarlos y mostrarlos.
    """
    df = json_to_dataframe('web-scrapping/scraper/extraction/*.json')
    print(df)

    return(df)


if __name__ == "__main__":
    test_transform_data()
