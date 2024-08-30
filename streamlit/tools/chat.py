import streamlit as st
import boto3
import json
import uuid
import logging
import os
from dotenv import load_dotenv
import time

from streamlit.delta_generator import DeltaGenerator

# Cargar las variables de entorno
load_dotenv()

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

agent_id = "VNSFCLRGBB"
agent_alias_id = "TSTALIASID"

# Configurar el logger
logging.basicConfig(
    format="[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Crear el cliente de Bedrock Agent Runtime
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

    # Invocar la API del agente
    agentResponse = bedrock_agent_runtime_client.invoke_agent(
        inputText=inputText,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=enable_trace,
        endSession=end_session,
    )

    event_stream = agentResponse["completion"]
    try:
        for event in event_stream:
            if "chunk" in event:
                data = event["chunk"]["bytes"]
                yield data.decode("utf8")  # Generar cada fragmento de datos
            elif "trace" in event:
                logger.info(json.dumps(event["trace"], indent=2))
            else:
                raise Exception("Unexpected event.", event)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        yield f"Error: {e}"


# Configuración de la aplicación


# Inicializa la lista de mensajes y estado de sugerencias en el estado de sesión si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggestion_selected" not in st.session_state:
    st.session_state.suggestion_selected = False

# Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


st.markdown("#### Risk Chat")


# Captura la entrada del usuario
user_input = st.chat_input("What is up?")
# Mostrar sugerencias si no se ha seleccionado una

if not st.session_state.suggestion_selected:
    suggestion_box: DeltaGenerator = st.empty()
    # Lista de sugerencias
    suggested_prompts = [
        "Monitor travel restrictions for Brazil related to monkeypox outbreaks and provide information on any potential risks and potential impact in insurance policies.",
        "Analyze public perception regarding tourism in Colombia, based on recent news articles, and provide insights into potential risks that might affect travel insurance.",
        "Validate the credibility of the statement: 'The monkeypox outbreak in Venezuela has led to a 50% increase in travel insurance premiums.'",
        "Search for news articles about the impact of monkeypox on international travel and provide a summary of the most relevant articles.",
    ]
    with suggestion_box.container():
        st.markdown("#### Try these prompts...")
        for prompt in suggested_prompts:
            if st.button(prompt, key=prompt):
                user_input = prompt
                # st.session_state.messages.append({"role": "user", "content": user_input})
                # st.session_state.suggestion_selected = True

def stream_data(response: str):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.1)


# Procesar la entrada del usuario
if user_input:
    suggestion_box.empty()
    # Añadir el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Genera y muestra la respuesta del asistente en tiempo real
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Placeholder para la respuesta

        # Mostrar spinner y texto de carga
        with st.spinner("Thinking..."):
            loading_text = st.empty()
            loading_text.markdown(
                "<p style='color: #888888;'> <b>Unlock Bedrock Agent</b> is querying <b>Pinecone</b> and <b>Bing Api</b> for accurate results...</p>",
                unsafe_allow_html=True,
            )

            # Llama a la función invokeAgent para obtener el generador
            full_response = ""
            for chunk in invokeAgent(user_input):
                full_response += chunk
                # Opcionalmente, actualizar el estado con la respuesta parcial
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response})

            # Limpiar el texto de carga después de recibir la respuesta completa
            loading_text.empty()
        response_placeholder.write_stream(stream_data(full_response))


