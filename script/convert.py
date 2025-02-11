import pandas as pd
import json
import sys

def excel_to_json(excel_file, json_file):
    # Read the Excel file
    df = pd.read_excel(excel_file, sheet_name=None)  # sheet_name=None to load all sheets

    # Convert the Excel sheets to JSON
    json_data = {}
    for sheet_name, data in df.items():
        json_data[sheet_name] = data.to_dict(orient='records')  # Convert each sheet to a list of dictionaries

    # Write the JSON data to a file
    with open(json_file, 'w') as f:
        f.write(json.dumps(json_data, indent=4))  # Pretty-print with indent

if __name__ == "__main__":
    # You can pass the file names as arguments
    excel_file = sys.argv[1]  # Input Excel file
    json_file = sys.argv[2]   # Output JSON file
    excel_to_json(excel_file, json_file)
