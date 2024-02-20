import json
from scraper.scraper import PropertyScraper
from scraper.threathimmolinks import multiWeblinks
from scraper.threathimmolinks import write_json
from scraper.threathimmolinks import write_csv

def main():
    webklinks = multiWeblinks()
    write_json(webklinks)

    with open('./data/weblinksimmo.json', 'r') as f:
        data = json.load(f)

    # Iterate through each element in the list
    mainl = []
    for url in data:
        scrape_url = PropertyScraper(url)
        x = scrape_url.scrape_property_info()
        mainl.append(x)
    
    write_csv(mainl)


if __name__ == "__main__":
    main()