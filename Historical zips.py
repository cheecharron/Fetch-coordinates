from selenium import webdriver
from selenium.webdriver.common.keys import Keys
options=webdriver.ChromeOptions()
import time
import pandas as pd
#conda install geopy
from geopy import geocoders
from geopy.geocoders import Nominatim

zip=85227

#make sure to install chromedriver
driver = webdriver.Chrome('C:/Users/pdennis/Documents/Python Projects/AJE/chromedriver.exe', chrome_options=options)

webpage="https://uszipcodesbystate.com"

#open link
driver.get(webpage)
            
#submit search results for zip
driver.find_element_by_name("query").send_keys(zip)
submit=driver.find_element_by_id("edit-submit-zip").click()

#looks for location, stores it if available
element = driver.find_elements_by_class_name('view-content')
if len(element) > 0:
    location=element[0].text
    locations = location.split(": ")

    city=locations[2].replace('Place Name: ','').replace('State','').strip() 
    state=locations[3][-3:-1]
    citystate=city + ", " + state
    
    driver.close()

    geolocator = Nominatim(user_agent="getcoords")
    location = geolocator.geocode(citystate)
    lat=location.latitude
    long=location.longitude



