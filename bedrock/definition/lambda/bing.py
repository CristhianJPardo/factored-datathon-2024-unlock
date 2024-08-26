import requests
import os

api_key = os.getenv("BING_API_KEY")


def fetch_top_news(query, top_num=10):
    # Define the endpoint and headers
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {
        "q": query,
        "count": top_num,  # Number of top results to fetch
        "textFormat": "Raw",  # To get the full content
    }

    # Make the request to Bing News API
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for unsuccessful requests

    # Parse the JSON response
    data = response.json()

    # Extract and return the top news articles' titles, content, and URLs
    articles = data.get("value", [])
    top_news = []
    for article in articles:
        title = article.get("name", "No title")
        content = article.get("description", "No content")
        url = article.get("url", "No URL")
        top_news.append({"title": title, "content": content, "url": url})

    return top_news
