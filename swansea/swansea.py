import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'Swansea_Prayer_Times_January.xlsx - Sheet1.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the input CSV structure
df.columns = [
    "date", "fajr_begins", "fajr_jamah", "sunrise", "zuhr_begins",
    "zuhr_jamah", "asr_begins", "asr_jamah", "maghrib_begins",
    "maghrib_jamah", "isha_begins", "isha_jamah"
]

# Function to convert times to 24-hour format
def format_time_24h(value):
    try:
        time_obj = datetime.strptime(value, "%H:%M")  # Parse in 24-hour format
        return time_obj.strftime("%H:%M")  # Convert to 24-hour format
    except ValueError:
        return ""  # Return empty string for invalid times

# Reformat the data into the desired structure
result = []

for index, row in df.iterrows():
    # Convert the date to the desired format
    try:
        d_date = datetime.strptime(row["date"].split(' ')[0], "%d-%b").strftime("2025-%m-%d")
    except ValueError:
        continue  # Skip rows with invalid date formats

    entry = {
        "d_date": d_date,
        "fajr_begins": format_time_24h(row["fajr_begins"]),
        "fajr_jamah": format_time_24h(row["fajr_jamah"]),
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["zuhr_begins"]),
        "zuhr_jamah": format_time_24h(row["zuhr_jamah"]),
        "asr_mithl_1": format_time_24h(row["asr_begins"]),
        "asr_mithl_2": format_time_24h(row["asr_begins"]),
        "asr_jamah": format_time_24h(row["asr_jamah"]),
        "maghrib_begins": format_time_24h(row["maghrib_begins"]),
        "maghrib_jamah": format_time_24h(row["maghrib_jamah"]),
        "isha_begins": format_time_24h(row["isha_begins"]),
        "isha_jamah": format_time_24h(row["isha_jamah"]),
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)

# Save JSON output to a file
output_file = 'swansea_prayer_times.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
