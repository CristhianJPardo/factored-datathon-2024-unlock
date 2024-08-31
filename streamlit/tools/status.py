"""# Status"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
df_news_per_day = fetch_data("platinum", "news_per_day")
df_total_database_size = fetch_data("platinum", "total_database_size")

# Ensure data is available
if df_news_per_day.empty:
    st.error("No data available for 'news_per_day'")
else:
    # Convert 'date' column to datetime
    df_news_per_day["date"] = pd.to_datetime(df_news_per_day["date"])

    # Streamlit application configuration
    st.title("Daily News Visualization")

    # Line Chart
    st.subheader("Number of News Articles per Day")
    fig = px.line(
        df_news_per_day,
        x="date",
        y="news_per_day",
        title="Daily News Articles Count",
        labels={"date": "Date", "news_per_day": "Number of News Articles"},
    )
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    # Bar Chart
    st.subheader("Daily News Articles (Bar Chart)")
    fig = px.bar(
        df_news_per_day,
        x="date",
        y="news_per_day",
        title="Daily News Articles Count",
        labels={"date": "Date", "news_per_day": "Number of News Articles"},
    )
    st.plotly_chart(fig)

    # Timeline Chart
    st.subheader("Timeline of News Articles")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_news_per_day["date"],
            y=df_news_per_day["news_per_day"],
            mode="markers+lines",
            marker=dict(color="blue", size=8),
            line=dict(width=2),
            name="News Articles",
        )
    )
    fig.update_layout(
        title="Timeline of News Articles",
        xaxis_title="Date",
        yaxis_title="Number of News Articles",
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )
    st.plotly_chart(fig)

    # Distribution Plot
    st.subheader("Distribution of Number of News Articles")
    fig = px.histogram(
        df_news_per_day,
        x="news_per_day",
        nbins=30,
        title="Distribution of Number of News Articles",
    )
    fig.update_layout(xaxis_title="Number of News Articles", yaxis_title="Frequency")
    st.plotly_chart(fig)

    # Moving Average
    st.subheader("Moving Average of News Articles")
    df_news_per_day["moving_avg"] = (
        df_news_per_day["news_per_day"].rolling(window=7).mean()
    )
    fig = px.line(
        df_news_per_day,
        x="date",
        y=["news_per_day", "moving_avg"],
        title="Moving Average of News Articles",
        labels={"date": "Date", "value": "Number of News Articles"},
    )
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    # Heatmap
    st.subheader("Heatmap of News Articles by Day and Month")
    df_news_per_day["day"] = df_news_per_day["date"].dt.day
    df_news_per_day["month"] = df_news_per_day["date"].dt.month
    heatmap_data = df_news_per_day.pivot_table(
        index="day", columns="month", values="news_per_day", aggfunc="sum"
    )
    fig = px.imshow(
        heatmap_data,
        color_continuous_scale="Viridis",
        title="Heatmap of News Articles by Day and Month",
    )
    st.plotly_chart(fig)

    # Box Plot
    st.subheader("Box Plot of News Articles")
    fig = px.box(
        df_news_per_day, y="news_per_day", title="Box Plot of Number of News Articles"
    )
    st.plotly_chart(fig)
