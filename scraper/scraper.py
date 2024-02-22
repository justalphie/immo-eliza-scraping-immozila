from bs4 import BeautifulSoup
import json


class PropertyScraper():
    """
    This class scrapes information from a single property url and stores it in a dictionary
    """
    def __init__(self, url, session):
        self.url = url
        self.session = session

    def scrape_property_info(self):
        """
        This is the main method that scrapes information from a single property URL 
        and stores
        """
        property_dict = self._fetch_all_info_from_property()
        if property_dict is not None:
            scraped_data = self._check_sale(property_dict)
            return scraped_data
        else:
            return None
    

    def _fetch_all_info_from_property(self) -> dict:
        """
        This private method scrapes information from a single property URL and stores it in a dictionary
        """
        r = self.session.get(self.url)
        content = r.content
        
        if r.status_code != 200:
            return None

        # parse HTML content
        soup = BeautifulSoup(content, "html.parser")
        
        # find the script tags containing window.classified
        result_data = soup.find_all('script',attrs={"type" :"text/javascript"})
        window_classified_data = None

        for tag in result_data:
            if 'window.classified' in str(tag.string):
                window_classified_data = str(tag.string)
        
        window_classified_data.strip()            
        window_classified_data = window_classified_data[window_classified_data.find("{"):window_classified_data.rfind("}")+1]

        # storing in a property dictionary
        property_dict = json.loads(window_classified_data)

        # converting to json only for display on commandprompt
        json_property_dict = json.dumps(property_dict, indent=4)
        
        # print(json_property_dict)
        
        return property_dict
            
    
    def _clean_data(self, data):
        """
        checks if property parameter is available or if property parameter is empty
        """
        if data is None or data == "null":
            return None
        else:
            return data


    def _get_fully_equiped_kitchen(self, data):
        """
        checks if kitchen is fully equiped
        """
        if data is None or data == "null":
            return None
        else:
            for keys in data:
                if data[keys] == "null":
                    return 0
                else:
                    return 1


    def _convert_to_boolean(self, data):
        """
        changes boolean into numeric values
        """
        if data is None or data == "null":
            return None
        elif data == True:
            return 1
        else:
            return 0


    def _get_garden_surface(self, data):
        """
        checks if garden is there and return surface if possible
        """
        if data["hasGarden"] == True:
            return self._clean_data(data["gardenSurface"])
        else:
            return None


    def _get_terrace_surface(self, data):
        """
        checks if terrace is there and if so returns surface area of it 
        """
        if data["hasTerrace"] == True:
            return self._clean_data(data["terraceSurface"])
        else:
            return None


    def _clean_building(self, data, value):
            if data == "None" or data is None:
                return None
            else:        
                facade_count_value = data[value]
                return facade_count_value


    def _check_sale(self, dictionary):
        """
        checks if property is for sale
        """
        if dictionary["transaction"]["type"] == "FOR_SALE":
            return self._data_to_insert_in_dataframe(dictionary)
        
    def _get_surface_of_good(self, data):
        if data["property"]["land"] == None:
            return None
        else:
            return self._clean_data(data["property"]["land"]["surface"])

        
    def _data_to_insert_in_dataframe(self, data_dictionary):
        """
        building a dictionary with all the scraped data
        """
        new_data = [{ "property_id": self._clean_data(data_dictionary["id"]),
                    "locality_name":self._clean_data(data_dictionary["property"]["location"]["locality"]),
                    "postal_code":self._clean_data(data_dictionary["property"]["location"]["postalCode"]),
                    "streetname":self._clean_data(data_dictionary["property"]["location"]["street"]),
                    "housenumber":self._clean_data(data_dictionary["property"]["location"]["number"]),
                    "latitude":self._clean_data(data_dictionary["property"]["location"]["latitude"]),
                    "longitude":self._clean_data(data_dictionary["property"]["location"]["longitude"]),
                    "property_type":self._clean_data(data_dictionary["property"]["type"]),
                    "property_subtype":self._clean_data(data_dictionary["property"]["subtype"]),
                    "price":self._clean_data(data_dictionary["price"]["mainValue"]),
                    "type_of_sale":data_dictionary["transaction"]["subtype"],
                    "nb_of_rooms":self._clean_data(data_dictionary["property"]["roomCount"]),
                    "area":self._clean_data(data_dictionary["property"]["netHabitableSurface"]),
                    "fully_equipped_kitchen":self._get_fully_equiped_kitchen(data_dictionary["property"]["kitchen"]),
                    "furnished":self._convert_to_boolean(data_dictionary["transaction"]["sale"]["isFurnished"]),
                    "open_fire":self._convert_to_boolean(data_dictionary["property"]["fireplaceExists"]),
                    "terrace":self._convert_to_boolean(data_dictionary["property"]["hasTerrace"]),
                    "terrace_area":self._get_terrace_surface(data_dictionary["property"]),
                    "garden":self._convert_to_boolean(data_dictionary["property"]["hasGarden"]),
                    "garden_area":self._get_garden_surface(data_dictionary["property"]),
                    "surface_of_good":self._get_surface_of_good(data_dictionary),
                    "nb_of_facades":self._clean_building(data_dictionary["property"]["building"], "facadeCount"),
                    "swimming_pool":self._convert_to_boolean(data_dictionary["property"]["hasSwimmingPool"]),
                    "state_of_building":self._clean_building(data_dictionary["property"]["building"], "condition")
        }]
        
        return new_data