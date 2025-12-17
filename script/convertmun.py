import pandas as pd
import json
import sys

RD_ONLY_FIELDS = [
    "Population",
    "PreviousYearPerCaptiaDisposal",
    "PreviousYearTotalDisposal"
]

def safe_strip(value):
    return value.strip() if isinstance(value, str) else value

def filter_rd_fields(record):
    """Keep only allowed RD fields + Name & Area Type"""
    allowed = set(RD_ONLY_FIELDS + ["Name", "Area Type"])
    return {k: v for k, v in record.items() if k in allowed}

def remove_rd_fields(record):
    """Remove RD-only fields from non-RD areas"""
    return {k: v for k, v in record.items() if k not in RD_ONLY_FIELDS}

def process_excel(file_path, output_json):
    xls = pd.ExcelFile(file_path)
    final_data = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if "Name" not in df.columns or "Area Type" not in df.columns:
            continue

        rd_names = df[df["Area Type"] == "RD"]["Name"].unique()

        for rd in rd_names:
            rd_row = df[df["Name"] == rd].iloc[0]
            rd_index = rd_row.name

            related_areas = df.loc[rd_index + 1:]

            next_rd_index = related_areas[related_areas["Area Type"] == "RD"].index.min()
            if pd.notna(next_rd_index):
                related_areas = related_areas.loc[:next_rd_index - 1]

            # RD info (restricted fields only)
            rd_info = filter_rd_fields(rd_row.to_dict())
            rd_info["Name"] = safe_strip(rd_info.get("Name", ""))

            # Associated areas (RD fields removed)
            associated_areas = []
            for _, row in related_areas.iterrows():
                area = remove_rd_fields(row.to_dict())
                area["Name"] = safe_strip(area.get("Name", ""))
                associated_areas.append(area)

            final_data[rd_info["Name"]] = {
                "RD_Info": rd_info,
                "Associated_Areas": associated_areas
            }

    with open(output_json, "w") as f:
        json.dump(final_data, f, indent=4)

    return output_json

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_json = sys.argv[2]
    process_excel(file_path, output_json)
