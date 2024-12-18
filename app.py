import re
import json
import streamlit as st
from pytz import timezone
from datetime import datetime

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

# Extract unique tournament names
tournament_names = list(set(re.sub(r"epicgames_S33_", "", event["eventId"]).rsplit("_", 1)[0]
                            for event in filtered_events))

# Streamlit App Title
st.title("Event Windows Visualizer")

# Tournament Dropdown
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
    
def parse_event_id(event_id):
    parts = event_id.split("_")  # Separar por "_"
    
    # Identificar las partes
    season = parts[0]  # Primera parte: "S33"
    region = parts[-1]  # Última parte: "BR", "EU", etc.
    event_window = parts[-2]  # Penúltima parte: "Week1Day1"
    
    # Todo lo que queda entre el season y el event_window es el nombre del torneo
    tournament = "_".join(parts[1:-2])  # Unir todo lo intermedio
    
    return {
        "season": season,
        "tournament": tournament,
        "event_window": event_window,
        "region": region
    }

# Filter events for selected tournament
selected_events = [event for event in filtered_events if selected_tournament in event["eventId"]]

# Group events by region
events_by_region = {}
for event in selected_events:
    for region in event.get("regions", []):
        if region not in events_by_region:
            events_by_region[region] = []
        events_by_region[region].extend(event.get("eventWindows", []))

# Create Grid Layout for Regions
region_list = ["ASIA", "BR", "EU", "ME", "NAC", "NAW", "OCE"]
cols = st.columns(7)

# Populate Each Column with Region Data
for i, region in enumerate(region_list):
    with cols[i]:
        st.subheader(region)
        if region in events_by_region and events_by_region[region]:
            for window in events_by_region[region]:
                parsed_events = [parse_event_id(window["eventWindowId"]) for event in filtered_events]
                round_name = parsed_events[0]["event_window"]
                start_time = window['beginTime']
                end_time = window['endTime']
                if show_region_time:
                    start_time = convert_time_to_region(window['beginTime'], region)
                    end_time = convert_time_to_region(window['endTime'], region)
                st.write(f"**Round:** {round_name}")
                st.write(f"Start: {start_time}")
                st.write(f"End: {end_time}")
        else:
            st.write("No Events Available")