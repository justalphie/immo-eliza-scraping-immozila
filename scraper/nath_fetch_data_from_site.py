import requests
from bs4 import BeautifulSoup
import json

# starting from one URL
#url = "https://www.immoweb.be/nl/zoekertje/benedenverdieping/te-koop/antwerpen/2100/11150891"
url = "https://www.immoweb.be/nl/zoekertje/appartement/te-koop/perwijs/1360/11144723"
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
print(json_house_dict)

# needed columns

# property ID
#print(house_dict['id'])

# locality name
# print(house_dict['property']['location']['locality'])

# # Postal code
# print(house_dict['property']['location']['postalCode'])

# Price


# Type of property (house or apartment)


# Subtype of property (bungalow, chalet, mansion, ...)


# Type of sale (note: exclude life sales)


# Number of rooms


# Living area (area in m²)


# Equipped kitchen (0/1)


# Furnished (0/1)


# Open fire (0/1)


# Terrace (area in m² or null if no terrace)


# Garden (area in m² or null if no garden)


# Surface of good


# Number of facades


# Swimming pool (0/1)


# State of building (new, to be renovated, ...)