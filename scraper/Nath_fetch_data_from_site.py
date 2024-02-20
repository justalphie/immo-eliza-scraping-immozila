import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# starting from one URL
url = "https://www.immoweb.be/nl/zoekertje/benedenverdieping/te-koop/antwerpen/2100/11150891"

# old URL that said te-koop but was in fact te-huur
# url = "https://www.immoweb.be/nl/zoekertje/appartement/te-koop/perwijs/1360/11144723"
r = requests.get(url)
content = r.content

# parse HTML content
soup = BeautifulSoup(content, "html.parser")

# find all script tags and from there look for windows.classified tag
result_data = soup.find_all('script',attrs={"type" :"text/javascript"})

for tag in result_data:
    if 'window.classified' in str(tag.string):
        window_classified_data = tag

# convert result to string
windows_classified_data = window_classified_data.string

# strip enters
windows_classified_data.strip()
            
windows_classified_data = windows_classified_data[windows_classified_data.find("{"):windows_classified_data.rfind("}")+1]

house_dict = json.loads(windows_classified_data)

json_house_dict = json.dumps(house_dict, indent=4)

# look at the full json
#print(json_house_dict)

#  ---- NEEDED COLUMNS ----

property_dict = {}

# property ID
#print("Property ID: " + str(house_dict['id']))
property_dict["property_dict"] = house_dict['id']

# locality name
#print("Locality name: " + str(house_dict['property']['location']['locality']))
property_dict["locality_name"] = house_dict['property']['location']['locality']

# Postal code
#print("Postal code: " + str(house_dict['property']['location']['postalCode']))
property_dict["postal_code"] = house_dict['property']['location']['postalCode']

# Price
# print("Price: " + str(house_dict['transaction']['sale']['price']))
#property_dict["price"] = house_dict['transaction']['sale']['price']

# Type of property (house or apartment)
# print("Type of property: " + str(house_dict['property']['type']))
property_dict["property_type"] = house_dict['property']['type']

# Subtype of property (bungalow, chalet, mansion, ...)
#print("Subtype of property: " + str(house_dict['property']['subtype']))
property_dict["property_subtype"] = house_dict['property']['subtype']

# Type of sale (note: exclude life sales)
#print("Type of Sale: " + str(house_dict['transaction']['type']))
property_dict["sale_type"] = house_dict['transaction']['type']

# Number of rooms
#print("Number of rooms: " + str(house_dict['property']['roomCount']))
property_dict["number_of_rooms"] = house_dict['property']['roomCount']

# # Living area (area in m²)
# #print("Living area (m2): " + str(house_dict['property']['livingroom']['surface']))
# if house_dict['property']['livingRoom']['surface']:
#     property_dict["living_area"] = house_dict['property']['livingRoom']['surface']
# else:
#     property_dict["living_area"] = 0

# Equipped kitchen (0/1)
#print("Equipped kitchen: " + str(house_dict['property']['kitchen']['type']))
if house_dict['property']['kitchen']['type'] is not None:
    property_dict["equipped_kitchen"] = house_dict['property']['kitchen']['type']
else:
    property_dict["equipped_kitchen"] = 0

# Furnished (0/1)
#print("Is furnished: " + str(house_dict['transaction']['sale']['isFurnished']))
if house_dict['transaction']['sale']['isFurnished'] is not None:
    property_dict["furnished"] = house_dict['transaction']['sale']['isFurnished']
else:
    property_dict["furnished"] = 0

# Open fire (0/1)
#print("Open fire: " + str(house_dict['property']['fireplaceExists']))
if house_dict['property']['fireplaceExists'] is not None:
    property_dict["open_fire"] = house_dict['property']['fireplaceExists']
else:
    property_dict["open_fire"] = 0

# Terrace (area in m² or null if no terrace)
#print("Terrace (m2): " + str(house_dict['property']['terraceSurface']))
if house_dict['property']['terraceSurface'] is not None:
    property_dict["terrace_area"] = house_dict['property']['terraceSurface']
else:
    property_dict["terrace_area"] = 0

# Garden (area in m² or null if no garden)
print("Garden (m2): " + str(house_dict['property']['gardenSurface']))
if house_dict['property']['gardenSurface'] is not None:
    property_dict["garden_area"] = house_dict['property']['gardenSurface']
else:
    property_dict["garden_area"] = 0

# Surface of good
#print("Surface of good (m2): " + str(house_dict['property']['land']['surface']))

# Number of facades
#print("Number of facades: " + str(house_dict['property']['building']['facadeCount']))
property_dict["facade_count"] = house_dict['property']['building']['facadeCount']

# Swimming pool (0/1)
# print("Garden (m2): " + str(house_dict[

# State of building (new, to be renovated, ...)
#print("State of building: " + str(house_dict['property']['building']['condition']))
property_dict["state_of_building"] = house_dict['property']['building']['condition']



#print(property_dict)

df = pd.DataFrame(property_dict, index=[0])

print(df)