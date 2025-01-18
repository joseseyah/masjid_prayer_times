import pandas as pd
import json
from datetime import datetime

# File path to your CSV file
csv_file = '2025 Full Year iMosque Timetable.xlsx - Masjid Timetable.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file)

# Rename columns to match the provided CSV data
df.columns = [
    "date", "fajr_adhan", "fajr_iqamah", "dhuhr_adhan", "dhuhr_iqamah",
    "asr_adhan", "asr_iqamah", "maghrib_adhan", "maghrib_iqamah",
    "isha_adhan", "isha_iqamah", "jumma_adhan", "jumma_iqamah",
    "sunrise", "suhoor_end"
]

# Drop unnecessary columns if any (e.g., Jumma Adhan and Iqamah)
df = df.drop(columns=["jumma_adhan", "jumma_iqamah"])

# Fill missing values with default placeholders
df = df.fillna("")

# Function to format the date as 2025-MM-DD
def format_date(date_str):
    try:
        # Parse the date as "MM/DD/YYYY" and format it as "YYYY-MM-DD"
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return ""  # Return an empty string if the date cannot be parsed

# Reformat the data into the desired structure
result = []
for index, row in df.iterrows():
    entry = {
        "d_date": format_date(row["date"]),  # Format the date
        "fajr_begins": (row["fajr_adhan"]) if row["fajr_adhan"] else "",
        "fajr_jamah": (row["fajr_iqamah"]) if row["fajr_iqamah"] else "",
        "sunrise": (row["sunrise"]) if row["sunrise"] else "",
        "zuhr_begins": (row["dhuhr_adhan"]) if row["dhuhr_adhan"] else "",
        "zuhr_jamah": (row["dhuhr_iqamah"]) if row["dhuhr_iqamah"] else "",
        "asr_mithl_1": (row["asr_adhan"]) if row["asr_adhan"] else "",
        "asr_jamah": (row["asr_iqamah"]) if row["asr_iqamah"] else "",
        "maghrib_begins": (row["maghrib_adhan"]) if row["maghrib_adhan"] else "",
        "maghrib_jamah": (row["maghrib_iqamah"]) if row["maghrib_iqamah"] else "",
        "isha_begins": (row["isha_adhan"]) if row["isha_adhan"] else "",
        "isha_jamah": (row["isha_iqamah"]) if row["isha_iqamah"] else "",
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)

# Save JSON output to a file as a list of objects
output_file = 'bury.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
