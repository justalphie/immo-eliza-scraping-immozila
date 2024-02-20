import requests
from bs4 import BeautifulSoup
import json
import re
    
def immolinksall(n):
    """
    Starting from a root_url fetches the immoweb links for n pages
    """
    weblinks=[]
    root_url = "https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page="

    seen_links = set()

    for number in range(1, n+1):
        pages_url = f"{root_url}{number}&orderBy=relevance"
        r = requests.get(pages_url)
        print(pages_url, r.status_code)
        soup = BeautifulSoup(r.content, "html.parser")

        for contentmain in soup.find_all("div", {"class": "container-main-content"}):
            for a in contentmain.find_all("a", {"class": "card__title-link"}):
                link = a.get('href')
                if link and link not in seen_links:
                    seen_links.add(link)
                    weblinks.append(link)
    
    print(weblinks)

    # number of weblinks fetched from the pages
    print(len(weblinks))
    write_json(weblinks)
    write_json_houses(weblinks)
    write_json_appartment(weblinks)
    
    return weblinks


def write_json(weblinks):
    """
    Write the immoweb links to a csv file
    """
    with open("./data/weblinksimmo.json", 'w') as output_file:
        print(json.dumps(weblinks, indent=2), file=output_file)

def write_json_houses(weblinks):
    filtered_links = [link for link in weblinks if "huis" in link.lower() or "villa" in link.lower() or "herenhuis" in link.lower()]

    with open("./data/weblinksimmohouse.json", 'w') as output_file:
        json.dump(filtered_links, output_file, indent=2)

def write_json_appartment(weblinks):
    filtered_links = [link for link in weblinks if "appartement" in link.lower() or "studio" in link.lower()]

    with open("./data/weblinksimmoappartment.json", 'w') as output_file:
        json.dump(filtered_links, output_file, indent=2)

if __name__ == "__main__":
    immolinksall(3)