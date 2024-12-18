import streamlit as st
from streamlit.components.v1 import html
from utils.time_utils import convert_time_to_region

# Function to parse event details
def parse_event_id(event_id):
    parts = event_id.split("_")
    return {
        "season": parts[0],
        "tournament": "_".join(parts[1:-2]),
        "event_window": parts[-2],
        "region": parts[-1],
    }

# Main function to render events
def render_events(selected_events, show_region_time):
    regions = ["ASIA", "BR", "EU", "ME", "NAC", "NAW", "OCE"]
    events_by_region = {}

    # Organize events by region
    for event in selected_events:
        for region in event.get("regions", []):
            if region not in events_by_region:
                events_by_region[region] = []
            events_by_region[region].extend(event.get("eventWindows", []))

    # First Row: 3 Regions
    cols = st.columns(3)
    for i, region in enumerate(["ASIA", "BR", "EU"]):
        with cols[i]:
            render_region_card(region, events_by_region, show_region_time)

    # Second Row: 3 Regions
    cols = st.columns(3)
    for i, region in enumerate(["ME", "NAC", "NAW"]):
        with cols[i]:
            render_region_card(region, events_by_region, show_region_time)

    # Third Row: 1 Region centered
    col = st.columns([1, 2, 1])[1]
    with col:
        render_region_card("OCE", events_by_region, show_region_time)

# Function to render a region card
def render_region_card(region, events_by_region, show_region_time):
    # Card Layout
    st.markdown(f"### 🌍 {region}")

    # Scrollable events container with fixed height using components.html
    if region in events_by_region and events_by_region[region]:
        events_html = ""
        for window in events_by_region[region]:
            parsed_event = parse_event_id(window["eventWindowId"])
            round_name = parsed_event["event_window"]
            begin_time = window.get("beginTime", "N/A")
            end_time = window.get("EndTime", "N/A")
            
            # Convert times
            start_time = convert_time_to_region(begin_time, region) if show_region_time else begin_time
            end_time = convert_time_to_region(end_time, region) if show_region_time else end_time

            events_html += f"""
                <div style='margin-bottom: 10px; color: white; font-size: 14px;'>
                    <strong>{round_name}</strong><br>
                    Start: {start_time}<br>
                    End: {end_time}
                </div>
            """

        # Scrollable container with fixed height
        html(f"""
            <div style='background-color: #1F1F2F; border-radius: 8px; padding: 10px; height: 200px; overflow-y: auto;'>  
              {events_html}
            </div>
        """, height=250, scrolling=False)
    else:
        st.write("No Events Available")