import pandas as pd
import json
import sys
import numpy as np

def excel_to_json(excel_file, json_file):
    # Read the Excel file
    # df = pd.read_excel(excel_file, sheet_name=None)  # sheet_name=None to load all sheets

 # Load the Excel file properly
    try:
        df = pd.read_excel(excel_file, engine="openpyxl")  # Ensure using the correct engine
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        exit(1)

# Ensure we have a valid DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Loaded data is not a DataFrame. Please check the input file.")

    
    # Ensure column names are correct
    print("Column Names:", df.columns.tolist())  # Helps verify headers

    # Replace NaN values with empty strings
    df = df.replace({np.nan: ""})

    # Group data by "Member" (Region)
    grouped_data = {"Regions": []}
    
    for member, group in df.groupby("Member"):
        facilities = group.drop(columns=["Member"]).to_dict(orient="records")
        grouped_data["Regions"].append({"Member": member, "Facilities": facilities})
    
    # Remove "Regions" and extract its contents
    if "Regions" in grouped_data:
        grouped_data = grouped_data["Regions"]

    # Save as JSON
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(grouped_data, file, indent=2)

    print(f"Data successfully grouped and saved ")

    

if __name__ == "__main__":
    # You can pass the file names as arguments
    excel_file = sys.argv[1]  # Input Excel file
    json_file = sys.argv[2]   # Output JSON file
    excel_to_json(excel_file, json_file)
