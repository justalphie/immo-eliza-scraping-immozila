import haversine as hs
from haversine import Unit
import pandas as pd
import requests
import math
from requests import Session
from tqdm import tqdm

session = Session()

def calculate_distance(loc1, loc2):
    dist = hs.haversine(loc1, loc2, unit=Unit.METERS)/1000
    return dist


def get_schools(lat, lon):

    if not isinstance(lat, (int, float)) or math.isnan(lat) or not isinstance(lon, (int, float)) or math.isnan(lon):
        # return {
        #     "how_many_schools": None, 
        #     "how_many_primary_schools": None,
        #     "how_many_secondary_schools": None,
        #     "how_many_kindergarten_schools": None}
        return pd.Series(
            [None], 
            index=["how_many_schools"])
    
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
        node[amenity=school]{lat-0.010*2,lon-0.015*2,lat+0.010*2,lon+0.015*2};
        out center;"""
        #print(query)
        response = session.post(
            "https://overpass-api.de/api/interpreter",
            headers=headers,
            data = {"data": query}
        ).json()
        #print(response)
        how_many_schools = 0
        distances = [2.5]
        for element in response["elements"]:
            if element["tags"]['amenity'] == 'school':
                how_many_schools +=1

                loc1 = (lat, lon)
                loc2 = (element["lat"], element["lon"])
                dist = calculate_distance(loc1, loc2)
                distances.append(dist)

        minimal_dist = round(min(distances), 3)

        if minimal_dist >= 2.5: minimal_dist = None

        return pd.Series(
            [how_many_schools, minimal_dist], 
            index=["how_many_schools", "closest_school"])
    except SystemExit:
        raise SystemExit()
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except BaseException as e:
        print(e)
        return pd.Series(
            [None, None], 
            index=["how_many_schools", "closest_school"])
    
df = pd.read_csv("csvdump_18k.csv")

batch_size = 200
df_new_columns = None
for i in tqdm(range(0, df.size, batch_size)):
    new_columns = df.iloc[i:min(df.size,i+batch_size)].apply(lambda row: get_schools(row["latitude"], row["longitude"]), axis=1)
    if df_new_columns is None:
        df_new_columns = new_columns
    else:
        df_new_columns = pd.concat([df_new_columns, new_columns], axis=0)
    df_new_columns.to_csv("csvdump_just_schools_data.csv")

df = pd.concat([df, new_columns], axis=1)


# Print the updated dataframe
print(df)

df.to_csv("csvdump_with_schools_18_k.csv")