
import json
import pandas as pd

with open("./example_data/te-koop-example.json") as json_file:
    data_dictionary = json.load(json_file)


#create dataframe
columns = ["id", "locality","property_type","property_subtype","price", "type_of_sale","nb_rooms", "area",
           "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
           "surface", "surface_area_plot", "nb_facades", "swimming_pool", "state_of_building"]
df = pd.DataFrame(columns=columns)

def insert_dataframe(data_dictionary):
    
    new_data = [{ "id": data_dictionary["id"],
                "locality":data_dictionary["property"]["location"]["locality"],
                "property_type":data_dictionary["property"]["type"],
                "property_subtype":data_dictionary["property"]["subtype"],
                "price":data_dictionary["price"]["mainValue"],
                "type_of_sale":data_dictionary["transaction"]["type"],
                "nb_rooms":data_dictionary["property"]["roomCount"],
                "area":data_dictionary["property"]["netHabitableSurface"],
                "fully_equipped_kitchen": 1,
                "furnished":data_dictionary["transaction"]["sale"]["isFurnished"],
                "open_fire":data_dictionary["property"]["fireplaceExists"],
                "terrace":data_dictionary["property"]["hasTerrace"],
                "terrace_area":data_dictionary["property"]["terraceSurface"],
                "garden":data_dictionary["property"]["hasGarden"],
                "garden_area":data_dictionary["property"]["hasGarden"],
                "surface":100,
                "surface_area_plot":100,
                "nb_facades":data_dictionary["property"]["building"]["facadeCount"],
                "swimming_pool":data_dictionary["property"]["hasSwimmingPool"],
                "state_of_building":data_dictionary["property"]["building"]["condition"]
    }]
    

    return new_data


columns = ["id", "locality","property_type","property_subtype","price", "type_of_sale","nb_rooms", "area",
           "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
           "surface", "surface_area_plot", "nb_facades", "swimming_pool", "state_of_building"]


new_data = insert_dataframe(data_dictionary)
df = pd.DataFrame(new_data)
df = pd.concat([df, pd.DataFrame(new_data)])
print(df)