from bs4 import BeautifulSoup
import concurrent
import json
import requests


def immo_pagelinks(n):
    """
    Starting from a root_url fetches the immoweb links for n pages
    """
    immopagelinks=[]
    root_url = "https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page="

    for number in range(1, n+1):
        immopagelinks.append(f"{root_url}{number}&orderBy=relevance")
    return immopagelinks


def immo_weblinks(pages_url):
    weblinks=[]
    seen_links = set()

    with requests.Session() as session:
        r = session.get(pages_url)
        soup = BeautifulSoup(r.content, "html.parser")
        
        for contentmain in soup.find_all("div", {"class": "container-main-content"}):
            
            for a in contentmain.find_all("a", {"class": "card__title-link"}):
                link = a.get('href')
                if link and link not in seen_links:
                    seen_links.add(link)
                    weblinks.append(link)
    print("done")
    return weblinks


def write_json(weblinks):
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


def multiWeblinks():
    page_links = immo_pagelinks(170)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(immo_weblinks, page_links))

    weblinks = []
    
    for sublist in results:
        for link in sublist:
            weblinks.append(link)

    return weblinks


if __name__ == "__main__":
    weblinks = multiWeblinks()
    write_json(weblinks)
    write_json_houses(weblinks)
    write_json_appartment(weblinks)