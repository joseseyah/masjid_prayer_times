import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'Prayer_Times_January_2025.xlsx - Sheet1.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the CSV structure
df.columns = [
    "no", "day", "fajr_begins", "sunrise", "zuhr_begins",
    "asr_mithl_1", "maghrib_begins", "isha_begins"
]

# Function to convert times to 24-hour format
def format_time_24h(value, is_pm=False):
    try:
        time_obj = datetime.strptime(value, "%I:%M")  # Parse in 12-hour format
        if is_pm and time_obj.hour < 12:
            time_obj = time_obj.replace(hour=time_obj.hour + 12)  # Add 12 hours for PM
        return time_obj.strftime("%H:%M")  # Convert to 24-hour format
    except ValueError:
        return ""  # Return empty string for invalid times

# Reformat the data into the desired structure
result = []
start_date = datetime(2025, 1, 1)  # Starting date for January 2025

for index, row in df.iterrows():
    day_offset = int(row["no"]) - 1
    d_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

    entry = {
        "d_date": d_date,
        "fajr_begins": format_time_24h(row["fajr_begins"]),
        "fajr_jamah": "06:45",  # Hardcoded value
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["zuhr_begins"], is_pm=True),
        "zuhr_jamah": "13:00",  # Hardcoded value
        "asr_mithl_1": format_time_24h(row["asr_mithl_1"], is_pm=True),
        "asr_mithl_2": format_time_24h(row["asr_mithl_1"], is_pm=True),  # Same as asr_mithl_1
        "asr_jamah": "14:30",  # Hardcoded value
        "maghrib_begins": format_time_24h(row["maghrib_begins"], is_pm=True),
        "maghrib_jamah": "16:45",  # Hardcoded value
        "isha_begins": format_time_24h(row["isha_begins"], is_pm=True),
        "isha_jamah": "18:30",  # Hardcoded value
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)

# Save JSON output directly as a list to a file
output_file = 'duisoc_prayer_times_jan.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
