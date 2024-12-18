import streamlit as st
from streamlit.components.v1 import html
from utils.time_utils import convert_time_to_region

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        * {
            font-family: 'Roboto', sans-serif;
        }

        /* Optional: Adjust font for specific elements */
        .stTextInput, .stSelectbox, .stButton {
            font-family: 'Roboto', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: bold;
            color: white;
        }

        body {
            font-family: 'Roboto', sans-serif;
            color: white;
            background-color: #1F1F2F;
        }

        .region-header {
            font-family: 'Roboto', sans-serif;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
        }

        .event-item {
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: white;
        }

    </style>
""", unsafe_allow_html=True)

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
    regions = [
        ["ASIA", "https://cdn-icons-png.flaticon.com/512/2072/2072187.png"],
        ["BR", "https://cdn-icons-png.flaticon.com/512/1477/1477945.png"],
        ["EU", "https://cdn-icons-png.flaticon.com/512/9098/9098339.png"],
        ["ME", "https://cdn-icons-png.flaticon.com/512/10170/10170613.png"],
        ["NAC", "https://cdn-icons-png.flaticon.com/512/7509/7509297.png"],
        ["NAW", "https://cdn-icons-png.flaticon.com/512/7509/7509297.png"],
        ["OCE", "https://cdn-icons-png.flaticon.com/512/6056/6056855.png"],
    ]
    events_by_region = {}

    # Organize events by region
    for event in selected_events:
        for region in event.get("regions", []):
            if region not in events_by_region:
                events_by_region[region] = []
            events_by_region[region].extend(event.get("eventWindows", []))

    # First Row: 3 Regions
    cols = st.columns(3)
    for i, region in enumerate(regions[:3]):  
        with cols[i]:
            render_region_card(region, events_by_region, show_region_time)

    # Second Row: 3 Regions
    cols = st.columns(3)
    for i, region in enumerate(regions[3:6]):  
        with cols[i]:
            render_region_card(region, events_by_region, show_region_time)

    # Third Row: 1 Region centered
    col = st.columns([1, 2, 1])[1]
    with col:
        render_region_card(regions[6], events_by_region, show_region_time)

# Function to render a region card
def render_region_card(region, events_by_region, show_region_time):
    region_name = region[0]
    region_icon = region[1]

    # Generate events HTML
    if region_name in events_by_region and events_by_region[region_name]:
        events_html = ""
        for window in events_by_region[region_name]:
            parsed_event = parse_event_id(window["eventWindowId"])
            round_name = parsed_event["event_window"]
            begin_time = window.get("beginTime", "N/A")
            end_time = window.get("endTime", "N/A")

            # Convert times
            start_time = convert_time_to_region(begin_time, region_name) if show_region_time else begin_time
            end_time = convert_time_to_region(end_time, region_name) if show_region_time else end_time

            events_html += f"""
              <div style='
                  margin-bottom: 10px;
                  background-color: #2E2E38;
                  border-radius: 8px;
                  color: white;
                  font-size: 14px;
                  text-align: left;
                  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.3);
                  padding: 10px;'>
                  <!-- Table Layout -->
                  <table style="width: 100%; border-collapse: collapse; color: white;">
                      <!-- Event Name Row -->
                      <tr>
                          <td style="font-weight: bold; color: #FFFFFF; padding: 5px; width: 20%; text-align: center;">{round_name}</td>
                      </tr>
                      <!-- Begin Time Row -->
                      <tr>
                          <td style="padding: 5px; width: 80%;">
                              <span style="color: #AAAAAA; font-weight: bold;">Begin Time:</span> <br/> {start_time}
                          </td>
                      </tr>
                      <!-- Total Row -->
                      <tr>
                          <td style="padding: 5px; width: 80%;">
                              <span style="color: #AAAAAA; font-weight: bold;">End Time:</span> <br/> {end_time}
                          </td>
                      </tr>
                  </table>
              </div>
          """

        # Combine everything in an HTML block
        html(f"""
            <div style='background-color: #1B1B23; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);'>
                <!-- Header Section -->
                <div style='background-color: #2E2E38; border-radius: 8px; margin-bottom:10px; padding-top: 10px; padding-bottom: 10px; margin-left: 50px; margin-right: 50px;'>
                    <img src="{region_icon}" width="50" style="display: block; margin: 0 auto;">
                    <div style='color: #FFFFFF; font-size: 1.2em; font-weight: bold; margin-top: 0px;'>{region_name}</div>
                </div>
                <!-- Scrollable Content -->
                <div style=' border-radius: 8px; padding: 10px; height: 180px; overflow-y: auto;'>
                    {events_html}
                </div>
            </div>
        """, height=300, scrolling=False)
    else:
        # No Events Case
        html(f"""
            <div style='background-color: #1B1B23; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);'>
                <!-- Header Section -->
                <div style='margin-bottom: 10px;'>
                    <img src="{region_icon}" width="50" style="display: block; margin: 0 auto;">
                    <div style='color: #FFFFFF; font-size: 1.2em; font-weight: bold; margin-top: 5px;'>{region_name}</div>
                </div>
                <!-- Empty Events -->
                <div style='background-color: #1B1B23; border-radius: 8px; padding: 10px; height: 180px; overflow-y: auto;'>
                    <p style='color: white;'>No Events Available</p>
                </div>
            </div>
        """, height=300, scrolling=False)