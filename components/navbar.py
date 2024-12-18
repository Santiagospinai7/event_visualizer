import streamlit as st
from utils.data_utils import get_image_base64

def render_navbar():
    logo_base64 = get_image_base64("assets/Epic_Games_logo.png")  # Ajustar la ruta local
    st.markdown(f"""
        <nav class="navbar navbar-expand-lg custom-navbar fixed-top">
            <a class="navbar-brand" href="#">
                <img src="data:image/png;base64,{logo_base64}" height="40" alt="Epic Games Logo">
            </a>
            <div class="mx-auto">
                <span class="navbar-text" style="color: white; font-size: 1.5em; font-weight: bold;">
                    Event Windows Visualizer
                </span>
            </div>
        </nav>
    """, unsafe_allow_html=True)