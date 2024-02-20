import requests
from bs4 import BeautifulSoup
import json
import re
    
def immolinks(n):
    """
    Starting from a root_url fetches the immoweb links for n pages
    """
    links=[]
    weblinks=[]
    root_url = "https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page="

    for number in range(1, n+1):
        pages_url = f"{root_url}{number}&orderBy=relevance"
        r = requests.get(pages_url)
        print(pages_url, r.status_code)
        soup = BeautifulSoup(r.content, "html.parser")

        for contentmain in soup.find_all("div",{"class":"container-main-content"}):

            for a in contentmain.find_all("a", {"class":"card__title-link"}):
                    links.append(a)
        
        for id, i in enumerate(links):
            text = str(i)
            pattern = r'href="([^"]*)"'
            match = re.search(pattern, text)
            if match:
                result = match.group(1)
                weblinks.append(result)
    
    print(weblinks)

    # number of weblinks fetched from the pages
    print(len(weblinks))
    write_json(weblinks)
    
    return weblinks


def write_json(weblinks):
    """
    Write the immoweb links to a csv file
    """
    with open("./data/weblinksimmo.json", 'w') as output_file:
        print(json.dumps(weblinks, indent=2), file=output_file)

if __name__ == "__main__":
    immolinks(50)