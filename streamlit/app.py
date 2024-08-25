import streamlit as st
from datetime import datetime
import os
import json
from dotenv import load_dotenv
import delta_sharing

load_dotenv()  # take environment variables from .env.

#########################################################
SHARECREDENTIALSVERSION = os.getenv("SHARECREDENTIALSVERSION")
BEARERTOKEN = os.getenv("BEARERTOKEN")
ENDPOINT = os.getenv("ENDPOINT")
EXPIRATIONTIME = os.getenv("EXPIRATIONTIME")

credentials = {
	"shareCredentialsVersion": SHARECREDENTIALSVERSION,
	"bearerToken": BEARERTOKEN,
	"endpoint": ENDPOINT,
	"expirationTime": EXPIRATIONTIME,
}

file_name = "config.share"


# Write the dictionary to a JSON file in a single line
with open(file_name, 'w') as json_file:
    json.dump(credentials, json_file, separators=(',', ':'), ensure_ascii=False)


# Point to the profile file. It can be a file on the local file system or a file on a remote storage.
profile_file = file_name

# Create a SharingClient.
client = delta_sharing.SharingClient(profile_file)

# List all shared tables.
# print(client.list_all_tables())

news_per_day = profile_file + "#unlock-share-streamlit.platinum.news_per_day"
total_database_size = profile_file + "#unlock-share-streamlit.platinum.total_database_size"

df_news_per_day = delta_sharing.load_as_pandas(news_per_day)
df_total_database_size = delta_sharing.load_as_pandas(total_database_size)


print(df_news_per_day.head())
# TODO: GUARDAR DATOS EN CACHE
############################################################

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

