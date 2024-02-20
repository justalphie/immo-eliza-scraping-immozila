import json
from scraper.scraper import PropertyScraper
import pandas as pd

def main():

    with open('./data/weblinksimmo_test.json', 'r') as f:
        data = json.load(f)

    columns = ["property_id", "locality_name","property_type","property_subtype","price", "type_of_sale","nb_of_rooms", "area",
                    "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
                    "surface", "surface_area_plot", "nb_of_facades", "swimming_pool", "state_of_building"]
    df = pd.DataFrame(columns=columns)

    # Iterate through each element in the list
    for url in data:
        scrape_url = PropertyScraper(url)
        dataframe_to_print = scrape_url.scrape_property_info()
        df = pd.concat([df, pd.DataFrame(dataframe_to_print)])
    print(df)    
        # print(dataframe_to_print)

if __name__ == "__main__":
    main()