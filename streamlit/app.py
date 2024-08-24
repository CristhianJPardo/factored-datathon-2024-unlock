import streamlit as st
from datetime import datetime
#################
## Page Config ##
#################
st.set_page_config(
    page_title="Unlock",
    page_icon="static/dollar.png",
    layout="centered",
    initial_sidebar_state="auto",
)


## Banner Config ##
#st.image("static/unlock.png", use_column_width=None)

## Page Title ##
st.title("Unlock")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

## Navigation ##
search = st.Page("tools/search.py", title="Search", icon=":material/search:")
chat = st.Page("tools/chat.py", title="Chat", icon=":material/chat:")
visualization = st.Page("tools/visualization.py", title="Visualization", icon=":material/dashboard:")
pg = st.navigation({"Tools": [search, chat, visualization]})

## Run Page ##
pg.run()

