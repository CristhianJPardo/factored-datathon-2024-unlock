import streamlit as st

### Buscador con embedigs

st.markdown("## Embeding Search")

title = st.text_input("Search News: ")
if title:
    st.write("Your results for", title)
