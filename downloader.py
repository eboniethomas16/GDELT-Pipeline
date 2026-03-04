import os
import requests
import datetime
from datetime import timedelta
from config import GDELT_BASE, DATA_DIR, CACHE_DIR

#GDELT publishes files every 15 minutes. this downloads any missing ones I don't already have
def generate_timestamp_list(hours_back=24):
    now = datetime.datetime.now(datetime.timezone.utc)
    minute = (now.minute // 15) * 15 #  Round DOWN to nearest 15-minute interval
    now = now.replace(minute=minute, second=0, microsecond=0)


    timestamps = []
    for i in range(hours_back * 4):  # 4 files per hour
        ts = now - datetime.timedelta(minutes=15 * i)
        timestamps.append(ts.strftime("%Y%m%d%H%M%S"))
            #YYYYMMDDHHMMSS is the timestamp for "DATEADDED" field
    print("Generated timestamps:", timestamps[:5])
    return timestamps

def download_gdelt_file(timestamp):
    filename = f"{timestamp}.gkg.csv.zip"
    local_path = os.path.join(CACHE_DIR, filename)

    # 1. Check cache first
    if os.path.exists(local_path):
        print(f"✔ Using cached .zip: {local_path}")
        return local_path

    # 2. Download if not cached
    url = f"{GDELT_BASE}{timestamp}.gkg.csv.zip"
    r = requests.get(url)

    if r.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(r.content)
        print(f"✔ Downloaded and cached .ZIP: {local_path}")
        return local_path

    print("✖ Missing on GDELT:", url)
    return None

def download_recent(hours_back=1):
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamps = generate_timestamp_list(hours_back)
    downloaded = []

    for ts in timestamps:
        path = download_gdelt_file(ts)
        if path:
            downloaded.append(path)

    return downloaded

