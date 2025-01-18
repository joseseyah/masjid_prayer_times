import pandas as pd
import json
from datetime import datetime

# File path to your CSV file
csv_file = 'JAN 25 TIMETABLE.xlsx - Full Year.csv'  # Replace with the actual file path

# Read the CSV file
df = pd.read_csv(csv_file, skiprows=0)

# Rename columns to be more descriptive
df.columns = [
    "empty1", "date", "day", "islamic_date", "fajr_begins", 
    "fajr_jamah", "sunrise", "zuhr_begins", "zuhr_jamah",
    "asr_mithl_1", "asr_mithl_2", "maghrib_begins", "isha_begins", "isha_jamah"
]

# Drop unnecessary columns
df = df.drop(columns=["empty1", "day", "islamic_date"])

# Fill missing columns with default values if needed
df = df.fillna("")

# Function to format the date as 2025-MM-DD
def format_date(date_str):
    try:
        # Parse the date as "DD-MMM" and format it as "2025-MM-DD"
        return datetime.strptime(date_str, "%d-%b").strftime("2025-%m-%d")
    except ValueError:
        return ""  # Return an empty string if the date cannot be parsed

# Function to convert times to 24-hour format
def format_time_24h(value, is_pm=False):
    try:
        # If it's a float or valid string, convert to 24-hour format
        if isinstance(value, (float, int)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
            # Format as HH:MM and replace '.' with ':'
            time_str = f"{float(value):.2f}".replace('.', ':')
            # Parse to datetime to adjust for AM/PM
            time_obj = datetime.strptime(time_str, "%H:%M")
            if is_pm and time_obj.hour < 12:
                time_obj = time_obj.replace(hour=time_obj.hour + 12)
            return time_obj.strftime("%H:%M")
        return value  # Return as-is if not a valid time
    except ValueError:
        return ""  # Return empty string for invalid values

# Reformat the data into the desired structure
# Reformat the data into the desired structure
result = []
for index, row in df.iterrows():
    asr_mithl_1 = format_time_24h(row["asr_mithl_1"], is_pm=True)  # Format asr_mithl_1 first
    entry = {
        "d_date": format_date(row["date"]),  # Format the date
        "fajr_begins": format_time_24h(row["fajr_begins"]),
        "fajr_jamah": format_time_24h(row["fajr_jamah"]),
        "sunrise": format_time_24h(row["sunrise"]),
        "zuhr_begins": format_time_24h(row["zuhr_begins"], is_pm=True),
        "zuhr_jamah": format_time_24h(row["zuhr_jamah"], is_pm=True),
        "asr_mithl_1": asr_mithl_1,
        "asr_mithl_2": asr_mithl_1,  # Set asr_mithl_2 to the same as asr_mithl_1
        "maghrib_begins": format_time_24h(row["maghrib_begins"], is_pm=True),
        "isha_begins": format_time_24h(row["isha_begins"], is_pm=True),
        "isha_jamah": format_time_24h(row["isha_jamah"], is_pm=True),
        "hijri_date": "0",  # Default value
        "is_ramadan": "0",  # Default value
    }
    result.append(entry)


# Save JSON output directly as a list to a file
output_file = 'output.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=4)

print(f"Data has been converted and saved to {output_file}")
