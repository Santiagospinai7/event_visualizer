import streamlit as st

def hide_streamlit_menu():
    st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        body {
            background-color: #0F0F14 !important; /* Fondo principal */
            color: white;
        }
        /* Eliminar márgenes extra de Streamlit */
        .st-emotion-cache-1n76uvr, .st-emotion-cache-uf99v8 {
            margin: 0 !important;
            padding: 0 !important;
            gap: 0 !important;
        }
        .st-emotion-cache-yw8pof {
            padding: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)
