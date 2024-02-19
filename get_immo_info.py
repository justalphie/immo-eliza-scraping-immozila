from bs4 import BeautifulSoup
import requests
import re
import json 

web_url = "https://www.immoweb.be/nl/zoekertje/appartement/te-koop/willebroek/2830/11148474"

def get_immo_info(web_url):

    r = requests.get(web_url)

    content = r.content

    soup = BeautifulSoup(content)

    json_file = soup.find_all('script')[1].text

    pattern = r'\[([^]]+)\]'

    json_regex = re.findall(pattern, json_file)
    json_dict = json.load(json_regex[0])
    
    print(json_dict)
    with open("immo.txt", "w") as file:
        file.write(json_regex[0])    

get_immo_info(web_url)