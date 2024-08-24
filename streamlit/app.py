import streamlit as st

#################
## Page Config ##
#################
st.set_page_config(
    page_title="Unlock",
    page_icon="static/dollar.png",
    layout="centered",
    initial_sidebar_state="auto",
)




st.title("Unlock")
search = st.Page("tools/search.py", title="Search", icon=":material/search:")
chat = st.Page("tools/chat.py", title="History", icon=":material/history:")
visualization = st.Page(
    "tools/visualization.py", title="Visualization", icon=":material/dashboard:"
)

pg = st.navigation(
        {
            #"Account": [logout_page],
            #"Reports": [dashboard, bugs, alerts],
            "Tools": [search, chat, visualization],
        }
    )
pg.run()

