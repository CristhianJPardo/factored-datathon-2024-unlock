import streamlit as st
import os
import json
from dotenv import load_dotenv
import delta_sharing
from pinecone import Pinecone

load_dotenv()  # take environment variables from .env.

#################
## Page Config ##
#################
st.set_page_config(
    page_title="Unlock",
    layout="wide",
    initial_sidebar_state="auto",
)

#########################################################
SHARECREDENTIALSVERSION = os.getenv("SHARECREDENTIALSVERSION")
BEARERTOKEN = os.getenv("BEARERTOKEN")
ENDPOINT = os.getenv("ENDPOINT")
EXPIRATIONTIME = os.getenv("EXPIRATIONTIME")

API_KEY = os.getenv("PINECONE")
INDEX_NAME = "news-idx"
DIM = 1536
pc = Pinecone(api_key=API_KEY)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

bucket_name = 'factored-hackaton-2024-unlock-medallion-bucket'
catalog = 'catalog=factored_hackaton_2024'
schema = 'schema=silver'

credentials = {
    "shareCredentialsVersion": SHARECREDENTIALSVERSION,
    "bearerToken": BEARERTOKEN,
    "endpoint": ENDPOINT,
    "expirationTime": EXPIRATIONTIME,
}

file_name = "config.share"


# Write the dictionary to a JSON file in a single line
with open(file_name, "w") as json_file:
    json.dump(credentials, json_file, separators=(",", ":"), ensure_ascii=False)


# Point to the profile file. It can be a file on the local file system or a file on a remote storage.
profile_file = file_name

# Create a SharingClient.
client = delta_sharing.SharingClient(profile_file)


@st.cache_data
def fetch_and_clean_data(schema, table_name):
    data_name = profile_file + f"#unlock-share-streamlit.{schema}.{table_name}"
    data = delta_sharing.load_as_pandas(data_name)
    return data


df_news_per_day = fetch_and_clean_data("platinum", "news_per_day")
df_total_database_size = fetch_and_clean_data("platinum", "total_database_size")
############################################################


st.sidebar.title("Unlock Team")
st.sidebar.markdown("""
                   - **[Juan Pablo Gomez](https://www.linkedin.com/in/juan-pablo-gomez-mendez/)**
                        - *Software Engineer*
                   - **[Christian Pardo](https://www.linkedin.com/in/cristhian-pardo/)**
                        - *Data Architect*
                   -  **[Eduards Mendez](https://www.linkedin.com/in/eduards-alexis-mendez-chipatecua-8584b21b4/)**
                        - *Machine Learning Engineer*
                   - **[Daniel Melo](https://www.linkedin.com/in/daniel-melo-09aa82325/)**
                        - *Data Engineer*
                    """)
## Page Title ##
col1, col2, col3 = st.columns(3)
col1.title("Unlock")
col2.metric(
    "Aggregated Today",
    str(df_news_per_day["date"].tolist()[0]),
    str(
        int(df_news_per_day["news_per_day"].tolist()[0])
        - int(df_news_per_day["news_per_day"].tolist()[1])
    ),
)
col3.metric(
    "Today News", int(df_total_database_size["total_database_size"].tolist()[0])
)
st.divider()

## Navigation ##
status = st.Page(
    "tools/status.py", title="Status", icon=":material/insert_chart_outlined:"
)
search = st.Page("tools/search.py", title="Search", icon=":material/search:")
chat = st.Page("tools/chat.py", title="Chat", icon=":material/chat:")
product = st.Page("tools/product.py", title="Product", icon=":material/dashboard:")
pg = st.navigation({"Tools": [product, search, chat, status]})

## Run Page ##
pg.run()
