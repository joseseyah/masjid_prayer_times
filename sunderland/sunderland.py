import pandas as pd
import json
from datetime import datetime, timedelta

# File path to your CSV file
csv_file = 'Prayer_Times_Sunderland.csv'  # Replace with the actual file path

# Read the CSV file, skipping rows and inferring headers appropriately
df = pd.read_csv(csv_file, skiprows=1, header=None)

# Define month names to identify header rows
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Remove rows that contain month names
df = df[~df[0].astype(str).str.strip().isin(months)]

# Reset index and rename columns
df = df.reset_index(drop=True)
df.columns = [
    "no", "day", "fajr_begins", "sunrise", "zuhr_begins",
    "jumuah", "asr_mithl_1", "maghrib_begins", "isha_begins"
]

# Function to convert times in the format `6.37` or `6:37` to `HH:MM` with afternoon support
def format_time(value, afternoon=False):
    try:
        value = str(value).strip()
        if not value or value.lower() in ["nan", ""]:
            return ""  # Handle empty or invalid values

        if "." in value:  # Handle time in `6.37` format
            hours, minutes = map(int, value.split('.'))
        elif ":" in value:  # Handle time in `6:37` format
            hours, minutes = map(int, value.split(':'))
        else:
            return ""  # Invalid format

        # Convert PM times to 24-hour format for afternoon/evening prayers
        if afternoon and hours < 12:
            hours += 12
        elif not afternoon and hours == 12:  # Handle 12 AM edge case
            hours = 0
        return f"{hours:02}:{minutes:02}"  # Format as HH:MM
    except Exception as e:
        return ""  # Return empty string for invalid times

# Reformat the data into the desired structure
result = []
start_date = datetime(2025, 1, 1)  # Starting date for January 2025

for index, row in df.iterrows():
    try:
        # Skip rows without a valid day number
        if pd.isna(row["no"]) or not str(row["no"]).isdigit():
            continue

        day_offset = int(row["no"]) - 1  # Day number starts from 1
        d_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

        entry = {
            "d_date": d_date,
            "fajr_begins": format_time(row["fajr_begins"]),  # Always AM
            "fajr_jamah": "",  # Blank as per requirement
            "sunrise": format_time(row["sunrise"]),  # Always AM
            "zuhr_begins": format_time(row["zuhr_begins"], afternoon=True),  # PM
            "zuhr_jamah": "",  # Blank as per requirement
            "asr_mithl_1": format_time(row["asr_mithl_1"], afternoon=True),  # PM
            "asr_mithl_2": format_time(row["asr_mithl_1"], afternoon=True),  # PM
            "maghrib_begins": format_time(row["maghrib_begins"], afternoon=True),  # PM
            "isha_begins": format_time(row["isha_begins"], afternoon=True),  # PM
            "isha_jamah": "",  # Blank as per requirement
            "hijri_date": "0",  # Default value
            "is_ramadan": "0",  # Default value
        }
        result.append(entry)
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        continue

# Save JSON output directly as a list to a file
output_file = 'sunderland_prayer_times.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")

