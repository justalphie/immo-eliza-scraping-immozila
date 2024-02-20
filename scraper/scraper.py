import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class PropertyScraper():
    """
    This class scrapes information from a single property url and stores it in a dictionary
    """
    def __init__(self, url):
        self.url = url
        
    def scrape_property_info(self):
        """
        This method scrapes information from a single property URL and stores it in a dictionary
        """
        property_dict = self._fetch_all_info_from_property()
        property_columns = self._create_column_dictionary(property_dict)
        new_data = self.check_sale(property_columns)
        df = pd.concat([df, pd.DataFrame(new_data)])
        return df
    

        

    def _fetch_all_info_from_property(self):
        """
        This private method scrapes information from a single property URL and stores it in a dictionary
        """
        r = requests.get(self.url)
        content = r.content
        
        # parse HTML content
        soup = BeautifulSoup(content, "html.parser")
        
        # find the script tags containing window.classified
        result_data = soup.find_all('script',attrs={"type" :"text/javascript"})
        window_classified_data = None

        for tag in result_data:
            if 'window.classified' in str(tag.string):
                window_classified_data = tag.string

        window_classified_data.strip()            
        window_classified_data = window_classified_data[window_classified_data.find("{"):window_classified_data.rfind("}")+1]

        # storing in a property dictionary
        property_dict = json.loads(window_classified_data)

        # converting to json only for display on commandprompt
        json_property_dict = json.dumps(property_dict, indent=4)
        
        # print(json_property_dict)
        
        return property_dict
        


    def _create_column_dictionary(self, property_dict):
        """
        This private will fetch only the needed columns from the property dictionary and store them in a temporary dictionary
        """
        
        temp_columns_dict = {}

        # property ID
        #print("Property ID: " + str(house_dict['id']))
        temp_columns_dict["property_ID"] = property_dict['id']

        # locality name
        #print("Locality name: " + str(house_dict['property']['location']['locality']))
        temp_columns_dict["locality_name"] = property_dict['property']['location']['locality']

        # Postal code
        #print("Postal code: " + str(house_dict['property']['location']['postalCode']))
        temp_columns_dict["postal_code"] = property_dict['property']['location']['postalCode']

        # Price
        # print("Price: " + str(house_dict['transaction']['sale']['price']))
        #property_dict["price"] = house_dict['transaction']['sale']['price']

        # Type of property (house or apartment)
        # print("Type of property: " + str(house_dict['property']['type']))
        temp_columns_dict["property_type"] = property_dict['property']['type']

        # Subtype of property (bungalow, chalet, mansion, ...)
        #print("Subtype of property: " + str(house_dict['property']['subtype']))
        temp_columns_dict["property_subtype"] = property_dict['property']['subtype']

        # Type of sale (note: exclude life sales)
        #print("Type of Sale: " + str(house_dict['transaction']['type']))
        temp_columns_dict["sale_type"] = property_dict['transaction']['type']

        # Number of rooms
        #print("Number of rooms: " + str(house_dict['property']['roomCount']))
        temp_columns_dict["number_of_rooms"] = property_dict['property']['roomCount']

        # # Living area (area in m²)
        # #print("Living area (m2): " + str(house_dict['property']['livingroom']['surface']))
        # if house_dict['property']['livingRoom']['surface']:
        #     property_dict["living_area"] = house_dict['property']['livingRoom']['surface']
        # else:
        #     property_dict["living_area"] = 0

        # Equipped kitchen (0/1)
        #print("Equipped kitchen: " + str(house_dict['property']['kitchen']['type']))
        # if property_dict['property']['kitchen']['type'] is not None:
        #     columns_dict["equipped_kitchen"] = property_dict['property']['kitchen']['type']
        # else:
        #     columns_dict["equipped_kitchen"] = 0

        # Furnished (0/1)
        #print("Is furnished: " + str(house_dict['transaction']['sale']['isFurnished']))
        if property_dict['transaction']['sale']['isFurnished'] is not None:
            temp_columns_dict["furnished"] = property_dict['transaction']['sale']['isFurnished']
        else:
            temp_columns_dict["furnished"] = 0

        # Open fire (0/1)
        #print("Open fire: " + str(house_dict['property']['fireplaceExists']))
        if property_dict['property']['fireplaceExists'] is not None:
            temp_columns_dict["open_fire"] = property_dict['property']['fireplaceExists']
        else:
            temp_columns_dict["open_fire"] = 0

        # Terrace (area in m² or null if no terrace)
        #print("Terrace (m2): " + str(house_dict['property']['terraceSurface']))
        if property_dict['property']['terraceSurface'] is not None:
            temp_columns_dict["terrace_area"] = property_dict['property']['terraceSurface']
        else:
            temp_columns_dict["terrace_area"] = 0

        # Garden (area in m² or null if no garden)
        # print("Garden (m2): " + str(property_dict['property']['gardenSurface']))
        if property_dict['property']['gardenSurface'] is not None:
            temp_columns_dict["garden_area"] = property_dict['property']['gardenSurface']
        else:
            temp_columns_dict["garden_area"] = 0

        # Surface of good
        #print("Surface of good (m2): " + str(house_dict['property']['land']['surface']))

        # # Number of facades
        # #print("Number of facades: " + str(house_dict['property']['building']['facadeCount']))
        # columns_dict["facade_count"] = property_dict['property']['building']['facadeCount']

        # Swimming pool (0/1)
        # print("Garden (m2): " + str(house_dict[

        # # State of building (new, to be renovated, ...)
        # #print("State of building: " + str(house_dict['property']['building']['condition']))
        # columns_dict["state_of_building"] = property_dict['property']['building']['condition']

        #print(temp_columns_dict)
        return temp_columns_dict
    
    
    def check_data(self, data):
        if data == "null" or data is None:
            return None
        else:
            return data


    def check_kitchen(self, data):
        for keys in data:
            if data[keys] == "null":
                return 0
            else:
                return 1


    # changes boolean into numeric values
    def check_boolean(self, data):
        if data is None or data == "null":
            return None
        elif data == True:
            return 1
        else:
            return 0


    # checks if garden is there and return surface if possible
    def check_garden(self, data):
        if data["hasGarden"] == True:
            return self.check_data(data["gardenSurface"])
        else:
            return "null"


    # Checks if terrace is there and returns thesruface area of it
    def check_terrace(self, data):
        if data["hasTerrace"] == True:
            return self.check_data(data["terraceSurface"])
        else:
            return "null"


    def check_sale(self, dictionary):
        if dictionary["transaction"]["type"] == "FOR_SALE":
            return self.insert_dataframe(dictionary)
        
    
    
    def building_a_dataframe(self):
        
        columns = ["id", "locality","property_type","property_subtype","price", "type_of_sale","nb_rooms", "area",
                "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
                "surface", "surface_area_plot", "nb_facades", "swimming_pool", "state_of_building"]
        df = pd.DataFrame(columns=columns)
        print(df)


    def insert_dataframe(self, data_dictionary):
        
        new_data = [{ "id": self.check_data(data_dictionary["id"]),
                    "locality":self.check_data(data_dictionary["property"]["location"]["locality"]),
                    "postal_code":self.check_data(data_dictionary["property"]["location"]["postalCode"]),
                    "property_type":self.check_data(data_dictionary["property"]["type"]),
                    "property_subtype":self.check_data(data_dictionary["property"]["subtype"]),
                    "price":self.check_data(data_dictionary["price"]["mainValue"]),
                    "type_of_sale":self.data_dictionary["transaction"]["subtype"],
                    "nb_rooms":self.check_data(data_dictionary["property"]["roomCount"]),
                    "area":self.check_data(data_dictionary["property"]["netHabitableSurface"]),
                    "fully_equipped_kitchen":self.check_kitchen(data_dictionary["property"]["kitchen"]),
                    "furnished":self.check_boolean(data_dictionary["transaction"]["sale"]["isFurnished"]),
                    "open_fire":self.check_boolean(data_dictionary["property"]["fireplaceExists"]),
                    "terrace":self.check_boolean(data_dictionary["property"]["hasTerrace"]),
                    "terrace_area":self.check_terrace(data_dictionary["property"]),
                    "garden":self.check_boolean(data_dictionary["property"]["hasGarden"]),
                    "garden_area":self.check_garden(data_dictionary["property"]),
                    "surface_of_good":0,
                    "nb_facades":self.check_data(data_dictionary["property"]["building"]["facadeCount"]),
                    "swimming_pool":self.check_boolean(data_dictionary["property"]["hasSwimmingPool"]),
                    "state_of_building":self.check_data(data_dictionary["property"]["building"]["condition"])
        }]
        
        return new_data

