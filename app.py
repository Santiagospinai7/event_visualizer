import streamlit as st
from components.navbar import render_navbar
from utils.load_bootstrap_and_js import load_bootstrap_and_js
from utils.hide_streamlit_menu import hide_streamlit_menu
from utils.data_utils import load_data, filter_events
from components.tournament_selector import render_tournament_selector
from components.toggle_buttons import render_toggle_buttons
from components.events_cards import render_events

# Hide Streamlit Menu
hide_streamlit_menu()

# Load Bootstrap CSS and JS
load_bootstrap_and_js()

# Load CSS
st.markdown("<link rel='stylesheet' href='./styles/style.css'>", unsafe_allow_html=True)

# Load JSON data
data = load_data("response.json")
filtered_events = filter_events(data)

# Render navbar
render_navbar()

# Estado de Región Time
if "region_time" not in st.session_state:
    st.session_state["region_time"] = False


# Estado para mostrar UTC o Region Time
if "region_time" not in st.session_state:
    st.session_state["region_time"] = False

# Selector de Torneos
selected_tournament = render_tournament_selector(filtered_events)

# Botones Toggle
show_region_time = render_toggle_buttons()

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
# Agrupar eventos por región
events_by_region = {}
for event in selected_events:
    for region in event.get("regions", []):
        if region not in events_by_region:
            events_by_region[region] = []
        events_by_region[region].extend(event.get("eventWindows", []))

# Mostrar eventos
if selected_tournament != "Choose Tournament":
    st.markdown(f"<h4 style='text-align:center'>Tournament: {selected_tournament}</h4>", unsafe_allow_html=True)
    render_events(events_by_region, show_region_time)
else:
    st.markdown("<p style='text-align:center'>No Tournament Selected</p>", unsafe_allow_html=True)