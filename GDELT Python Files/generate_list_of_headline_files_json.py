import os
import json

FOLDER = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Updated Monthly Filtered Datasets\CLEANED Combined Datasets\filtered_crime_rows_only"

files = [f for f in os.listdir(FOLDER) if f.endswith(".csv")]

with open(r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\Data_Visuals\Scrollytelling_draft\data\monthly_headline_filenames.json", "w") as f:
    json.dump(files, f, indent=2)

print("Saved monthly_files.json with", len(files), "files.")
