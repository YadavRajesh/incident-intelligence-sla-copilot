import pandas as pd
from pathlib import Path

# =====================================================
# EXCEL TO CSV CONVERTER
# =====================================================

INPUT_EXCEL_PATH = "data/HistoricalIncidents.xlsx"
OUTPUT_CSV_PATH = "data/HistoricalIncidents.csv"

# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [
    "incident_number",
    "short_description",
    "description",
    "assignment_group",
    "business_service",
    "cmdb_ci"
]

# =====================================================
# VALIDATE FILE EXISTS
# =====================================================

excel_path = Path(INPUT_EXCEL_PATH)

if not excel_path.exists():
    raise FileNotFoundError(
        f"Excel file not found: {INPUT_EXCEL_PATH}"
    )

print("Loading Excel file...")

# =====================================================
# READ EXCEL
# =====================================================

df = pd.read_excel(
    INPUT_EXCEL_PATH,
    dtype=str
)

print(f"Rows loaded: {len(df)}")

# =====================================================
# VALIDATE REQUIRED COLUMNS
# =====================================================

missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

print("All required columns found.")

# =====================================================
# CLEAN DATA
# =====================================================

# Keep only required columns
df = df[REQUIRED_COLUMNS]

# Replace NaN with empty strings
df = df.fillna("")

# Remove extra spaces
df = df.apply(
    lambda col: col.str.strip()
)

# Remove duplicates
df = df.drop_duplicates(
    subset=["incident_number"]
)

print(f"Rows after cleanup: {len(df)}")

# =====================================================
# EXPORT CSV
# =====================================================

df.to_csv(
    OUTPUT_CSV_PATH,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print("CSV generated successfully.")
print(f"Output path: {OUTPUT_CSV_PATH}")