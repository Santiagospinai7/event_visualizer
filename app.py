import re
import json
import base64
import streamlit as st
from pytz import timezone
from datetime import datetime

hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load JSON data
with open("response.json", "r") as file:
    data = json.load(file)

# Load Bootstrap CSS and JS
st.markdown("""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
""", unsafe_allow_html=True)

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
    return encoded

# Load logo
logo_path = "assets/Epic_Games_logo.png"  # Replace with your local path
logo_base64 = get_image_base64(logo_path)

# Navbar with Bootstrap
st.markdown(f"""
    <style>
        .custom-navbar {{
            background-color: #1B1B23 !important; /* Custom background color */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Shadow for the navbar */
        }}

        /* Add margin to the logo */
        .navbar-brand img {{
            margin-right: 10px; /* Small margin to the right of the logo */
        }}
    </style>

    <!-- Bootstrap Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark custom-navbar fixed-top">
        <!-- Logo -->
        <a class="navbar-brand" href="#">
            <img src="data:image/png;base64,{logo_base64}" height="40" alt="Epic Games Logo">
        </a>
        <!-- Title centered -->
        <div class="mx-auto">
            <span class="navbar-text" style="color: white; font-size: 1.5em; font-weight: bold;">
                Event Windows Visualizer
            </span>
        </div>
    </nav>

    <!-- Margin to push content below navbar -->
    <div style="margin-top: 80px;"></div>
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

# Dropdown for selecting a tournament
selected_tournament = st.selectbox("Select Tournament", tournament_names)

# Toggle for UTC/Region Time
show_region_time = st.checkbox("Show Region Time Instead of UTC", value=False)

# Time Conversion Function
def convert_time_to_region(utc_time, region):
    region_mapping = {
        "ASIA": "Asia/Tokyo", "BR": "America/Sao_Paulo",
        "EU": "Europe/Berlin", "ME": "Asia/Dubai",
        "NAC": "America/New_York", "NAW": "America/Los_Angeles",
        "OCE": "Australia/Sydney"
    }
    try:
        utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone("UTC"))
        return utc_dt.astimezone(timezone(region_mapping.get(region, "UTC"))).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
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

for region in region_list:
    st.markdown("<div class='col-md-4 mb-4'>", unsafe_allow_html=True)
    st.markdown(f"<h5 class='text-center'>{region}</h5>", unsafe_allow_html=True)
    
    if region in events_by_region and events_by_region[region]:
        for window in events_by_region[region]:
            parsed_event = parse_event_id(window["eventWindowId"])
            round_name = parsed_event["event_window"]
            start_time = window['beginTime']
            end_time = window['endTime']
            if show_region_time:
                start_time = convert_time_to_region(window['beginTime'], region)
                end_time = convert_time_to_region(window['endTime'], region)
            
            # Bootstrap Card
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

st.markdown("</div></div>", unsafe_allow_html=True)