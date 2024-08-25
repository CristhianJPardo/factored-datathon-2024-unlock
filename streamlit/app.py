import streamlit as st
from datetime import datetime
#################
## Page Config ##
#################
st.set_page_config(
    page_title="Unlock",
    page_icon="static/dollar.png",
    layout="wide",
    initial_sidebar_state="auto",
)
# If you want to add a logo to the page, uncomment the line below and add the path to the image
#st.logo("static/key.png", icon_image="static/key.png")

## Banner Config ##
#st.image("static/unlock.png", use_column_width=None)

## Page Title ##
st.title("Unlock")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

## Navigation ##
status = st.Page("tools/status.py", title="Status", icon=":material/insert_chart_outlined:")
search = st.Page("tools/search.py", title="Search", icon=":material/search:")
chat = st.Page("tools/chat.py", title="Chat", icon=":material/chat:")
visualization = st.Page("tools/visualization.py", title="Visualization", icon=":material/dashboard:")
pg = st.navigation({"Tools": [status, search, chat, visualization]})

## Run Page ##
pg.run()

