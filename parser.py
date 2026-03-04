import os
import zipfile
import pandas as pd
from collections import Counter
from config import PARSED_DIR, GKG_COLS, CRIME_THEMES, UK_SITES, CACHE_PARSED_DIR
import pyarrow.csv as pv
import pyarrow.parquet as pq


#this file takes a raw GDELT 2.0 ZIP file, extracts the CSV within it,
#assignes the correct column names,
#and saves a clean, readable CSV for downstream processing.
#ZIP → CSV → DataFrame → Cleaned CSV

GDELT_COLUMNS = [
    "GKGRECORDID",             
    "V2.1DATE",                
    "V2SOURCECOLLECTIONID",   
    "V2SOURCECOMMONNAME",      
    "V1DOCUMENTIDENTIFIER",    
    "V1COUNTS",                
    "V2.1COUNTS",
    "V1THEMES",                
    "V2ENHANCEDTHEMES",
    "V1LOCATIONS",
    "V2ENHANCEDLOCATIONS",
    "V1PERSONS",               
    "V2ENHANCEDPERSONS",
    "V1ORGANIZATIONS",         
    "V2ENHANCEDORGANIZATIONS",
    "V1.5TONE",                
    "V2.1ENHANCEDDATES",
    "V2GCAM",
    "V2.1SHARINGIMAGE",
    "V2.1RELATEDIMAGES",
    "V2.1SOCIALIMAGEEMBEDS",
    "V2.1SOCIALVIDEOEMBEDS",
    "V2.1QUOTATIONS",
    "V2.1ALLNAMES",
    "V2.1AMOUNTS",
    "V2.1TRANSLATIONINFO",
    "V2EXTRASXML"
]

EXPECTED_COLS = len(GDELT_COLUMNS)
os.makedirs(CACHE_PARSED_DIR, exist_ok=True)


# DELETE EVERYTHING ABOVE THIS
#loads the data frame
def parse_gkg_file(zip_path):
    timestamp = os.path.basename(zip_path).split(".")[0]
    parsed_path = os.path.join(CACHE_PARSED_DIR, f"{timestamp}.parquet")

    # 1. Load cached parsed DF if available
    if os.path.exists(parsed_path):
        print(f"✔ Using cached parsed DF: {parsed_path}")
        return pd.read_parquet(parsed_path)

    # 2. Extract CSV from ZIP using pyarrow (fast)
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                table = pv.read_csv(
                    f,
                    parse_options=pv.ParseOptions(delimiter="\t"),
                    convert_options=pv.ConvertOptions(strings_can_be_null=True)
                )
                df = table.to_pandas()
    except Exception as e:
        print("✖ Parse failed:", e)
        return None

    # 3. Validate column count
    if df.shape[1] < EXPECTED_COLS:
        print(f"✖ Unexpected column count: {df.shape[1]} (expected ≥ {EXPECTED_COLS})")
        return None
    # 4. Assign minimal schema
    df = df.iloc[:, :EXPECTED_COLS]
    df.columns = GDELT_COLUMNS

    # 5. Cache parsed DF
    df.to_parquet(parsed_path, index=False)
    print(f"✔ Cached parsed DF: {parsed_path}")

    return df



