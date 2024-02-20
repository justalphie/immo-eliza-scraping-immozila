import json
from scraper.scraper import PropertyScraper

def main():

    with open('./data/weblinksimmo_test.json', 'r') as f:
        data = json.load(f)

    # Iterate through each element in the list
    for url in data:
        scrape_url = PropertyScraper(url)
        dataframe_to_print = scrape_url.scrape_property_info()
        print(dataframe_to_print)

if __name__ == "__main__":
    main()