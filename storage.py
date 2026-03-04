import pandas as pd
import os

#this function saves the dataframe as a Parquet FileExistsError
#It gives your pipeline a final output stage
#parquet is:
    #- columnar (fast for analytics)
    #- compressed (small file size)
    #- much faster than CSV for reading/writing
    #- ideal for dashboards, APIs, and large datasets
#result is a clean, efficient file ready for data manipulation

#path =  = "AA - Individual Project Files/GDELT2.0 cleaned datasets/GDELT_CRIME_Tones.parquet"
def save_parquet(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)
