import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import re

def get_website():
    c = 2
    pages = 4
    teller = 0
    url = ""
    links = []
    weblinks=[]


    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.immoweb.be/nl")
    driver.maximize_window()
    time.sleep(5)
    shadow_host = driver.find_element(By.ID, 'usercentrics-root')
    script = 'return arguments[0].shadowRoot'
    shadow_root = driver.execute_script(script, shadow_host)
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, 'button.sc-dcJsrY:nth-child(2)')
    shadow_content.click()
    time.sleep(5)
    findlist = driver.find_element(By.CSS_SELECTOR, "#searchBoxSubmitButton > span:nth-child(1)")
    findlist.click()
    url = driver.current_url
    print(url)


    r = requests.get(url)
    print(url, r.status_code)
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
            teller += 1
    print(weblinks)

    while c < pages:
        button = driver.find_element(By.XPATH(""));
        button.click()
        url = driver.current_url
        r = requests.get(url)
        print(url, r.status_code)
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
                teller += 1
        c += 1
        print(weblinks)
        
    return weblinks
    

if __name__ == "__main__":
    get_website()