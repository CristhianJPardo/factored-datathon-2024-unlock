
import streamlit as st
import pinecone_vector_database  # Suponiendo que aquí está implementada la función knn_pinecone

# Interfaz de Streamlit
st.markdown("## Embedding Search")

title = st.text_input("Search News:")
if title:
    st.write("Your results for:", title)
    
    # Realizar la búsqueda utilizando la función existente `knn_pinecone`
    k = 10  # Número de vecinos más cercanos a recuperar
    results = pinecone_vector_database.knn_pinecone(title, k)
    
    # Mostrar los resultados
    for i in range(k):
        st.write(f"Result {i+1}: {results['matches'][i]['id']}")
