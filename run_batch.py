import os
import pandas as pd
from datetime import datetime
from daterange import generate_gkg_timestamps
from downloader import download_gdelt_file as download_gkg_file
from parser import parse_gkg_file
from filters import filter_crime
from aggregator import extract_tone_and_date
from config import OUTPUT_DIR
import time


total_start = time.perf_counter()

OUTPUT_FILE = "data/outputs/London_Crime_2015_to_today.parquet"

start = "2026-02-28"
end = "2026-03-01"
def run_batch(start=start, end=end):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    all_daily = []

    for ts in generate_gkg_timestamps(start_date, end_date):
        print(f"\n=== Processing {ts} ===")

        # Download
        zip_path = download_gkg_file(ts)
        print(zip_path)
        if zip_path is None:
            print("✖ File missing on GDELT — skipping")
            continue

        # Parse
        df = parse_gkg_file(zip_path)
        if df is None or df.empty:
            print("✖ Parsed DF empty — skipping")
            continue

        # Filter
        crime_df = filter_crime(df, ts)
        if crime_df is None or crime_df.empty:
            print("No London crime rows — skipping")
            continue
        crime_df["date"] = pd.to_datetime(ts, format="%Y%m%d%H%M%S", errors="coerce")
    
        #append
        all_daily.append(crime_df)
    
    if not all_daily:
        print("\nNo crime data found in the entire date range.")
        return

    

    # Combine everything once
    combined_df = pd.concat(all_daily, ignore_index=True)
 
    #removes the london_top2 column if exists
    if "london_top2" in combined_df.columns:
        print("removed london_top2")
        combined_df = combined_df.drop(columns=["london_top2"])

    #EXTRACT TONE AND DATE   
    combined_df = extract_tone_and_date(combined_df)


    # Compute daily average tone
    daily_avg = (
        combined_df.groupby(combined_df["date"].dt.date)["tone"]
        .mean()
        .reset_index()
        .rename(columns={"tone": "daily_avg_tone", "date": "date_only"})
    )

    combined_df["date_only"] = combined_df["date"].dt.date
    combined_df = combined_df.merge(daily_avg, on="date_only", how="left")
    combined_df.drop(columns=["date_only"], inplace=True)
    
    #DROP UNUSED COLUMNS
    cols_to_drop = [
    "V2.1TRANSLATIONINFO",
    "V2SOURCECOLLECTIONID",
    "V2EXTRASXML",
    "V2.1QUOTATIONS",
    "V2.1SOCIALIMAGEEMBEDS",
    "V2.1RELATEDIMAGES",
    "V1COUNTS",
    "V2GCAM",
    "V2.1SHARINGIMAGE",
    "V2.1ENHANCEDDATES",
    "V1PERSONS",
    "V2.1DATE",
    "V2SOURCECOLLECTIONIDENTIFIER"
    ]
    combined_df = combined_df.drop(columns=[c for c in cols_to_drop if c in combined_df.columns], errors="ignore")

    # Reorder columns: date, tone, daily_avg_tone first
    first_cols = ["date", "tone", "daily_avg_tone","crime_mentions","V2ENHANCEDTHEMES","V2SOURCECOMMONNAME","V1DOCUMENTIDENTIFIER"]
    other_cols = [c for c in combined_df.columns if c not in first_cols]
    combined_df = combined_df[first_cols + other_cols]
    
    def safe_save(base_path):
        """
        Returns a unique file path by appending (1), (2), ... if needed.
        """
        if not os.path.exists(base_path):
            return base_path

        root, ext = os.path.splitext(base_path)
        counter = 1

        while True:
            new_path = f"{root} ({counter}){ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    # Save final combined_df CSV
    filename = f"London_Crime_combined_df_{start}_to_{end}.csv"
    out_path = os.path.join(OUTPUT_DIR, filename)
    output_path = safe_save(out_path)
    combined_df.to_csv(output_path, index=False)


    print(f"\n✔ combined_df CSV saved to: {out_path}")

    #combine_parsed_csvs(start,end)


if __name__ == "__main__":
    run_batch(start, end)

total_end = time.perf_counter()
print(f"\n⏱ Total pipeline runtime: {total_end - total_start:.2f} seconds")
