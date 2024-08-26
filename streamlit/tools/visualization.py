import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_timeline import st_timeline

## page for visualization of the data
st.markdown("## Use Case of News API")
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Data")
    """
    **1.** Monitoreo en tiempo real de Restricciones de viaje"""
    """
    **2.** Analisi de precepcion publica y sentimientos en Destinos Turisticos
    **3.** Sistema de alerta temprana para cancelaciones masivas
    """

with col2:
    st.write("Unlock test")    

## Tabs
tab1, tab2 = st.tabs(["Maps", "Graph"])
with tab1:
    st.markdown("### Maps")
    import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
## page for visualization of the data
st.markdown("## Visualization")

chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
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
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
with tab2:
    st.markdown("### Graph")

