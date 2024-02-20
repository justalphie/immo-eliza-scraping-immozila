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
        This is the main method that scrapes information from a single property URL 
        and stores
        """
        
        property_dict = self._fetch_all_info_from_property()
        scraped_data = self._check_sale(property_dict)
        return scraped_data
    

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
            
    
    def _check_data(self, data):
        if data == "null" or data is None:
            return None
        else:
            return data


    def _check_kitchen(self, data):
        for keys in data:
            if data[keys] == "null":
                return 0
            else:
                return 1


    # changes boolean into numeric values
    def _check_boolean(self, data):
        if data is None or data == "null":
            return None
        elif data == True:
            return 1
        else:
            return 0


    # checks if garden is there and return surface if possible
    def _check_garden(self, data):
        if data["hasGarden"] == True:
            return self._check_data(data["gardenSurface"])
        else:
            return "null"


    # Checks if terrace is there and returns thesruface area of it
    def _check_terrace(self, data):
        if data["hasTerrace"] == True:
            return self._check_data(data["terraceSurface"])
        else:
            return "null"


    def _check_sale(self, dictionary):
        if dictionary["transaction"]["type"] == "FOR_SALE":
            return self._data_to_insert_in_dataframe(dictionary)
        
    def _data_to_insert_in_dataframe(self, data_dictionary):
        
        new_data = [{ "property_id": self._check_data(data_dictionary["id"]),
                    "locality_name":self._check_data(data_dictionary["property"]["location"]["locality"]),
                    "postal_code":self._check_data(data_dictionary["property"]["location"]["postalCode"]),
                    "property_type":self._check_data(data_dictionary["property"]["type"]),
                    "property_subtype":self._check_data(data_dictionary["property"]["subtype"]),
                    "price":self._check_data(data_dictionary["price"]["mainValue"]),
                    "type_of_sale":data_dictionary["transaction"]["subtype"],
                    "nb_of_rooms":self._check_data(data_dictionary["property"]["roomCount"]),
                    "area":self._check_data(data_dictionary["property"]["netHabitableSurface"]),
                    "fully_equipped_kitchen":self._check_kitchen(data_dictionary["property"]["kitchen"]),
                    "furnished":self._check_boolean(data_dictionary["transaction"]["sale"]["isFurnished"]),
                    "open_fire":self._check_boolean(data_dictionary["property"]["fireplaceExists"]),
                    "terrace":self._check_boolean(data_dictionary["property"]["hasTerrace"]),
                    "terrace_area":self._check_terrace(data_dictionary["property"]),
                    "garden":self._check_boolean(data_dictionary["property"]["hasGarden"]),
                    "garden_area":self._check_garden(data_dictionary["property"]),
                    "surface_of_good":0,
                    "nb_of_facades":self._check_data(data_dictionary["property"]["building"]["facadeCount"]),
                    "swimming_pool":self._check_boolean(data_dictionary["property"]["hasSwimmingPool"]),
                    "state_of_building":self._check_data(data_dictionary["property"]["building"]["condition"])
        }]
        
        return new_data