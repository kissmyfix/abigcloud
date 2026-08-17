import glob
import os
import pandas as pd
import pdfplumber

# Canonical output schema
OUT_COLS = ["YEAR", "COUNTY", "PROJ_TYPE", "FILING_DATE", "CASE_NO", "LESSEE",
            "PROPERTY_ADDRESS", "CITY", "PARCEL_ID", "PROP_TYPE", "PROP_CODE",
            "CONTACT", "CONTACT_TITLE", "EMAIL", "EST_VALUE", "RENT",
            "PILOT_CITY", "PILOT_COUNTY", "LH_TAX", "LEASE_BEGIN", "LEASE_END",
            "REPORTING_FLAG", "SOURCE_NOTE"]

# Each format maps this year's raw row field names, in order (index 0 = county),
# to canonical field names. None = drop that field.
FORMATS = {
    2016: ["COUNTY", "CASE_NO_SKIP", "FILING_DATE", "PROJ_TYPE", "LESSEE", "PROPERTY_ADDRESS",
           "CITY", "CONTACT", "EMAIL", "PARCEL_ID", "PROP_CODE", "REPORTING_FLAG",
           "SEQ_SKIP", "EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX",
           "LEASE_BEGIN", "LEASE_END"],
    2017: ["COUNTY", "CTY_CODE_SKIP", "PROJ_TYPE", "FILING_DATE", "CASE_NO", "LESSEE",
           "PROPERTY_ADDRESS", "CITY", "PARCEL_ID", "PROP_CODE", "CONTACT", "CONTACT_TITLE",
           "EMAIL", "EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX",
           "LEASE_BEGIN", "LEASE_END"],
    2018: ["COUNTY", "PROJ_TYPE", "FILING_DATE", "CASE_NO", "LESSEE", "PROPERTY_ADDRESS",
           "CITY", "PARCEL_ID", "PROP_CODE", "CONTACT", "CONTACT_TITLE", "EMAIL",
           "EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX",
           "LEASE_BEGIN", "LEASE_END"],
    2019: None,  # same as 2018
    2020: ["COUNTY", "PROJ_TYPE", "FILING_DATE", "CASE_NO", "LESSEE", "PROPERTY_ADDRESS",
           "CITY", "PARCEL_ID", "PROP_TYPE", "PROP_CODE", "CONTACT", "CONTACT_TITLE",
           "EMAIL", "EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX",
           "LEASE_BEGIN", "LEASE_END"],
    2021: ["COUNTY", "PROJ_TYPE", "FILING_DATE", "LESSEE", "PROPERTY_ADDRESS", "CITY",
           "PARCEL_ID", "PROP_TYPE", "PROP_CODE", "CONTACT", "CONTACT_TITLE", "EMAIL",
           "EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX",
           "LEASE_BEGIN", "LEASE_END"],
    2022: None,  # same as 2021
}
FORMATS[2019] = FORMATS[2018]
FORMATS[2022] = FORMATS[2021]
ODS_FORMAT = FORMATS[2021]  # confirmed identical field order to 2021/2022

def clean_num(v):
    if v is None:
        return None
    v = str(v).strip().replace(",", "").replace("$", "").replace("\xad", "")
    if v == "" or v.lower() == "nan":
        return None
    try:
        return float(v)
    except ValueError:
        return None

def clean_str(v):
    if v is None:
        return None
    if isinstance(v, float) and pd.isna(v):
        return None
    v = str(v).strip().replace("\xad", "").replace("\n", " ")
    return v if v and v.lower() != "nan" else None

NUMERIC_FIELDS = {"EST_VALUE", "RENT", "PILOT_CITY", "PILOT_COUNTY", "LH_TAX"}

def map_row(field_names, raw_row, year, source_note=None):
    rec = {c: None for c in OUT_COLS}
    rec["YEAR"] = year
    for name, val in zip(field_names, raw_row):
        if name.endswith("_SKIP") or name not in rec:
            continue
        rec[name] = clean_num(val) if name in NUMERIC_FIELDS else clean_str(val)
    if source_note:
        rec["SOURCE_NOTE"] = source_note
    return rec

def rows_from_pdf(path, year, target_county="Hamilton"):
    field_names = FORMATS.get(year)
    if field_names is None:
        return []
    out = []
    current_county = None
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if not row:
                        continue
                    first = (row[0] or "").strip()
                    if first.upper() == "COUNTY":
                        continue
                    if first:
                        current_county = first
                    if current_county and current_county.strip().lower() == target_county.lower():
                        note = None
                        if year == 2016 and clean_str(row[4]) and any(
                            ch.isdigit() for ch in str(row[4])[:5]
                        ):
                            note = "LESSEE field may actually be a property address in source PDF (2016 filing anomaly) - verify manually"
                        out.append(map_row(field_names, row, year, note))
    return out

def rows_from_ods(path, target_county="Hamilton"):
    df = pd.read_excel(path, sheet_name=0, header=None)
    out = []
    current_year = None
    current_county = None
    for _, row in df.iterrows():
        cell0 = row[0]
        if isinstance(cell0, (int, float)) and not pd.isna(cell0) and pd.isna(row[1]):
            current_year = int(cell0)
            continue
        first = clean_str(cell0) or ""
        if first.upper() == "COUNTY":
            continue
        if first:
            current_county = first
        if current_county and current_county.strip().lower() == target_county.lower():
            raw_row = [row[i] if i < len(row) else None for i in range(0, 19)]
            out.append(map_row(ODS_FORMAT, raw_row, current_year))
    return out

def main():
    base = "/home/brandon/Documents/data_center_research/pilot_data/hamilton_county"
    all_rows = []

    for p in sorted(glob.glob(os.path.join(base, "*.pdf"))):
        year = int(os.path.basename(p)[:4])
        recs = rows_from_pdf(p, year)
        print(f"{os.path.basename(p)}: {len(recs)} Hamilton rows")
        all_rows.extend(recs)

    for p in sorted(glob.glob(os.path.join(base, "*.ods"))):
        recs = rows_from_ods(p)
        print(f"{os.path.basename(p)}: {len(recs)} Hamilton rows")
        all_rows.extend(recs)

    df = pd.DataFrame(all_rows, columns=OUT_COLS)
    df = df.sort_values(["YEAR", "LESSEE"], kind="stable", na_position="last").reset_index(drop=True)

    out_csv = os.path.join(base, "hamilton-county-pilot-master-2014-2025.csv")
    df.to_csv(out_csv, index=False)
    print(f"\nWrote {len(df)} total rows to {out_csv}")
    print(df["YEAR"].value_counts().sort_index())
    flagged = df[df["SOURCE_NOTE"].notna()]
    if len(flagged):
        print(f"\n{len(flagged)} row(s) flagged for manual verification:")
        print(flagged[["YEAR", "LESSEE", "PROPERTY_ADDRESS", "SOURCE_NOTE"]].to_string())

if __name__ == "__main__":
    main()
