import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'January_2025_Prayer_Times_Dublin.xlsx - Sheet1 copy.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the input CSV structure
df.columns = [
    "day", "date", "fajr", "sunrise", "dhuhr",
    "asr", "maghrib", "isha"
]

# Function to convert times to 24-hour format
def format_time_24h(value):
    try:
        # Parse as 12-hour format, assuming all times are in the morning unless specified otherwise
        time_obj = datetime.strptime(value.strip(), "%H:%M") if ":" in value else None
        return time_obj.strftime("%H:%M") if time_obj else ""
    except ValueError:
        return ""  # Return empty string for invalid times

# Reformat the data into the desired structure
result = []
start_date = datetime(2025, 1, 1)  # Assuming the year 2025

for index, row in df.iterrows():
    try:
        day_offset = int(row["date"]) - 1
        d_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
    except ValueError:
        continue  # Skip rows with invalid date values

    entry = {
        "d_date": d_date,
        "fajr_begins": format_time_24h(row["fajr"]),
        "fajr_jamah": "",  # Leave empty
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["dhuhr"]),
        "zuhr_jamah": "",  # Leave empty
        "asr_mithl_1": format_time_24h(row["asr"]),
        "asr_mithl_2": format_time_24h(row["asr"]),  # Same as asr
        "asr_jamah": "",  # Leave empty
        "maghrib_begins": format_time_24h(row["maghrib"]),
        "maghrib_jamah": "",  # Leave empty
        "isha_begins": format_time_24h(row["isha"]),
        "isha_jamah": "",  # Leave empty
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)

# Save JSON output to a file
output_file = 'dublin_prayer_times.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
