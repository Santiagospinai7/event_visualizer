from datetime import datetime
import pytz

def convert_time_to_region(utc_time, region):
    region_mapping = {
        "ASIA": "Asia/Tokyo", 
        "BR": "America/Sao_Paulo",
        "EU": "Europe/Berlin", 
        "ME": "Asia/Dubai",
        "NAC": "America/New_York", 
        "NAW": "America/Los_Angeles",
        "OCE": "Australia/Sydney"
    }
    try:
        # Validar formato de tiempo
        if not utc_time:
            return "Invalid Time"
        
        # Parsear el tiempo UTC
        utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
        
        # Convertir a la zona horaria de la región
        target_timezone = pytz.timezone(region_mapping.get(region, "UTC"))
        return utc_dt.astimezone(target_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    except (ValueError, KeyError):
        return "Invalid Time"