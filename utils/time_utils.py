import pendulum

def convert_time_to_region(utc_time, region):
    """
    Convert UTC time to the target region's local time using Pendulum.

    Args:
        utc_time (str): Time in UTC format (e.g., "2024-12-11T09:00:00Z").
        region (str): Target region for conversion.

    Returns:
        str: Formatted local time for the region, or 'Invalid Time' on failure.
    """
    # Region to timezone mapping
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
        # Parse UTC time using Pendulum
        utc_dt = pendulum.parse(utc_time, tz="UTC")
        
        # Fetch target timezone
        target_timezone = region_mapping.get(region, "UTC")
        
        # Convert UTC to target timezone
        local_dt = utc_dt.in_timezone(target_timezone)
        
        # Return formatted time
        return local_dt.format("YYYY-MM-DD HH:mm:ss")
    
    except Exception:
        return "Invalid Time"