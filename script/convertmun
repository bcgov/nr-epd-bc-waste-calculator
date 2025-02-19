import pandas as pd
import json
import sys

def safe_strip(value):
    return value.strip() if isinstance(value, str) else value

def process_excel(file_path, output_json):
    xls = pd.ExcelFile(file_path)
    final_data = {}
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        if "Name" in df.columns and "Area Type" in df.columns:
            rd_names = df[df["Area Type"] == "RD"]["Name"].unique()
            
            for rd in rd_names:
                rd_data = df[df["Name"] == rd]
                rd_index = df[df["Name"] == rd].index[0]
                related_areas = df.loc[rd_index + 1:]
                
                next_rd_index = related_areas[related_areas["Area Type"] == "RD"].index.min()
                if pd.notna(next_rd_index):
                    related_areas = related_areas.loc[:next_rd_index - 1]
                
                rd_info = rd_data.to_dict(orient="records")[0] if not rd_data.empty else {}
                associated_areas = related_areas.to_dict(orient="records")
                
                rd_info["Name"] = safe_strip(rd_info.get("Name", ""))
                for area in associated_areas:
                    area["Name"] = safe_strip(area.get("Name", ""))
                
                final_data[rd_info["Name"]] = {"RD_Info": rd_info, "Associated_Areas": associated_areas}
    
    with open(output_json, "w") as f:
        json.dump(final_data, f, indent=4)
    
    return output_json

if __name__ == "__main__":
    # You can pass the file names as arguments
    excel_file = sys.argv[1]  # Input Excel file
    json_file = sys.argv[2]   # Output JSON file
    process_excel(file_path, output_json)
