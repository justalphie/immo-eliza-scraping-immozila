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
        This is the main method that scrapes information from a single property URL, 
        stores it in a dictionary that is then used to fetch only the needed columns.

        :return: dictionary with needed columns
        """
        property_dict = self._fetch_all_info_from_property()
        if property_dict is not None:
            scraped_data = self._check_sale(property_dict)
            return scraped_data
        else:
            return None
    

    def _fetch_all_info_from_property(self) -> dict:
        """
        This private method scrapes information from a single property URL and stores it in a dictionary.
        A check is included to see if the URL is still responding.

        :return: dictionary with all scraped information
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
        This private method checks if a property parameter is available or empty

        :param data: property parameter
        :return: value of the property parameter
        """
        if data is None or data == "null":
            return None
        else:
            return data


    def _get_fully_equiped_kitchen(self, data):
        """
        This private method checks if the kitchen of the property is fully equiped
        Logic of this method is if all of the kitchen parameters are null a 0 is returned, else 1

        :param data: property parameter
        :return: 1 if fully equiped, 0 if not
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
        This private method changes boolean (True/False) into numeric values (0/1)

        :param data: property parameter
        :return: 1 if True, 0 if False
        """
        if data is None or data == "null":
            return None
        elif data == True:
            return 1
        else:
            return 0


    def _get_garden_surface(self, data):
        """
        This private method checks if the garden parameter is there and return the garden surface if possible

        :param data: property parameter
        :return: garden surface
        """
        if data["hasGarden"] == True:
            return self._clean_data(data["gardenSurface"])
        else:
            return None


    def _get_terrace_surface(self, data):
        """
        This private method checks if a terrace parameter is there and if so it returns the terrace surface area of it 

        :param data: property parameter
        :return: surface of the terrace
        """
        if data["hasTerrace"] == True:
            return self._clean_data(data["terraceSurface"])
        else:
            return None


    def _clean_building(self, data, value):
        """
        This private method checks for a few property parameters if they are available or empty

        :param data: property parameter
        :param value: property parameter
        :return: value of the property parameter
        """
        if data == "None" or data is None:
            return None
        else:        
            type_value = data[value]
            return type_value

        
    def _get_surface_of_good(self, data):
        """
        This private method checks if a surface of good parameter is available and if so returns the value of it

        :param data: property parameter
        :return: surface of good
        """
        if data["property"]["land"] == None or data["property"]["land"] is None:
            return None
        else:
            return self._clean_data(data["property"]["land"]["surface"])


    def _check_sale(self, dictionary):
        """
        This private method checks if property is for sale.

        :param dictionary: the dictionary that is build up with the scraped data of one URL
        :return: dictionary with needed columns which is created in _data_to_insert_in_dataframe
        """
        if dictionary["transaction"]["type"] == "FOR_SALE":
            return self._data_to_insert_in_dataframe(dictionary)
        
        
    def _data_to_insert_in_dataframe(self, data_dictionary):
        """
        This private method is used to build a dictionary with only the needed colums. Methods are used
        to implement certain logic when filling up the dictionary.

        :param data_dictionary: the dictionary that is build up with the scraped data of one URL
        :return: dictionary with needed columns
        """
        new_data = [{ "property_id": self._clean_data(data_dictionary["id"]),
                    "locality_name":self._clean_data(data_dictionary["property"]["location"]["locality"]),
                    "postal_code":self._clean_data(data_dictionary["property"]["location"]["postalCode"]),
                    "street_name":self._clean_data(data_dictionary["property"]["location"]["street"]),
                    "house_number":self._clean_data(data_dictionary["property"]["location"]["number"]),
                    "latitude":self._clean_data(data_dictionary["property"]["location"]["latitude"]),
                    "longitude":self._clean_data(data_dictionary["property"]["location"]["longitude"]),
                    "property_type":self._clean_data(data_dictionary["property"]["type"]),
                    "property_subtype":self._clean_data(data_dictionary["property"]["subtype"]),
                    "price":self._clean_data(data_dictionary["price"]["mainValue"]),
                    "type_of_sale":data_dictionary["transaction"]["subtype"],
                    "number_of_rooms":self._clean_data(data_dictionary["property"]["roomCount"]),
                    "living_area":self._clean_data(data_dictionary["property"]["netHabitableSurface"]),
                    "kitchen_type":self._clean_building(data_dictionary["property"]["kitchen"], "type"),
                    "fully_equipped_kitchen":self._get_fully_equiped_kitchen(data_dictionary["property"]["kitchen"]),
                    "furnished":self._convert_to_boolean(data_dictionary["transaction"]["sale"]["isFurnished"]),
                    "open_fire":self._convert_to_boolean(data_dictionary["property"]["fireplaceExists"]),
                    "terrace":self._convert_to_boolean(data_dictionary["property"]["hasTerrace"]),
                    "terrace_area":self._get_terrace_surface(data_dictionary["property"]),
                    "garden":self._convert_to_boolean(data_dictionary["property"]["hasGarden"]),
                    "garden_area":self._get_garden_surface(data_dictionary["property"]),
                    "surface_of_good":self._get_surface_of_good(data_dictionary),
                    "number_of_facades":self._clean_building(data_dictionary["property"]["building"], "facadeCount"),
                    "swimming_pool":self._convert_to_boolean(data_dictionary["property"]["hasSwimmingPool"]),
                    "state_of_building":self._clean_building(data_dictionary["property"]["building"], "condition")
        }]
        
        return new_data