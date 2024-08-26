def lambda_handler(event, context):
    agent = event["agent"]
    actionGroup = event["actionGroup"]
    function = event["function"]
    parameters = event.get("parameters", [])
    responseBody = {"TEXT": {"body": "Error, no function was called"}}

    if function == "monitor_travel_restrictions":
        region = None
        alert_threshold = None
        coverage_type = None

        for param in parameters:
            if param["name"] == "region":
                region = param["value"]
            if param["name"] == "alert_threshold":
                alert_threshold = param["value"]
            if param["name"] == "coverage_type":
                coverage_type = param["value"]

        if not region:
            raise Exception("Missing mandatory parameter: region")
        if not alert_threshold:
            raise Exception("Missing mandatory parameter: alert_threshold")

        changes_summary = monitor_travel_restrictions(
            region, alert_threshold, coverage_type
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
        news_id = None
        source_criteria = None

        for param in parameters:
            if param["name"] == "news_id":
                news_id = param["value"]
            if param["name"] == "source_criteria":
                source_criteria = param["value"]

        if not news_id:
            raise Exception("Missing mandatory parameter: news_id")

        validation_report = validate_news_sources(news_id, source_criteria)
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
    # Placeholder return value
    return (
        f"Travel restrictions for region {region} are as follows: [link1, link2, link3]"
    )


def analyze_public_sentiment(destination, time_frame):
    # Placeholder return value
    return f"Positive sentiment score of 75 for destination {destination} during {time_frame}, links of related news articles: [link1, link2, link3]"


def validate_news_sources(region, topic):
    # Placeholder return value
    return f"News sources validated for region {region} and topic {topic} links related to the topic: [link1, link2, link3]"
