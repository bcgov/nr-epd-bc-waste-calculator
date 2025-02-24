import json
import math
import os

# Fetch file paths from environment variables
input_file1 = os.getenv("INPUT_FILE1", "output2.json")
input_file2 = os.getenv("INPUT_FILE2", "output-2.json")
output_file = os.getenv("OUTPUT_FILE", "final_merged_output.json")

# Load JSON files
with open(input_file1, "r") as f1, open(input_file2, "r") as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

# Function to check if a value is NaN
def is_nan(value):
    return isinstance(value, float) and math.isnan(value)

# Function to remove NaN entries from a list of dictionaries
def remove_nan_entries(areas):
    return [area for area in areas if not any(is_nan(value) for value in area.values())]

# Function to convert float values to int where applicable
def convert_floats_to_int(data):
    if isinstance(data, dict):
        return {key: convert_floats_to_int(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_floats_to_int(item) for item in data]
    elif isinstance(data, float) and data.is_integer():
        return int(data)  # Convert float to int if it's a whole number
    return data

# Create a mapping from Member in output-2.json to Facilities data
facilities_mapping = {entry["Member"]: entry["Facilities"] for entry in data2}

# Merge data while cleaning NaN entries and converting numbers
for rd_name, rd_data in data1.items():
    rd_info_name = rd_data["RD_Info"]["Name"]

    # Remove NaN entries from Associated_Areas
    if "Associated_Areas" in rd_data:
        rd_data["Associated_Areas"] = remove_nan_entries(rd_data["Associated_Areas"])

    # Add Facilities if available
    if rd_info_name in facilities_mapping:
        rd_data["Facilities"] = facilities_mapping[rd_info_name]

# Convert SGC, Population2023, and AuthorizationNumber values to integers where applicable
cleaned_data = convert_floats_to_int(data1)

# Save cleaned and formatted merged data
with open(output_file, "w") as f:
    json.dump(cleaned_data, f, indent=4)

print(f"Merged JSON saved to {output_file}")
