import pandas as pd
import requests
import math


def get_coordinates(number, street, postalcode):
    root_url = "https://nominatim.openstreetmap.org/search?"
    params = {"street": str(number)+" "+ street,
            "country": "belgium",
            "postalcode": str(postalcode),
            "format": "jsonv2",
            "addressdetails":"1"}
    print(params)
    response = requests.get(root_url, params=params)
    data = response.json()
    
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    type = data[0]["type"]
    return lat, lon, type

def get_address(lat, lon, postalcode):
    root_url = "https://nominatim.openstreetmap.org/search?"
    params = {"street": str(number)+" "+ street,
            "country": "belgium",
            "postalcode": str(postalcode),
            "format": "jsonv2",
            "addressdetails":"1"}
    print(params)
    response = requests.get(root_url, params=params)
    data = response.json()
    housenumber = data[0]["address"]["house_number"]


df = pd.read_csv("csvdump.csv")
print(df)

print(df[df['latitude'] == None])

print(df.iloc[1,3])

s = "Voetbalstraat"
n = 105
p = 9050

print(get_coordinates(n, s, p))

# {'version': 0.6, 'generator': 'Overpass API 0.7.61.5 4133829e', 'osm3s': {'timestamp_osm_base': '2024-02-21T13:44:51Z', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'}, 'elements': [{'type': 'node', 'id': 11509088910, 'lat': 51.0301866, 'lon': 3.7756311, 'tags': {'addr:city': 'Gentbrugge, Gent', 'addr:housenumber': '67', 'addr:postcode': '9050', 'addr:street': 'Jules Destréelaan', 'amenity': 'school', 'description': 'Buitengewoon Secundair Onderwijs voor jongeren en jongvolwassenen met een beperking.', 'email': 'info@sintgregorius.be', 'language:nl': 'yes', 'name': 'BuSO Sint-Gregorius', 'operator': 'Broeders van Liefde', 'operator:type': 'vzw', 'phone': '+32 9 210 01 50', 'school': 'post_secondary;secondary', 'school:gender': 'mixed', 'school:language': 'Nederlands', 'website': 'https://sintgregorius.be/buso'}}, {'type': 'node', 'id': 11509088911, 'lat': 51.0293129, 'lon': 3.773922, 'tags': {'addr:city': 'Gentbrugge, Gent', 'addr:housenumber': '67', 'addr:postcode': '9050', 'addr:street': 'Jules Destréelaan', 'amenity': 'school', 'description': 'Buitengewoon BasisOnderwijs voor kleuters en kinderen met een beperking of leermoeilijkheden.', 'email': 'nadine.vandesompel@gregorius.broedersvanliefde.be', 'language:nl': 'yes', 'name': 'BuBaO Sint-Gregorius', 'operator': 'Broeders van Liefde', 'operator:type': 'vzw', 'phone': '+32 9 210 01 60', 'school': 'kindergarten;primary', 'school:gender': 'mixed', 'website': 'https://sintgregorius.be/bubao'}}]}
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
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            headers=headers,
            data = {"data": query}
        ).json()
        #print(response)
        how_many_schools = 0
        for element in response["elements"]:
            if element["tags"]['amenity'] == 'school':
                how_many_schools +=1

        return pd.Series(
            [how_many_schools], 
            index=["how_many_schools"])
    except:
        return pd.Series(
            [None], 
            index=["how_many_schools"])

#print(get_schools(51.2016514,4.3998097))

# Apply get_schools function to the dataframe
new_columns = df.apply(lambda row: get_schools(row["latitude"], row["longitude"]), axis=1)
df = pd.concat([df, new_columns], axis=1)


# Print the updated dataframe
print(df)

df.to_csv("csvdump_with_schools.csv")