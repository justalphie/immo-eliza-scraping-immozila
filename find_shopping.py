import haversine as hs
from haversine import Unit
import pandas as pd
import requests
import math
from requests import Session
from tqdm import tqdm

session = Session()

def get_shopping(lat, lon):

    if not isinstance(lat, (int, float)) or math.isnan(lat) or not isinstance(lon, (int, float)) or math.isnan(lon):
        # return {
        #     "how_many_schools": None, 
        #     "how_many_primary_schools": None,
        #     "how_many_secondary_schools": None,
        #     "how_many_kindergarten_schools": None}
        return pd.Series(
            [None], 
            index=["how_many_shops"])
    
    try:
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,fr;q=0.8,fr-FR;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referrer": "https://overpass-turbo.eu/",
        }   
        # (41.879147390418765,12.47677803039551,41.90074384269173,12.50724792480469 # 2.5km #we take 5 km
        # lat+=0.01079822613648318
        # lon+=0.015234947204589844

        query = f"""[out:json];
        node[shop]{lat-0.010,lon-0.015,lat+0.010,lon+0.015};
        out center;"""
        #print(query)
        response = session.post(
            "https://overpass-api.de/api/interpreter",
            headers=headers,
            data = {"data": query}
        ).json()
        #print(response)
        how_many_shops = 0

        for element in response["elements"]:
            if element["tags"]['shop']:
                how_many_shops += 1

        return pd.Series(
            [how_many_shops], 
            index=["how_many_shops"])
    except SystemExit:
        raise SystemExit()
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except BaseException as e:
        print(e)
        return pd.Series(
            [None], 
            index=["how_many_shops"])
    
df = pd.read_csv("csvdump_18k.csv")

batch_size = 200
df_new_columns = None
for i in tqdm(range(0, df.size, batch_size)):
    new_columns = df.iloc[i:min(df.size,i+batch_size)].apply(lambda row: get_shopping(row["latitude"], row["longitude"]), axis=1)
    if df_new_columns is None:
        df_new_columns = new_columns
    else:
        df_new_columns = pd.concat([df_new_columns, new_columns], axis=0)
    df_new_columns.to_csv("csvdump_just_shops_data.csv")

df_new_columns = df_new_columns[["how_many_shops"]]

# concat the new columns with the existing ones
df = pd.concat([df, df_new_columns], axis=1)
df.to_csv("csvdump_with_shops.csv")