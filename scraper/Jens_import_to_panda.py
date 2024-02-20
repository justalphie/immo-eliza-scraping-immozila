import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

### NATHALIE CODE TO FETCH JSON

url = "https://www.immoweb.be/nl/zoekertje/huis/te-koop/godinne/5530/10882096"

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


#### END NATHALIE CODE


#create dataframe
columns = ["id", "locality","property_type","property_subtype","price", "type_of_sale","nb_rooms", "area",
           "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
           "surface", "surface_area_plot", "nb_facades", "swimming_pool", "state_of_building"]
df = pd.DataFrame(columns=columns)


#### NEW CODE

def check_data(data):
    if data == "null" or data is None:
        return None
    else:
        return data

def check_kitchen(data):
    for keys in data:
        if data[keys] == "null":
            return 0
        else:
            return 1

# changes boolean into numeric values
def check_boolean(data):
    if data is None or data == "null":
        return None
    elif data == True:
        return 1
    else:
        return 0

# checks if garden is there and return surface if possible
def check_garden(data):
    if data["hasGarden"] == True:
        return check_data(data["gardenSurface"])
    else:
        return "null"

# Checks if terrace is there and returns thesruface area of it
def check_terrace(data):
    if data["hasTerrace"] == True:
        return check_data(data["terraceSurface"])
    else:
        return "null"


def check_sale(dictionary):
    if dictionary["transaction"]["type"] == "FOR_SALE":
        return insert_dataframe(dictionary)




####END NEW CODE


# Creates and returns record to put into DataFrame
def insert_dataframe(data_dictionary):
    
    new_data = [{ "id": check_data(data_dictionary["id"]),
                "locality":check_data(data_dictionary["property"]["location"]["locality"]),
                "postal_code":check_data(data_dictionary["property"]["location"]["postalCode"]),
                "property_type":check_data(data_dictionary["property"]["type"]),
                "property_subtype":check_data(data_dictionary["property"]["subtype"]),
                "price":check_data(data_dictionary["price"]["mainValue"]),
                "type_of_sale":data_dictionary["transaction"]["subtype"],
                "nb_rooms":check_data(data_dictionary["property"]["roomCount"]),
                "area":check_data(data_dictionary["property"]["netHabitableSurface"]),
                "fully_equipped_kitchen":check_kitchen(data_dictionary["property"]["kitchen"]),
                "furnished":check_boolean(data_dictionary["transaction"]["sale"]["isFurnished"]),
                "open_fire":check_boolean(data_dictionary["property"]["fireplaceExists"]),
                "terrace":check_boolean(data_dictionary["property"]["hasTerrace"]),
                "terrace_area":check_terrace(data_dictionary["property"]),
                "garden":check_boolean(data_dictionary["property"]["hasGarden"]),
                "garden_area":check_garden(data_dictionary["property"]),
                "surface_of_good":100,
                "nb_facades":check_data(data_dictionary["property"]["building"]["facadeCount"]),
                "swimming_pool":check_boolean(data_dictionary["property"]["hasSwimmingPool"]),
                "state_of_building":check_data(data_dictionary["property"]["building"]["condition"])
    }]
    

    return new_data


columns = ["id", "locality","property_type","property_subtype","price", "type_of_sale","nb_rooms", "area",
           "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
           "surface", "surface_area_plot", "nb_facades", "swimming_pool", "state_of_building"]



new_data = check_sale(house_dict)
df = pd.concat([df, pd.DataFrame(new_data)])
print(df)
