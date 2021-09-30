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
    if math.isnan(latitude): #if latitude not available, search through other countries for postal code
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

# splitting out single column to multiple columns and storing in "results" dataframe
results=pd.DataFrame(output['ZIPCODE'].to_list(), columns=['Zip Codes','Latitude', 'Longitude', 'State', 'Outside US?'])

results.to_csv(r'Coordinates.csv', index = False)