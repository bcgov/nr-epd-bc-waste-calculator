
import pandas as pd
import json
import sys

RD_ONLY_FIELDS = [
    "Population",
    "PreviousYearPerCapitaDisposal",
    "PreviousYearTotalDisposal",
    "EstimatedNumberOfHouseholds"
]

def safe_strip(value):
    return value.strip() if isinstance(value, str) else value

def filter_rd_fields(record):
    allowed = set(RD_ONLY_FIELDS + ["Name", "Area Type"])
    return {k: v for k, v in record.items() if k in allowed}

def remove_rd_fields(record):
    return {
        k: v for k, v in record.items()
        if k not in RD_ONLY_FIELDS
    }

def process_excel(file_path, output_json):
    xls = pd.ExcelFile(file_path)
    final_data = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Normalize Excel column names
        df.columns = df.columns.str.strip()
        df.rename(columns={
            "PreviousYearPerCaptiaDisposal":
                "PreviousYearPerCapitaDisposal"
        }, inplace=True)

        # NEW: Round per-capita disposal to whole numbers
        if "PreviousYearPerCapitaDisposal" in df.columns:
            df["PreviousYearPerCapitaDisposal"] = (
                pd.to_numeric(
                    df["PreviousYearPerCapitaDisposal"],
                    errors="coerce"
                )
                .round(0)
                .apply(lambda x: int(x) if pd.notna(x) else None)
            )

        # Convert NaN values to None
        df = df.astype(object).where(pd.notna(df), None)

        if "Name" not in df.columns or "Area Type" not in df.columns:
            continue

        df["Name"] = df["Name"].apply(safe_strip)
        df["Area Type"] = df["Area Type"].apply(safe_strip)

        rd_indices = df.index[df["Area Type"] == "RD"].tolist()

        for pos, rd_index in enumerate(rd_indices):
            rd_row = df.loc[rd_index]

            next_index = (
                rd_indices[pos + 1]
                if pos + 1 < len(rd_indices)
                else len(df)
            )

            related_areas = df.iloc[rd_index + 1:next_index]

            rd_info = filter_rd_fields(rd_row.to_dict())

            associated_areas = []

            for _, row in related_areas.iterrows():
                area = remove_rd_fields(row.to_dict())
                associated_areas.append(area)

            final_data[rd_info["Name"]] = {
                "RD_Info": rd_info,
                "Associated_Areas": associated_areas
            }

    # Export valid JSON without NaN
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            final_data,
            f,
            indent=4,
            allow_nan=False
        )

    return output_json

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_json = sys.argv[2]
    process_excel(file_path, output_json)
