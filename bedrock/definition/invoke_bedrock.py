import boto3
import json
import uuid

# import pprint
import logging
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

agent_id = "VNSFCLRGBB"
agent_alias_id = "TSTALIASID"


# setting logger
logging.basicConfig(
    format="[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bedrock_agent_runtime_client = boto3.client(
    "bedrock-agent-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,
)


def invokeAgent(inputText: str):

    session_id: str = str(uuid.uuid1())
    enable_trace: bool = False
    end_session: bool = False

    # invoke the agent API
    agentResponse = bedrock_agent_runtime_client.invoke_agent(
        inputText=inputText,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=enable_trace,
        endSession=end_session,
    )
    #
    # logger.info(pprint.pprint(agentResponse))

    event_stream = agentResponse["completion"]
    try:
        for event in event_stream:
            if "chunk" in event:
                data = event["chunk"]["bytes"]
                # logger.info(f"Final answer ->\n{data.decode('utf8')}")
                agent_answer = data.decode("utf8")
                end_event_received = True
                # End event indicates that the request finished successfully
            elif "trace" in event:
                logger.info(json.dumps(event["trace"], indent=2))
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)

    # And here is the response if you just want to see agent's reply
    return agent_answer
