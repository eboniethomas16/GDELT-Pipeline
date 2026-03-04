from downloader import download_gdelt_file
from parser import parse_gkg_file
from filters import filter_crime
from aggregator import extract_tone, aggregate_daily
from storage import save_parquet


def run_pipeline(timestamp, output_path):
    print(f"\n=== GDELT Crime Pipeline Started ===")
    print(f"Timestamp: {timestamp}")

    # 1. Download
    print("\n[1] Downloading GKG file...")
    zip_path = download_gdelt_file(timestamp)
    if zip_path is None:
        print("❌ File not found on GDELT servers.")
        return
    print(f"✔ Downloaded: {zip_path}")

    # 2. Parse
    print("\n[2] Parsing GKG file...")
    df = parse_gkg_file(zip_path)
    print(f"✔ Parsed rows: {len(df)}")

    # 3. Filter crime themes
    print("\n[3] Filtering crime-related records...")
    crime_df = filter_crime(df)
    print(f"✔ Crime rows: {len(crime_df)}")

    if crime_df.empty:
        print("⚠ No crime-related records found for this timestamp.")
        return

    # 4. Extract tone + date
    print("\n[4] Extracting tone and timestamp...")
    crime_df = extract_tone(crime_df)
    print("✔ Tone + date extracted")

    # 5. Aggregate daily sentiment
    print("\n[5] Aggregating daily sentiment...")
    daily_df = aggregate_daily(crime_df)
    print("✔ Aggregation complete")

    # 6. Save output
    print("\n[6] Saving final dataset...")
    save_parquet(daily_df, output_path)
    print(f"✔ Saved to: {output_path}")

    print("\n=== Pipeline Complete ===\n")


if __name__ == "__main__":
    # Example run:
    # Pick a known-valid timestamp
    test_timestamp = "20150219004500"

    # Output location
    output_file = "data/processed/gdelt_daily_tone.parquet"

    run_pipeline(test_timestamp, output_file)

