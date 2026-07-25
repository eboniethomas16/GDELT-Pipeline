import os
import pandas as pd

# Input folder containing all cleaned headline datasets
INPUT_FOLDER = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Updated Monthly Filtered Datasets\CLEANED Combined Datasets"

# Output folder + filename
OUTPUT_FOLDER = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Headlines_All_Years"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "headline_AllYearsCombined.csv")

def combine_and_filter_headline_datasets():
    all_dfs = []

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Loop through every CSV in the folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(INPUT_FOLDER, filename)
            print(f"📄 Loading: {filename}")

            df = pd.read_csv(file_path, dtype=str)  # read as strings to avoid dtype issues

            # Ensure column exists
            if "crime_types" not in df.columns:
                print(f"⚠️ Skipping {filename}: missing 'crime_types' column")
                continue

            # Filter out UNKNOWN crime types
            before = len(df)
            df = df[df["crime_types"].str.upper() != "UNKNOWN"]
            after = len(df)

            print(f"   ➤ Filtered UNKNOWN: {before - after} rows removed")

            all_dfs.append(df)

    if not all_dfs:
        print("❌ No valid CSV files found.")
        return

    # Combine all datasets
    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"✅ Combined dataset size: {len(combined_df)} rows")

    # Save final CSV
    combined_df.to_csv(OUTPUT_FILE, index=False)
    print(f"🎉 Final combined CSV saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    combine_and_filter_headline_datasets()
