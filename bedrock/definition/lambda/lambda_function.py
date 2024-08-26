from bing import fetch_top_news


def lambda_handler(event, context):
    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    parameters = event.get("parameters", [])
    responseBody = {"TEXT": {"body": "Error, no function was called"}}

    if function == "monitor_travel_restrictions":
        region = None

        for param in parameters:
            if param["name"] == "region":
                region = param["value"]

        if not region:
            raise Exception("Missing mandatory parameter: region")

        changes_summary = monitor_travel_restrictions(
            region
        )
        responseBody = {"TEXT": {"body": changes_summary}}

    elif function == "analyze_public_sentiment":
        destination = None
        time_frame = None

        for param in parameters:
            if param["name"] == "destination":
                destination = param["value"]
            if param["name"] == "time_frame":
                time_frame = param["value"]

        if not destination:
            raise Exception("Missing mandatory parameter: destination")

        sentiment_score = analyze_public_sentiment(destination, time_frame)
        responseBody = {
            "TEXT": {
                "body": f"Sentiment score for destination {destination}: {sentiment_score}"
            }
        }

    elif function == "validate_news_sources":
        new = None

        for param in parameters:
            if param["name"] == "new":
                new = param["value"]

        if not new:
            raise Exception("Missing mandatory parameter: new")

        validation_report = validate_news_sources(new)
        responseBody = {"TEXT": {"body": validation_report}}

    action_response = {
        "actionGroup": actionGroup,
        "function": function,
        "functionResponse": {"responseBody": responseBody},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event["messageVersion"],
    }
    print("Response: {}".format(function_response))

    return function_response


def monitor_travel_restrictions(region):

    query = f"travel restrictions related to monkeypox for {region}"
    top_news = fetch_top_news(query, top_num=5)
    return f"Here are the top news articles: {top_news}"


def analyze_public_sentiment(destination, time_frame):
    query = f"perception towards {destination} about monkeypox in the past {time_frame}"
    top_news = fetch_top_news(query, top_num=5)
    return f"Here are the top news articles: {top_news}"


def validate_news_sources(new):
    query = f"is it true that {new}"
    top_news = fetch_top_news(query, top_num=5)
    return f"Here are the top news articles: {top_news}"
