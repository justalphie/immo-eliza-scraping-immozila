import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expectedconditions as EC
from bs4 import BeautifulSoup
import requests
import re

def getwebsite():
    teller = 0
    url = ""
    count = 0
    links = []
    weblinks=[]
    options = webdriver.FirefoxOptions()
    #options.addargument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.immoweb.be/nl")
    #driver.maximizewindow()
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
        for a in contentmain.find_all("a", {"class":"cardtitle-link"}):
                links.append(a)
    for id, i in enumerate(links):
        text = str(i)
        pattern = r'href="([^"]*)"'
        match = re.search(pattern, text)
        if match:
            result = match.group(1)
            weblinks.append(result)
            teller += 1
    driver.close()
    print(weblinks)
    return weblinks


if __name__ == "__main":
    get_website()
