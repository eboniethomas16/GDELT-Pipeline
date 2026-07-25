from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pyarrow.parquet as pq

CACHE_PARSED_DIR = r"C:\Users\einob\OneDrive - King's College London\AA - Individual Project Files\GDELT_pipeline\data\cache\corrupted"

def is_parquet_corrupted(path):
    # A. Size check
    if os.path.getsize(path) < 1000:   # tiny parquet = corrupted
        return True

    # B. Magic bytes check
    with open(path, "rb") as f:
        start = f.read(4)
        f.seek(-4, os.SEEK_END)
        end = f.read(4)

    if start != b"PAR1" or end != b"PAR1":
        return True

    # C. Safe read check
    try:
        pq.read_table(path)
        return False
    except Exception:
        return True


def clean_one_file(path):
    """Check + delete a single parquet file. Returns filename if removed."""
    if is_parquet_corrupted(path):
        fname = os.path.basename(path)
        print(f"🗑️ Removing corrupted parquet: {fname}")
        os.remove(path)
        return fname
    return None


def clean_corrupted_parquets(directory, max_threads=15):
    """Parallel cleanup using ThreadPoolExecutor."""
    removed = []

    # Collect all parquet paths
    parquet_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".parquet")
    ]

    # Parallel corruption checking + deletion
    with ThreadPoolExecutor(max_workers=max_threads) as ex:
        futures = {ex.submit(clean_one_file, path): path for path in parquet_files}

        for future in as_completed(futures):
            result = future.result()
            if result:
                removed.append(result)

    return removed


# ---- RUN CLEANUP ----
removed = clean_corrupted_parquets(CACHE_PARSED_DIR)

print("\n🧹 Cleanup complete.")
print(f"Total corrupted parquet files removed: {len(removed)}")
for fname in removed:
    print(" -", fname)
