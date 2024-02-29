import concurrent.futures
import json
import functools
from scraper.scraper import PropertyScraper
import pandas as pd
import requests
import time

from scraper.threathimmolinks import multiWeblinks
from scraper.threathimmolinks import write_json

def process_url(url, session):
    """
    Processes a URL and returns a dataframe with the scraped data.

    :param url: url to scrape
    :param session: session to use
    :return: dataframe with scraped data
    """
    scrape_url = PropertyScraper(url, session)
    dataframe_to_print = scrape_url.scrape_property_info()
    
    return pd.DataFrame(dataframe_to_print) if dataframe_to_print is not None else None

def main():
    

    weblinks = multiWeblinks()
    write_json(list(set(weblinks)))

    with open('./data/raw/raw_weblinksimmo.json', 'r') as f:
        data = json.load(f)

    columns = ["property_id", "locality_name", "postal_code", "street_name", "house_number", "latitude", "longitude", 
                    "property_type", "property_subtype", "price", "type_of_sale", "number_of_rooms", "living_area", "kitchen_type",
                    "fully_equipped_kitchen", "furnished", "open_fire","terrace", "terrace_area","garden", "garden_area",
                    "surface_of_good", "number_of_facades", "swimming_pool", "state_of_building"]
    df = pd.DataFrame(columns=columns)

    with requests.Session() as session:
    # Use ThreadPoolExecutor to parallelize the URL processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use functools.partial to pass the session as an argument
            partial_process_url = functools.partial(process_url, session=session)

        # Process each URL asynchronously
            futures = [executor.submit(partial_process_url, url) for url in data]

        # Collect the results as they become available
            for future in concurrent.futures.as_completed(futures):
                result_df = future.result()
                if result_df is not None:
                    df = pd.concat([df, result_df])
    print(df)    
    df.to_csv("./data/cleaned/clean.csv", sep=',', index=False, encoding='utf-8')    

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()

    total_time = end_time - start_time
    print(total_time)