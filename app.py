import json 
import re 
import streamlit as st

current_season = 's33'

with open(r'C:\Users\alejandro_castano1\Documents\FN\json_templating\response.json', 'r') as file:
    content = file.read()
    data = json.loads(content)

filtered_events = [elem for elem in data if current_season in elem['eventId'].lower()]

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