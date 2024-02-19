import requests
from bs4 import BeautifulSoup
import json

# starting from one URL
url = "https://www.immoweb.be/nl/zoekertje/appartement/te-koop/perwijs/1360/11144723"
r = requests.get(url)
content = r.content

# parse HTML content
soup = BeautifulSoup(content, "html.parser")

# find all script tags and from there look for windows.classified tag
result_data = soup.find_all('script',attrs={"type" :"text/javascript"})

for tag in result_data:
    if 'window.classified' in str(tag.string):
        window_classified_data = tag

# convert result to string
windows_classified_data = window_classified_data.string

# strip enters
windows_classified_data.strip()
            
windows_classified_data = windows_classified_data[windows_classified_data.find("{"):windows_classified_data.rfind("}")+1]

house_dict = json.loads(windows_classified_data)

json_house_dict = json.dumps(house_dict, indent=4)

# look at the full json
print(json_house_dict)

# pick one key from the json and print it's value
print(house_dict['property']['type'])