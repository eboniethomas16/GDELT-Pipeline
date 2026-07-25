"""dsfdfs
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ------------------------------------------------------------
# 1. Load all monthly CSVs
# ------------------------------------------------------------
folder = Path(r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\combined_datasets\Updated Monthly Filtered Datasets\CLEANED Combined Datasets")
files = sorted(folder.glob("*.csv"))

dfs = []
for f in files:
    print(f"processing file:", f)
    df = pd.read_csv(f)

    # Mixed-format date parser
    df["date"] = pd.to_datetime(df["date"], format="mixed")

    dfs.append(df)

raw = pd.concat(dfs, ignore_index=True)

# ------------------------------------------------------------
# 2. Filter duplicates
# ------------------------------------------------------------
raw["headline_is_duplicate"] = raw["headline_is_duplicate"].astype(str).str.upper().str.strip()
filtered = raw[raw["headline_is_duplicate"] == "TRUE"]

# ------------------------------------------------------------
# 3. Compute duplicate frequency per headline
# ------------------------------------------------------------
dup_freq = (
    filtered.groupby("headline")["GKGRECORDID"]
    .nunique()
)

# ------------------------------------------------------------
# 4. Plot histogram
# ------------------------------------------------------------
# Keep only headlines repeated 3+ times
dup_freq_filtered = dup_freq[dup_freq >= 3]

plt.figure(figsize=(10, 6))
plt.hist(dup_freq_filtered, bins=50, color="steelblue", edgecolor="black")
plt.title("Distribution of Duplicate Headline Frequency")
plt.xlabel("Number of Duplicate Mentions (unique GKGRECORDID)")
plt.ylabel("Number of Headlines")
plt.grid(alpha=0.3)
plt.show()
