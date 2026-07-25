import os
import pandas as pd

# Input folder containing all monthly headline datasets
INPUT_FOLDER = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Updated Monthly Filtered Datasets\CLEANED Combined Datasets"

# Output folder for filtered monthly files
OUTPUT_FOLDER = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Updated Monthly Filtered Datasets\CLEANED Combined Datasets\filtered_crime_rows_only"

def filter_each_month():
    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Loop through every CSV in the folder
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".csv"):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            print(f"📄 Loading: {filename}")

            # Load CSV safely
            df = pd.read_csv(input_path, dtype=str)

            # Ensure column exists
            if "crime_types" not in df.columns:
                print(f"⚠️ Skipping {filename}: missing 'crime_types' column")
                continue

            # Filter out UNKNOWN crime typeshuu
            before = len(df)
            df_filtered = df[df["crime_types"].str.upper() != "UNKNOWN"]
            after = len(df_filtered)

            print(f"   ➤ Filtered UNKNOWN: {before - after} rows removed")

            # Save filtered monthly file
            df_filtered.to_csv(output_path, index=False)
            print(f"   ✔ Saved filtered file → {output_path}\n")

    print("🎉 All monthly files processed and saved!")

if __name__ == "__main__":
    filter_each_month()
