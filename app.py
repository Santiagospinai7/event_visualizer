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

# Region Time Toggle
if "region_time" not in st.session_state:
    st.session_state["region_time"] = False

selected_tournament = render_tournament_selector(filtered_events)

show_region_time = render_toggle_buttons()

selected_events = [event for event in filtered_events if selected_tournament in event["eventId"]]

# Display Events
if selected_tournament != "Choose Tournament":
    render_events(selected_events, show_region_time)
else:
    st.markdown("<p style='text-align:center'>No Tournament Selected</p>", unsafe_allow_html=True)