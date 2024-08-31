# ml-pipeline

This project utilizes Pinecone and OpenAI to create an efficient vector database based on embeddings generated from clean and processed data. Below is a description of the scripts included in this folder and their purpose.

## Project Structure

- `batch_data_loader_to_pinecone.py`
- `embedding_generator.py`
- `pinecone_vector_database.py`
- `run.py`


## Script Descriptions

### 1. `batch_data_loader_to_pinecone.py`

**Purpose:**  
This script loads batches of processed data into the Pinecone vector database. It is useful for handling large volumes of data, ensuring that the generated embeddings are efficiently stored in Pinecone.

**Usage:**  
Run this script after generating the embeddings and cleaning the data. The script is configured to process the data in batches, optimizing the loading process into Pinecone.

### 2. `embedding_generator.py`

**Purpose:**  
This script generates embeddings from clean data using the OpenAI model. These embeddings are vectors that represent the data in a way that can be used for efficient comparisons and searches within the vector database.

**Usage:**  
Run this script after cleaning the data. The generated embeddings can be stored in a file or passed directly to the next processing step.

### 3. `pinecone_vector_database.py`

**Purpose:**  
This script manages direct interaction with the Pinecone vector database. It includes functions to create, update, search, and delete vectors in the database.

**Usage:**  
This script serves as a helper module and can be imported into other scripts when interaction with Pinecone is needed. Make sure to configure it properly with your Pinecone account credentials.

### 4. `run.py`

**Purpose:**  
This script orchestrates the complete execution of the pipeline, from data cleaning to loading embeddings into Pinecone. It is the main entry point of the project.

**Usage:**  
Run this script to start the entire process. It is recommended to have all the scripts configured beforehand and to ensure that the data is ready.

---


## Execution

1. Clean and preprocess the data using `data_clean.ipynb`.
2. Generate embeddings with `embedding_generator.py`.
3. Load the data into Pinecone with `batch_data_loader_to_pinecone.py` or run the entire pipeline with `run.py`.

---

This README should provide you with a clear overview of how to use each script in this project. Good luck!