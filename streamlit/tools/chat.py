import streamlit as st
st.markdown("## Risk Chat")
#from anthropic import AnthropicBedrock

#client = AnthropicBedrock(
    # Authenticate by either providing the keys below or use the default AWS credential providers, such as
    # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
#    aws_access_key="<access key>",
#    aws_secret_key="<secret key>",
    # Temporary credentials can be used with aws_session_token.
    # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
#    aws_session_token="<session_token>",
    # aws_region changes the aws region to which the request is made. By default, we read AWS_REGION,
    # and if that's not present, we default to us-east-1. Note that we do not read ~/.aws/config for the region.
#    aws_region="us-west-2",
#)
#
#message = client.messages.create(
#    model="anthropic.claude-3-5-sonnet-20240620-v1:0",
#    max_tokens=256,
#    messages=[{"role": "user", "content": "Hello, world"}]
#)
#print(message.content)



#if "messages" not in st.session_state:
#    st.session_state.messages = []

#for message in st.session_state.messages:
#    with st.chat_message(message["role"]):
#        st.markdown(message["content"])

#if prompt := st.chat_input("What is up?"):
#    st.session_state.messages.append({"role": "user", "content": prompt})
#    with st.chat_message("user"):
#        st.markdown(prompt)
#
#    with st.chat_message("assistant"):
#        stream = client.chat.completions.create(
#            model=st.session_state["openai_model"],
#            messages=[
#                {"role": m["role"], "content": m["content"]}
#                for m in st.session_state.messages
#            ],
#            stream=True,
#        )
#        response = st.write_stream(stream)
#    st.session_state.messages.append({"role": "assistant", "content": response})

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
import random
import time
# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
