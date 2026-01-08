#!/usr/bin/python3

'''
Crawl and scrape xml URLs based on PPNs (Pica-Produktionsnummer) of manuscripts at StaBi Berlin
(c) 2023, Florian Jäckel
'''

# import libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# setup selenium

driver_location = "/home/chromedriver"

options = Options()
options.add_argument("--headless=new")

#driver = webdriver.Chrome()
driver = webdriver.Chrome(driver_location, options=options)

# base variables

'''
The following two variables are based on this procedure:
- visit "https://digital.staatsbibliothek-berlin.de/"
- chose "Christlich-orientalische Handschriften"
- search "languages:syr"
- check number of pages
'''
number_of_pages = 9
base_url = "https://digital.staatsbibliothek-berlin.de/suche?category%5B0%5D=Christlich-orientalische%20Handschriften&queryString=languages%3Asyr&fulltext=&junction=&current_page="

mets_base_url = "https://content.staatsbibliothek-berlin.de/dc/"
mets_extension = ".mets.xml"

# generate list of URLs to mets xml files based on PPNs

ppns = []

for page in range(1, number_of_pages + 1):

    driver.get(base_url + str(page))

    time.sleep(5)

    titles = driver.find_elements(By.XPATH, value="//div[@class='resultlist-entry-title']")
    
    ppns += [title.get_attribute("rel") for title in driver.find_elements(by=By.CLASS_NAME, value="resultlist-entry-title")]

output = open("xml_urls", "w")
output.write("\n".join(mets_base_url + ppn + mets_extension for ppn in ppns))
output.close()
