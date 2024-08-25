import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_timeline import st_timeline
st.set_page_config(layout="wide")
## Load the data from a dataframe
df = pd.read_csv("static/data.csv")
df = df.head(10)
chart_data= df.rename(columns={"actiongeo_lat": "LAT", "actiongeo_long": "LON"})


# Función para crear el formato deseado
def create_dict(row):
    # Extraer y formatear la fecha
    sqldate = str(row['sqldate'])
    formatted_date = f"{sqldate[0:4]}-{sqldate[4:6]}-{sqldate[6:8]}"
    
    # Crear el diccionario
    return {
        "id": row['globaleventid'],  # El id es un entero
        "content": formatted_date
    }

result_list = df.apply(create_dict, axis=1).tolist()

## page for visualization of the data
st.markdown("## Use Case of News API")
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Data")
    """
    **1.** Monitoreo en tiempo real de Restricciones de viaje"""
    timeline = st_timeline(result_list, groups=[], options={}, height="300px")
    st.write(timeline)
    """
    **2.** Analisi de precepcion publica y sentimientos en Destinos Turisticos
    **3.** Sistema de alerta temprana para cancelaciones masivas
    """

with col2:
    st.write("Hola")    
## Tabs
tab1, tab2 = st.tabs(["Maps", "Graph"])
with tab1:
    st.markdown("### Maps")
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
                    get_position="[LON, LAT]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=chart_data,
                    get_position="[LON, LAT]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )
    st.divider()
    st.map(chart_data)
with tab2:
    st.markdown("### Graph")
    st.area_chart(chart_data)
    st.divider()
    st.line_chart(chart_data)

