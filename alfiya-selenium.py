import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_properties_urls():
    properties_urls=[]
    options = webdriver.FirefoxOptions()
    #options.addargument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.immoweb.be/nl")
    #driver.maximizewindow()
    time.sleep(5)
    shadow_host = driver.find_element(By.ID, 'usercentrics-root')
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
    accept_button = shadow_root.find_element(By.CSS_SELECTOR, 'button.sc-dcJsrY:nth-child(2)')
    accept_button.click()
    time.sleep(5)

    start_search_button = driver.find_element(By.CSS_SELECTOR, "#searchBoxSubmitButton > span:nth-child(1)")
    start_search_button.click()

    while len(properties_urls) < 500:

        search_results = driver.find_element(By.ID, 'searchResults')
        card_links = search_results.find_elements(By.CSS_SELECTOR, '.card__title-link')
        for link in card_links:
            properties_urls.append(link.get_attribute('href'))

        next_page_buttons = driver.find_elements(By.CSS_SELECTOR, ".search-results__pagination .pagination__link--next")
        if len(next_page_buttons) > 0:
            next_page_buttons[0].click()
            time.sleep(2)
        else:
            break

    driver.close()
    return properties_urls



if __name__ == "__main__":
    properties_urls= get_properties_urls()
    with open("list_of_links.json", "w", encoding="utf-8") as f:
        json.dump(properties_urls, f)
