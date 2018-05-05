import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\Users\Lenovo\chromedriver.exe')
driver.implicitly_wait(30)
driver.maximize_window()

driver.get('https://www.tutorialspoint.com/apache_poi/apache_poi_core_classes.htm')
for id in range(1,7):
    search_fields=driver.find_elements_by_tag_name("h"+str(id))
    for field in search_fields:
        print field.text

