import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json
import os
from dotenv import load_dotenv
import delta_sharing

# Load environment variables
load_dotenv()

# Constants
SHARECREDENTIALSVERSION = os.getenv("SHARECREDENTIALSVERSION")
BEARERTOKEN = os.getenv("BEARERTOKEN")
ENDPOINT = os.getenv("ENDPOINT")
EXPIRATIONTIME = os.getenv("EXPIRATIONTIME")
PROFILE_FILE = "config.share"

# Prepare Delta Sharing credentials
credentials = {
    "shareCredentialsVersion": SHARECREDENTIALSVERSION,
    "bearerToken": BEARERTOKEN,
    "endpoint": ENDPOINT,
    "expirationTime": EXPIRATIONTIME,
}

# Write the credentials to a JSON file
with open(PROFILE_FILE, "w") as json_file:
    json.dump(credentials, json_file, separators=(",", ":"), ensure_ascii=False)

# Create a SharingClient
client = delta_sharing.SharingClient(PROFILE_FILE)


@st.cache_data
def fetch_data(schema, table_name):
    """Fetch and clean data from Delta Sharing."""
    data_name = f"{PROFILE_FILE}#unlock-share-streamlit.{schema}.{table_name}"
    try:
        data = delta_sharing.load_as_pandas(data_name)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Fetch data
# events = fetch_data("silver", "events")
# chart_data = events[['actiongeo_lat', 'actiongeo_long']].dropna()
# print(chart_data.head())

## Page for usage cases and visualization
# st.set_page_config(page_title="Travel Insights Dashboard", layout="wide")

# Title and introductory text
st.title("Travel Insights Dashboard")
st.markdown("""
Welcome to the Travel Insights Dashboard! This application provides valuable information and insights for travelers. Use the tabs below to explore various features and visualizations.
""")

## Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Search", "Chat", "Status"])

# Search Tab
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://imagenes.elpais.com/resizer/v2/CFYWKVZDMFAZNIRMN5HWEY6MBE.jpg?auth=e1b10fa00d720a75d34a06876424542bc3ffb334b971c7cc93d6b0d89dc4b82a&width=1960&height=1470&focal=889%2C501",
            caption="Travel is the only thing you can buy that makes you richer.",
        )
    with col2:
        st.header("Embedding Search")
        st.markdown("""
Traveling to a new country can be an exciting and enriching experience 😄. However, to ensure that your trip is safe and enjoyable, it's essential to stay informed about current events and potential risks that could affect your itinerary ⚠️. Situations in each country can change rapidly, and being well-informed will allow you to make better decisions and adapt to any unexpected circumstances.

This news finder provides the perfect tool to keep you updated on everything relevant in the country you’re visiting 🗺️. From security issues and local conflicts 🚨 to weather conditions 🌧️ that might influence your plans, this service gives you the necessary information to prepare adequately and avoid unpleasant surprises.

With advanced technologies like Pinecone and OpenAI 🧠, you can access the most relevant and up-to-date articles based on your specific queries 🗞️. This means you’ll not only stay informed about important events but also receive personalized information that suits your needs and concerns. With this tool, you can plan your trip more securely, be prepared for any eventuality, and enjoy a smoother, more seamless travel experience 👍.
""")
# Chat Tab
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.header("Chat with Our Intelligent Agent")
        st.markdown("""

        """)
        st.markdown("""
    You are an advanced intelligent agent designed to support a travel insurance agency and its end users by performing essential tasks:

    - **Querying News Articles**: Retrieve the latest information on travel-related topics from our database.
    - **Monitoring Global Travel Restrictions**: Stay updated with current travel policies and regulations.
    - **Analyzing Public Sentiment**: Evaluate and interpret public opinion on travel and health issues.
    - **Validating Statements about Monkeypox Outbreaks**: Verify and provide accurate information on disease outbreaks.

    For any queries, you can ask about travel advisories, restrictions, public sentiment, or disease outbreaks.
    """)
    with col2:
        st.image(
            "https://i.cbc.ca/1.2730018.1437112433!/fileImage/httpImage/image.jpg_gen/derivatives/16x9_780/hitchbot-victoria-or-bust.jpg"
        )

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            "https://images.ctfassets.net/pdf29us7flmy/1OY6V5qnB5e490hm3lTK2i/c490cc85b117b64bc5ac10f0b9d6f1a4/GOLD-6487-CareerGuide-Batch04-Images-GraphCharts-04-Histogram.png"
        )
    with col2:
        st.header("Status")
        st.markdown(
            """
In this section, you'll find detailed information about the current state of our dataset. Here’s what you can expect to find:

- **Dataset Size:** Get an overview of the total volume of data available, including file sizes and the number of records. This helps you gauge the scale and comprehensiveness of the dataset.
- **Last Updated:** Check the most recent update timestamp to ensure you're working with the latest data. We regularly refresh our datasets to incorporate new information and maintain accuracy.
- **Update Frequency:** Learn about how often the dataset is updated. Whether it’s daily, weekly, or monthly, this information helps you understand the freshness of the data.
- **Version History:** Access a log of changes made to the dataset over time. This includes major updates, corrections, and any modifications that could impact your use of the data.
- **Data Integrity Checks:** Find details about the quality assurance processes in place to ensure the reliability and consistency of the data. This section includes information on validation checks and error handling practices.

Stay informed about the state of the dataset to better manage your data-driven projects and ensure that your analyses are based on the most current and accurate information available.
            """
        )
st.divider()

# Visualization
st.header("Visualization")
chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=chart_data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                auto_highlight=True,
                coverage=1,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
                pickable=True,
            ),
        ],
    )
)
