import json
import base64

def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def filter_events(data):
    # Filter tournaments for s33 season
    current_season = "s33"
    excluded_events = ["PerformanceEvaluation", "FNCSMajor1"]

    filtered_events = [
        event for event in data
        if current_season in event['eventId'].lower()
        and not any(excluded in event['eventId'] for excluded in excluded_events)
    ]

    return filtered_events

def get_image_base64(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
    return encoded

def parse_event_id(event_id):
    parts = event_id.split("_")
    season = parts[0]
    region = parts[-1]
    event_window = parts[-2]
    tournament = "_".join(parts[1:-2])
    return {"season": season, "tournament": tournament, "event_window": event_window, "region": region}