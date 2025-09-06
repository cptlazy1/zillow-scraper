from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

zillow_url = "https://appbrewery.github.io/Zillow-Clone/"
google_forms_url = "https://docs.google.com/forms/d/e/1FAIpQLScbEZ1vxX1uoeb8np6aCRdoEs9fGAxSE2uYMAKv6CnHU4zHtw/viewform?usp=dialog"

firefox_options = webdriver.FirefoxOptions()
firefox_options.set_preference("detach", True)

zillow_driver = webdriver.Firefox(options=firefox_options)
zillow_driver.get(zillow_url)

g_forms_driver = webdriver.Firefox(options=firefox_options)
g_forms_driver.get(google_forms_url)

soup = BeautifulSoup(zillow_driver.page_source, "html.parser")

# Get all the links and put them in a list
link_list = [link['href'] for link in soup.select('a.property-card-link')]

# Get all the prices and put them in a list
rent_list = soup.find_all("span", attrs={"data-test": "property-card-price"})
clean_rent_list = []
for rent in rent_list:
    parts = re.split(r"[+/]", rent.text)
    price = parts[0].strip()
    clean_rent_list.append(price)

# Get all the addresses and put them in a list
address_list = soup.find_all("address", attrs={"data-test": "property-card-addr"})
clean_address_list = []
for address in address_list:
    clean_address_list.append(address.text.strip())

# Use Selenium to fill out the Google Form
for i in range(len(link_list)):
    sleep(3)
    try:
        address_field = WebDriverWait(g_forms_driver, 3).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[aria-labelledby="i1 i4"]')
            )
        )

        address_field.clear()
        address_field.send_keys(clean_address_list[i])

        rent_field = WebDriverWait(g_forms_driver, 5).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[aria-labelledby="i6 i9"]')
            )
        )
        rent_field.clear()
        rent_field.send_keys(clean_rent_list[i])

        link_field = WebDriverWait(g_forms_driver, 4).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[aria-labelledby="i11 i14"]')
            )
        )
        link_field.clear()
        link_field.send_keys(link_list[i])

        submit_button = WebDriverWait(g_forms_driver, 3).until(
            ec.presence_of_element_located(
                (By.XPATH, "//span[normalize-space()='Verzenden']")
            )
        )
        submit_button.click()

        submit_another_response_link = WebDriverWait(g_forms_driver, 6).until(
            ec.presence_of_element_located(
                (By.LINK_TEXT, "Nog een antwoord verzenden")
            )
        )
        submit_another_response_link.click()


    except TimeoutException:
        print("Timeout")
zillow_driver.quit()
