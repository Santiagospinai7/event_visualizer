import streamlit as st

def load_bootstrap_and_js():
    st.markdown("""
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
      <style>
          /* Navbar personalizado */
          .custom-navbar {
              background-color: #1B1B23;
              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
              margin-bottom: 0; /* Sin margen inferior */
              padding: 5px 20px;
          }

          /* Ajustar el espacio del filtro */
          .filter-section {
              margin-top: -10px; /* Eliminar espacio con el navbar */
              background-color: #1B1B23;
              padding: 10px 20px;
              border-radius: 0;
              display: flex;
              justify-content: space-between;
              align-items: center;
              width: 100%;
          }

          /* Eliminar márgenes extra de Streamlit */
          .st-emotion-cache-1n76uvr, .st-emotion-cache-uf99v8 {
              margin: 0 !important;
              padding: 0 !important;
              gap: 0 !important;
          }

          /* Fix para todo el contenedor principal */
          .main-content {
              margin-top: 0 !important;
              padding-top: 0 !important;
          }

          /* Switch */
          .custom-control-label::before {
              border: 1px solid #FFFFFF;
          }

          .custom-switch input:checked + .custom-control-label::before {
              background-color: #00E7D5;
          }
      </style>
""", unsafe_allow_html=True)
