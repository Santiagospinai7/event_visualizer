import json
import streamlit as st
# import pandas as pd
# from pytz import timezone
# from datetime import datetime

# Load JSON data
with open("response.json", "r") as file:
    data = json.load(file)

# Filter tournaments for s33 season
current_season = "s33"
excluded_events = ["PerformanceEvaluation", "FNCSMajor1"]

filtered_events = [
    event for event in data
    if current_season in event['eventId'].lower()
    and not any(excluded in event['eventId'] for excluded in excluded_events)
]

# generate a JSON with the filtered events data and if exists a file with the same name, it will be overwritten
with open("filtered_events.json", "w") as file:
    json.dump(filtered_events, file)

grouped_events = {}
for event in filtered_events:
    event_group = event.get('eventGroup', 'No Group')  # Default to 'No Group' if eventGroup not found
    if event_group not in grouped_events:
        grouped_events[event_group] = []
    grouped_events[event_group].append(event)

# Add Streamlit title and dropdown
st.title("Event Group Viewer")

# Create dropdown for event groups
selected_group = st.selectbox(
    "Select an Event Group",
    options=list(grouped_events.keys())
)

# Display the events for selected group
if selected_group:
    st.subheader(f"Events in {selected_group}")
    for event in grouped_events[selected_group]:
        # Create an expander for each event
        with st.expander(f"Event ID: {event['eventId']}"):
            # Pretty print the JSON
            st.json(event)


## Por Grupo de evento visualizar las regiones y los horarios de las ventanas de los eventos. 