import os.path
import pandas as pd
import math

#pip install pgeocode # normally, this would suffice to install modules

# I had to use the below code to circumvent Duke's firewall
#conda config --set ssl_verify no
#conda config --add channels conda-forge
#conda install pgeocode
#conda install pycountry

import pgeocode
import pycountry as pc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
options=webdriver.ChromeOptions()
import time
import pandas as pd
#conda install geopy
from geopy import geocoders
from geopy.geocoders import Nominatim

#make sure to install chromedriver
driver = webdriver.Chrome('C:/Users/pdennis/Documents/Python Projects/AJE/chromedriver.exe', chrome_options=options)

#this is the webpage to look up defunct zip codes
webpage="https://uszipcodesbystate.com"

# set directory
os.chdir('U:/Python Projects/Zip Codes/')

# import zip codes
zips = pd.read_excel (r'Cntl_zipCode_NeedLatLong_10orMore_Paul.xlsx')

#defining the country code for the pgeocode module
country = pgeocode.Nominatim('us')

# defining custom function "geocodes" to return coordinates from zip codes
def geocodes(zipcodes):
    zipcodes=int(zipcodes)
    location = country.query_postal_code(zipcodes)
    latitude=location.latitude
    longitude=location.longitude
    state=location.state_code
    outsideUS=""
    if math.isnan(latitude): #if latitude not available, search through defunct zip codes
        #open link
        driver.get(webpage)
            
        #submit search results for zip
        driver.find_element_by_name("query").send_keys(zipcodes)
        submit=driver.find_element_by_id("edit-submit-zip").click()

        #looks for location, stores it if available
        element = driver.find_elements_by_class_name('view-content')
        if len(element) > 0:
            location=element[0].text
            locations = location.split(": ")
            
            city=locations[2].replace('Place Name: ','').replace('State','').strip() 
            state=locations[3][-3:-1]
            citystate=city + ", " + state          

            geolocator = Nominatim(user_agent="getcoords")
            location = geolocator.geocode(citystate)
            latitude=location.latitude
            longitude=location.longitude
            outsideUS=""
        
        else: #search through other countries for postal code
            dfs = {}
            for i in pgeocode.COUNTRIES_VALID:
                nomi = pgeocode.Nominatim(i)
                df = nomi.query_postal_code(zipcodes)
                #the dfs dataframe contains data from all available countries
                dfs[i] = df
   
            #the below code returns countries with positive matches on the postal code
            countries=[]
            for v in dfs.values():
                altcountry=(v[1])
                if pd.isnull(altcountry)==False:
                    altcountry=pc.countries.get(alpha_2=altcountry).name #converting country codes to names
                    countries.append(altcountry)
    
            outsideUS = [x for x in countries if pd.isnull(x) == False and x!='US']
    return [zipcodes, latitude, longitude, state, outsideUS]

# storing results for all zip codes from zips dataset in "output" dataframe
output=zips['ZIPCODE'].map(geocodes).to_frame()

driver.close()

# splitting out single column to multiple columns and storing in "results" dataframe
results=pd.DataFrame(output['ZIPCODE'].to_list(), columns=['Zip Codes','Latitude', 'Longitude', 'State', 'Outside US?'])

#replacing nan with blanks
results.fillna('', inplace=True)

results.to_csv(r'Coordinates.csv', index = False)