import re
import pytz  # Importar la librería para zonas
import json
import base64
import streamlit as st
from datetime import datetime
# Ocultar menú Streamlit
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
    </style>
""", unsafe_allow_html=True)

# Load JSON data
with open("response.json", "r") as file:
    data = json.load(file)

# Load Bootstrap CSS and JS
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

# Custom CSS para botones
st.markdown("""
    <style>
        .toggle-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        .toggle-button {
            padding: 10px 20px;
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
    </style>
""", unsafe_allow_html=True)

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
    return encoded

# Navbar con Bootstrap
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

# Filter tournaments for s33 season
current_season = "s33"
excluded_events = ["PerformanceEvaluation", "FNCSMajor1"]

filtered_events = [
    event for event in data
    if current_season in event['eventId'].lower()
    and not any(excluded in event['eventId'] for excluded in excluded_events)
]

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

# Toggle buttons que actualizan el estado directamente
col1, col2 = st.columns(2)
with col1:
    if st.button("UTC", key="utc_button"):
        st.session_state["region_time"] = False  # Cambia el estado a UTC
with col2:
    if st.button("Region Time", key="region_button"):
        st.session_state["region_time"] = True  # Cambia el estado a Region Time

if selected_tournament != "Choose Tournament":
    st.markdown(f"""
        <div style="color: white; text-align: center; margin-top: 0px; font-size: 1.0em;">
            Selected Tournament: <strong>{selected_tournament}</strong><br>
            Time Mode: <strong>{"Region Time" if st.session_state["region_time"] else "UTC"}</strong>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div style="color: white; text-align: center; margin-top: 0px; font-size: 1.0em;">
            Selected Tournament: <strong>No Tournament Selected</strong><br>
            Time Mode: <strong>{"Region Time" if st.session_state["region_time"] else "UTC"}</strong>
        </div>
    """, unsafe_allow_html=True)

    
# Streamlit Logic for the Switch
show_region_time = st.session_state["region_time"]

# Time Conversion Function
def convert_time_to_region(utc_time, region):
    region_mapping = {
        "ASIA": "Asia/Tokyo", 
        "BR": "America/Sao_Paulo",
        "EU": "Europe/Berlin", 
        "ME": "Asia/Dubai",
        "NAC": "America/New_York", 
        "NAW": "America/Los_Angeles",
        "OCE": "Australia/Sydney"
    }
    try:
        # Validar formato de tiempo
        if not utc_time:
            return "Invalid Time"
        
        # Parsear el tiempo UTC
        utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
        
        # Convertir a la zona horaria de la región
        target_timezone = pytz.timezone(region_mapping.get(region, "UTC"))
        return utc_dt.astimezone(target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    except (ValueError, KeyError):
        return "Invalid Time"

# Parse Event ID Function
def parse_event_id(event_id):
    parts = event_id.split("_")
    season = parts[0]
    region = parts[-1]
    event_window = parts[-2]
    tournament = "_".join(parts[1:-2])
    return {"season": season, "tournament": tournament, "event_window": event_window, "region": region}

# Filter events for selected tournament
selected_events = [event for event in filtered_events if selected_tournament in event["eventId"]]

# Group events by region
events_by_region = {}
for event in selected_events:
    for region in event.get("regions", []): 
        if region not in events_by_region:
            events_by_region[region] = []
        events_by_region[region].extend(event.get("eventWindows", []))

# Regions to display
region_list = ["ASIA", "BR", "EU", "ME", "NAC", "NAW", "OCE"]

# Display Cards for Each Region
st.markdown("<div class='container'><div class='row'>", unsafe_allow_html=True)

# Mostrar eventos por región
for region in region_list:
    st.markdown("<div class='col-md-4 mb-4'>", unsafe_allow_html=True)
    st.markdown(f"<h5 class='text-center'>{region}</h5>", unsafe_allow_html=True)

    if region in events_by_region and events_by_region[region]:
        for window in events_by_region[region]:
            # Validar existencia de claves
            begin_time = window.get('beginTime', None)
            end_time = window.get('endTime', None)

            parsed_event = parse_event_id(window["eventWindowId"])
            round_name = parsed_event["event_window"]

            # Convertir a región o mantener UTC
            start_time = convert_time_to_region(begin_time, region) if show_region_time else begin_time
            end_time = convert_time_to_region(end_time, region) if show_region_time else end_time

            # Mostrar tarjeta
            st.markdown(f"""
                <div class="card bg-dark text-white">
                    <div class="card-body text-center">
                        <h6 class="card-title">{round_name}</h6>
                        <p class="card-text">
                            <strong>Start:</strong> {start_time}<br>
                            <strong>End:</strong> {end_time}
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="card bg-secondary text-white">
                <div class="card-body text-center">
                    <p>No Events Available</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)