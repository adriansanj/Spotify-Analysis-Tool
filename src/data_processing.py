import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def create_clean_dataframe(json_files):

    df_list = [pd.read_json(json_file) for json_file in json_files]
    df = pd.concat(df_list, ignore_index=True)

    df_clean = pd.DataFrame()
    df_clean['timestamp'] = pd.to_datetime(df['ts'])
    df_clean['day'] = df_clean['timestamp'].dt.date
    df_clean["week"] = df_clean["timestamp"].dt.to_period("W")
    df_clean['month'] = df_clean['timestamp'].dt.to_period("M")
    df_clean['artist'] = df['master_metadata_album_artist_name']
    df_clean['track'] = df['master_metadata_track_name']
    df_clean['minutes'] = df['ms_played']/1000/60
    df_clean['minutes'] = df_clean['minutes'].apply(lambda x: Decimal(str(x)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))
    
    return df_clean

