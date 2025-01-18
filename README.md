# Prayer Times CSV to JSON Converter

This repository provides a tool for converting CSV files into the correct JSON format for prayer times. Each folder in the repository represents a masjid, and the `output.json` file within each folder contains the prayer times for that specific masjid.

## JSON Format

The JSON output format looks like this:
The reason being is the output is necessary for the firebase to correctly read the prayer times for the users device
```json
[
    {
        "d_date": "2025-01-01",
        "fajr_begins": "6:37",
        "fajr_jamah": "",
        "sunrise": "08:27",
        "zuhr_begins": "12:14",
        "zuhr_jamah": "",
        "asr_mithl_1": "1:35",
        "asr_mithl_2": "1:35",
        "maghrib_begins": "3:51",
        "isha_begins": "5:31",
        "isha_jamah": "",
        "hijri_date": "0",
        "is_ramadan": "0"
    },
    {
        "d_date": "2025-01-02",
        "fajr_begins": "6:37",
        "fajr_jamah": "",
        "sunrise": "08:27",
        "zuhr_begins": "12:15",
        "zuhr_jamah": "",
        "asr_mithl_1": "1:36",
        "asr_mithl_2": "1:36",
        "maghrib_begins": "03:53",
        "isha_begins": "5:33",
        "isha_jamah": "",
        "hijri_date": "0",
        "is_ramadan": "0"
    }
]
```

## Folder Structure

Each folder represents a masjid and contains an `output.json` file for the prayer times. The `output.json` file cannot be modified directly. For future months, the new prayer times will be appended to the end of the existing `output.json` file for that masjid.

### Example Folder Structure

```
├── masjid_1
│   ├── input.csv
│   ├── output.json
├── masjid_2
│   ├── input.csv
│   ├── output.json
```

## Workflow

1. Place the CSV file (`input.csv`) with prayer times in the corresponding masjid folder.
2. Run the script to convert the CSV file into the correct JSON format.
3. The script will append the prayer times to the existing `output.json` file in the correct format.

## Requirements

- Python 3.x
- pandas library

## Usage

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install the required dependencies:
   ```bash
   pip install pandas
   ```

3. Run the conversion script:
   ```bash
   python masjid.py 
   ```

   Replace `masjid` with the name of the masjid file you are working on but make sure you are in that folder before you try to run the code

## Contributions

Contributions are welcome! Please ensure your changes align with the repository's purpose and maintain the correct JSON format.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
