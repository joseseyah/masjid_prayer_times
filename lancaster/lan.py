import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'JanPrayerTimes.xlsx - Sheet1.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the CSV structure
df.columns = [
    "day",
    "fajr",
    "fajr_jamah",
    "sunrise",
    "dhuhr",
    "dhuhr_jamah",
    "asr_s",
    "asr_h",
    "asr_jamah",
    "maghrib",
    "isha",
    "isha_jamah"
]

# Function to format time in 24-hour format
def format_time_24h(value):
    try:
        return datetime.strptime(value, "%H:%M").strftime("%H:%M")
    except ValueError:
        try:
            return datetime.strptime(value, "%I:%M").strftime("%H:%M")
        except ValueError:
            return None  # Return None for invalid or missing times

# Fill gaps with values from the row above
df.fillna(method='ffill', inplace=True)

# Reformat the data into the desired structure
result = []
start_date = datetime(2025, 1, 1)  # Starting date for January 2025

for index, row in df.iterrows():
    day_offset = index  # Index corresponds to the day offset
    d_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

    entry = {
        "d_date": d_date,
        "fajr_begins": format_time_24h(row["fajr"]),
        "fajr_jamah": format_time_24h(row["fajr_jamah"]),
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["dhuhr"]),
        "zuhr_jamah": format_time_24h(row["dhuhr_jamah"]),
        "asr_mithl_1": format_time_24h(row["asr_s"]),
        "asr_mithl_2": format_time_24h(row["asr_h"]),
        "asr_jamah": format_time_24h(row["asr_jamah"]),
        "maghrib_begins": format_time_24h(row["maghrib"]),
        "maghrib_jamah": format_time_24h(row["maghrib"]),
        "isha_begins": format_time_24h(row["isha"]),
        "isha_jamah": format_time_24h(row["isha_jamah"]),
        "hijri_date": "0",  # Default value
        "is_ramadan": "0"  # Default value
    }
    result.append(entry)

# Save JSON output directly as a list to a file
output_file = 'lancaster_prayer_times.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
