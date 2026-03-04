import pandas as pd
import os
from collections import Counter
from config import CRIME_THEMES, UK_SITES, CACHE_FILTERED, GREATER_LONDON_LOC

### Imports the CRIME_THEMES list from your config.py file.
### CRIME_THEMES is A list of theme keywords I defined in config, e.g.
### ["CRIME", "VIOLENCE", "POLICE", "SECURITY", "TERROR"] ###

#filters.py is the gatekeeper:
#- It takes the full GDELT GKG dataset.
#- It keeps only the rows that are about crime, violence, policing, security, or terrorism.
#- Everything else is discarded before you compute tone, aggregate, or visualise.
#outputs a focused subset of GDELT that aligns with crime and policing perception (or whatever parameters i want)


#filter_crime function will return only the rows in df that are related to crime/policing in LONDON
#the "|" is an "OR". 
    # ex. CRIME_THEMES = ["CRIME", "VIOLENCE", "POLICE"]
    # pattern = "CRIME|VIOLENCE|POLICE"
#It lets you search for any of the themes in a single .str.contains() call.

os.makedirs(CACHE_FILTERED, exist_ok=True)


def filter_crime(df, timestamp): #df is a pandas DataFrame containing GDELT GKG data (already parsed)
    #If filtered cache exists → load and return
    filtered_path = os.path.join(CACHE_FILTERED, f"{timestamp}.parquet")

    if os.path.exists(filtered_path):
        print(f"✔ Using cached filtered DF: {filtered_path}")
        return pd.read_parquet(filtered_path)

    for col in [
        "V1THEMES", "V2ENHANCEDTHEMES",
        "V1LOCATIONS", "V2ENHANCEDLOCATIONS",
        "V2SOURCECOMMONNAME"
    ]:
        df[col] = df[col].fillna("").str.upper()


    #filterrrr

    # ---------------------------------------------------------
    # 2. Crime theme detection (vectorised)
    # ---------------------------------------------------------
    crime_pattern = "|".join(CRIME_THEMES)
    crime_mask = (
        df["V2ENHANCEDTHEMES"].str.contains(crime_pattern, regex=True)
    )

    # ---------------------------------------------------------
    # 3. Website filtering (vectorised)
    # ---------------------------------------------------------
    
    uk_pattern = "|".join(UK_SITES)
    website_mask = df["V2SOURCECOMMONNAME"].str.contains(uk_pattern, regex=True)

    # ---------------------------------------------------------
    # 4. London detection (vectorised)
    # ---------------------------------------------------------
    pattern = "|".join(GREATER_LONDON_LOC)
    greater_london_mask = (
    df["V1LOCATIONS"].str.contains(pattern, case=False, regex=True) |
    df["V2ENHANCEDLOCATIONS"].str.contains(pattern, case=False, regex=True)
    )


    # ---------------------------------------------------------
    # 5. London mentions ≥ 2 (fast vectorised counting)
    # ---------------------------------------------------------
    # Make an uppercase lookup set once
    df["london_mentions"] = df["V2ENHANCEDLOCATIONS"].apply(
        lambda s: sum(
            1
            for b in (s.split(";") if isinstance(s, str) else [])
            if b.count("#") >= 2 and any(
                gl in b.split("#")[1].upper()
                for gl in GREATER_LONDON_LOC
            )
        )
    )
    london_count_mask = df["london_mentions"] >= 2
    # ---------------------------------------------------------
    # 6. Crime mentions ≥ 2 (vectorised)
    # ---------------------------------------------------------
    df["crime_mentions"] = df["V2ENHANCEDTHEMES"].apply(
    lambda s: sum(1 for crime in CRIME_THEMES if crime in s)
    )
    crime_mentions_mask = df["crime_mentions"] >= 2

    # ---------------------------------------------------------
    # 7. London top‑2 logic (vectorised)
    # ---------------------------------------------------------
    # def top2_london(loc_string):
    #     if not isinstance(loc_string, str) or not loc_string.strip():
    #         return False

    #     names = []
    #     for block in loc_string.split(";"):
    #         parts = block.split("#")
    #         if len(parts) >= 2 and parts[1].strip():
    #             names.append(parts[1].upper())

    #     if not names:
    #         return False

    #     top_two = [loc for loc, _ in Counter(names).most_common(2)]
    #     return any("LONDON" in loc for loc in top_two)
    # df["london_top2"] = df["V2ENHANCEDLOCATIONS"].apply(top2_london)


    #Debug to figure out filters
    print("Rows after crime theme filter:", crime_mask.sum())
    print("Rows after website filter:", website_mask.sum())
    print("Rows after Greater London filter:", greater_london_mask.sum())
    print("Rows after London mentions >=2:", london_count_mask.sum())
    print("Rows after crime mentions >=2:", crime_mentions_mask.sum())
    #print("Rows after London top2:", df["london_top2"].sum())

    # ---------------------------------------------------------
    # 8. Combine all filters
    # ---------------------------------------------------------
    final_mask = (
        crime_mask &
        website_mask &
        greater_london_mask &
        london_count_mask &
        crime_mentions_mask
        #df["london_top2"]
    )
    filtered = df[final_mask].copy()

    # ---------------------------------------------------------
    # 9. Cache filtered DF
    # ---------------------------------------------------------
    filtered.to_parquet(filtered_path, index=False)
    print(f"✔ Cached filtered DF: {filtered_path}")

    return filtered

   