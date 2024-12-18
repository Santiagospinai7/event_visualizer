import streamlit as st
import re

def render_tournament_selector(filtered_events):
    # Extract unique tournament names
    tournament_names = list(set(re.sub(r"epicgames_S33_", "", event["eventId"]).rsplit("_", 1)[0]
                                for event in filtered_events))

    # Estado para mostrar UTC o Region Time
    if "region_time" not in st.session_state:
        st.session_state["region_time"] = False

    # CSS para el contenedor combinado
    st.markdown("""
        <style>
            .filter-container {
                background-color: #262636;
                padding: 0px;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                align-items: center;
                justify-content: center;
                max-width: 850px;
                margin: 0px auto 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            .toggle-container {
                display: flex;
                justify-content: center;
                gap: 10px;
            }
            .toggle-button {
                padding: 5px 20px;
                border-radius: 8px;
                background-color: #1E1E2E;
                color: white;
                font-weight: bold;
                border: 2px solid transparent;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .toggle-button.active {
                border-color: #00E7D5;
                box-shadow: 0 0 10px rgba(0, 231, 213, 0.7);
            }
            .toggle-button:hover {
                background-color: #00E7D5;
                color: black;
            }
            .select-box {
                width: 100%;
                max-width: 400px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Contenedor combinado
    st.markdown("""
        
        <div style="text-align: center;">
            <label style="color: white; font-size: 1.2em; font-weight: bold;">Select Tournament:</label>
        </div>
        
    """.format(
        ), unsafe_allow_html=True)

    # Actualizar estado usando query params
    query_params = st.query_params
    if "region_time" in query_params:
        st.session_state["region_time"] = query_params["region_time"] == "false"

    # Mostrar el torneo seleccionado y el modo de tiempo
    selected_tournament = st.selectbox("", ["Choose Tournament"] + tournament_names, index=0)

    return selected_tournament