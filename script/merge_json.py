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

# Convert the original dictionary structure into a flat list of dictionaries, including Associated_Areas
final_merged_output = []

for rd_name, rd_data in data1.items():
    rd_info = rd_data["RD_Info"]

    # Remove NaN entries from Associated_Areas
    associated_areas = remove_nan_entries(rd_data.get("Associated_Areas", []))

    # Add Facilities if available
    if rd_info["Name"] in facilities_mapping:
        rd_info["Facilities"] = facilities_mapping[rd_info["Name"]]

    # Convert float values to integers where applicable
    cleaned_rd_info = convert_floats_to_int(rd_info)
    cleaned_associated_areas = convert_floats_to_int(associated_areas)

    # Append the restructured RD_Info dictionary to the list, including Associated_Areas
    cleaned_rd_info["Associated_Areas"] = cleaned_associated_areas
    final_merged_output.append(cleaned_rd_info)

# Save cleaned and formatted merged data with associated areas
with open(output_file, "w") as f:
    json.dump(final_merged_output, f, indent=4)

print(f"Merged JSON saved to {output_file}")
