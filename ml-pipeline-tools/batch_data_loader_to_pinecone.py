# Importamos las librerías necesarias
import pandas as pd
import tiktoken
import json
import os

# Definimos las funciones
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Retorna el número de tokens en un string de texto."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def batch_de_json(json_lines_file, max_tokens_per_batch= 50_000):
    """
    Recibe un archivo JSON Lines (json line) y genera baches donde cada bache tiene menos de max_tokens_per_batch tokens.
    Cada bache se guarda como un archivo JSON separado.
    """
    encoding = tiktoken.get_encoding("cl100k_base")

    with open(json_lines_file, 'r') as file:
        json_lines = file.readlines()

    batches = []
    current_batch = []
    current_token_count = 0

    for line in json_lines:
        record = json.loads(line)
        content = record.get('content', '')
        tokens = num_tokens_from_string(content, "cl100k_base")
        
        if current_token_count + tokens > max_tokens_per_batch:
            # Si añadir este registro excede el límite de tokens, guarda el batch actual
            batches.append(current_batch)
            current_batch = []
            current_token_count = 0
        
        # Añadir el registro al batch actual
        current_batch.append(record)
        current_token_count += tokens

    # Añadir el último batch si no está vacío
    if current_batch:
        batches.append(current_batch)

    # Guardar los baches como archivos JSON
    for i, batch in enumerate(batches, start=1):
        with open(f'batch_{i}.json', 'w') as batch_file:
            json.dump(batch, batch_file, ensure_ascii=False, indent=4)

def conteo_de_cantidad_de_tokens_total(df):
    """
    Recibe un dataframe con las columnas: 'title', 'content', 'md5_id', 'url'.
    Calcula la cantidad de tokens en la columna 'content' y suma la cantidad de tokens totales.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    df['num_tokens'] = df['content'].apply(lambda x: len(encoding.encode(x)))
    total_tokens = df['num_tokens'].sum()
    return total_tokens

def json_to_dataframe(json_files):
    """
    Recibe una lista de archivos JSON y los convierte en un dataframe.
    """
    dataframes = []
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            df = pd.DataFrame(data)
            dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# Paso 1: Divide el archivo data.json en batches con menos de 1,000,000 tokens
batch_de_json('data.json')

# Paso 2: Obtén la lista de archivos JSON generados
json_files = [f'batch_{i}.json' for i in range(1, len(os.listdir()) + 1) if os.path.isfile(f'batch_{i}.json')]

# Paso 3: Calcula la cantidad de tokens para cada archivo JSON creado y para el total
total_tokens = 0
tokens_summary = {}

for i, json_file in enumerate(json_files, start=1):
    # Convierte el archivo JSON a un DataFrame
    with open(json_file, 'r') as file:
        data = json.load(file)
        df = pd.DataFrame(data)
    
    # Calcula la cantidad de tokens en el DataFrame
    tokens_in_batch = conteo_de_cantidad_de_tokens_total(df)
    total_tokens += tokens_in_batch
    
    # Guarda la cantidad de tokens en el resumen
    tokens_summary[json_file] = tokens_in_batch
    
    # Imprime la cantidad de tokens en el bache actual
    print(f'Cantidad de tokens en {json_file}: {tokens_in_batch}')

# Imprime la cantidad total de tokens
print(f'Cantidad total de tokens en todos los baches: {total_tokens}')

# Paso 4: Guarda el resumen de tokens en un archivo JSON
#with open('tokens_summary.json', 'w') as summary_file:
#    json.dump(tokens_summary, summary_file, ensure_ascii=False, indent=4)
