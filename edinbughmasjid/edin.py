import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'Edinburgh_Prayer_Timetable_January_2025.xlsx - Sheet1.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the input CSV structure
df.columns = [
    "greg_date", "week_day", "fajr_start", "fajr_jamah", "sunrise",
    "zuhr_start", "zuhr_jamah", "asr_start", "asr_jamah",
    "maghrib_start", "isha_start", "isha_jamah"
]

# Function to convert times to 24-hour format
def format_time_24h(value):
    try:
        time_obj = datetime.strptime(value, "%I:%M")  # Parse in 12-hour format
        return time_obj.strftime("%H:%M")  # Convert to 24-hour format
    except ValueError:
        return ""  # Return empty string for invalid times

# Reformat the data into the desired structure
result = []
start_date = datetime(2025, 1, 1)  # Assuming the year 2025

for index, row in df.iterrows():
    try:
        day_offset = int(row["greg_date"]) - 1
        d_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
    except ValueError:
        continue  # Skip rows with invalid date values

    entry = {
        "d_date": d_date,
        "fajr_begins": format_time_24h(row["fajr_start"]),
        "fajr_jamah": format_time_24h(row["fajr_jamah"]),
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["zuhr_start"]),
        "zuhr_jamah": format_time_24h(row["zuhr_jamah"]),
        "asr_mithl_1": format_time_24h(row["asr_start"]),
        "asr_mithl_2": format_time_24h(row["asr_start"]),  # Same as asr_start
        "asr_jamah": format_time_24h(row["asr_jamah"]),
        "maghrib_begins": format_time_24h(row["maghrib_start"]),
        "maghrib_jamah": format_time_24h(row["maghrib_start"]),  # Assuming same as maghrib_start
        "isha_begins": format_time_24h(row["isha_start"]),
        "isha_jamah": format_time_24h(row["isha_jamah"]),
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)

# Save JSON output to a file
output_file = 'edinburgh_prayer_times.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
