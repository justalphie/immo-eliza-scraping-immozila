import haversine as hs
from haversine import Unit
import pandas as pd
import requests
import math




def get_restaurants(lat, lon):

    if not isinstance(lat, (int, float)) or math.isnan(lat) or not isinstance(lon, (int, float)) or math.isnan(lon):
        # return {
        #     "how_many_schools": None, 
        #     "how_many_primary_schools": None,
        #     "how_many_secondary_schools": None,
        #     "how_many_kindergarten_schools": None}
        return pd.Series(
            [None], 
            index=["how_many_restaurants"])
    
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
        node[amenity = 'restaurant']{lat-0.010,lon-0.015,lat+0.010,lon+0.015};
        out center;"""
        #print(query)
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            headers=headers,
            data = {"data": query}
        ).json()
        print(response)
        how_many_restaurants = 0
        
        for element in response["elements"]:
            if element["tags"]['amenity'] == "restaurant":
                how_many_restaurants +=1

        return pd.Series(
            [how_many_restaurants], 
            index=["how_many_restaurants"])
    except:
        return pd.Series(
            [None], 
            index=["how_many_restaurants"])
    
df = pd.read_csv("csvdump_with_shops.csv")

new_columns = df.apply(lambda row: get_restaurants(row["latitude"], row["longitude"]), axis=1)
df = pd.concat([df, new_columns], axis=1)


# Print the updated dataframe
#print(df)

df.to_csv("csvdump_with_restaurants.csv")