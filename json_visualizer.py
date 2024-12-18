import pandas as pd
import json

# Cargar el JSON
with open("filtered_events.json", "r") as file:
    data = json.load(file)

# Procesar los datos
rows = []
for event in data:
    tournament = event['eventId']
    for region in event.get('regions', []):
        for window in event.get('eventWindows', []):
            rows.append({
                "Torneo": tournament,
                "Region": region,
                "Round": window.get('round', "N/A"),
                "Start": window.get('beginTime'),
                "End": window.get('endTime')
            })

# Mostrar como tabla
df = pd.DataFrame(rows)
print(df)