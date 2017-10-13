# Cherie Chung, 10/13/2017
# Scraper written to pull all needed information about each country from this website:
# http://www.ffinetwork.org/country_profiles/

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Create list of column names and empty pandas dataframe
columns = ['Country', 'Availability in food supply (grams/capita/day)', '% produced in industrial mills',
           '% of industrially milled product fortified',
           'Availability in food supply (grams/capita/day)', '% produced in industrial mills',
           '% of industrially milled product fortified',
           'Availability in food supply (grams/capita/day)', '% produced in industrial mills',
           '% of industrially milled product fortified', ]
data = pd.DataFrame(columns=columns)

# Check that 10 columns are created
# print(data.shape)

# loop through all countries using Beautiful Soup and return data
num = 0
for start in range(1, 300, 1):
    country_data = []
    page = requests.get('http://www.ffinetwork.org/country_profiles/' + 'country.php?record=' + str(start))
    time.sleep(1)  # ensuring at least 1 second between page grabs
    soup = BeautifulSoup(page.text, 'lxml', from_encoding='utf-8')
    soup.prettify()
    heading = str(soup.h1)
    country = (heading.split(" <?echo", 1)[0]).split("Profile - ", 1)[1]
    # Return to beginning of loop if no country listed (since page will be empty)
    if len(country) < 1:
        continue
    country_data.append(country)
    table = soup.find_all('table')[0]
    table2 = soup.find_all('table')[1]
    food = ['wheat', 'maize', 'rice']
    attr1 = 'db-grain_avail_'
    attr2 = 'db-prop_ind_'
    attr3 = 'db-prop_milled_fortified'
    for item in food:
        c1 = attr1 + item
        c2 = attr2 + item
        availability = table.find_all(name='td', attrs={'id': str(c1)})
        for b in availability:
            country_data.append(b.text)
        percent_produced = table2.find_all(name='td', attrs={'id': str(c2)})
        for c in percent_produced:
            country_data.append(c.text)
        percent_fortified = table2.find_all(name='td', attrs={'id': str(attr3)})
        for d in percent_fortified:
            if item.title() in str(d.parent.text):
                country_data.append(d.text)
    num += 1
    data.loc[num] = country_data

print(data.to_csv("ScrapedFFIdata.csv"))
