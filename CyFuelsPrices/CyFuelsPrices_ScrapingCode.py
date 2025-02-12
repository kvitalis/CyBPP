# Important libraries
import pandas as pd 
import re
import requests
import time
import xlsxwriter
import urllib.request
import json
import tabula as tb
#import PyPDF2
import pypdf
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pdfplumber

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
from tabula import read_pdf

# Ignore specific warning
warnings.simplefilter("ignore")

# Read necessary data
df = pd.read_csv("CyFuelsPrices/CyFuelsPrices_ScrapedData.csv")
urls = pd.read_csv("CyFuelsPrices/CyFuelsPrices_ProductsList.csv")

# Create a null dataframe
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
scraped_data = pd.DataFrame(columns = ["Date","Name","Price","Fuel Type","Subclass","Division","Retailer","District"])

# Define the functions for the web-scraping of the target retailers

def results_FuelDaddy(u):
    
    new_row = []
    price_list = []
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_ = str(Item_url_)
    bs = BeautifulSoup(url_, "html.parser")
    response = requests.get(bs, {'headers':header})
        
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div", {"class":"col-md-7 pump-info-right"})
        for brand_name in element_soup:
            brand = brand_name.find_all(class_ = "col-sm-9")[1]
            for brand_name in brand:
                brand_word = brand_name.get_text(strip = True).upper()
        '''    
        if brand_word:
            if brand_word=="Πετρολίνα" or (brand_word=="ΠΕΤΡΟΛΊΝΑ"):
                brand_word="PETROLINA"
        else:
            brand_word="PETROLINA"
        '''    
        name = element_soup[0].find_all("div",{"class" : "col-sm-9"})
        name_word = name[0].text.strip().replace("\n","")
        element_price = soup.find_all("div", {"class":"price-item"})
        
        for i in range(len(element_price)):
            name = element_price[i].find(class_ = "brandtag cut-text fueltype-heading").get_text(strip = True)
            price = element_price[i].find(class_ = "pricetag").get_text(strip = True).replace(" €","")
            price_list.append(name)
            price_list.append(price)
        
        for i in range(1,len(price_list),2):
            new_row = []
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    
            if price_list[i-1] == 'Unleaded 95':
                new_row.append(name_word)
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Unleaded 95")
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                new_row.append(brand_word) 
                new_row.append(distric_)
                
            elif price_list[i-1] == 'Unleaded 98':
                new_row.append(name_word)
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append('Unleaded 98')
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                new_row.append(brand_word) 
                new_row.append(distric_)
                
            elif price_list[i-1] == 'Diesel':
                new_row.append(name_word)
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append('Diesel')
                new_row.append("Diesel")
                new_row.append("TRANSPORT")
                new_row.append(brand_word) 
                new_row.append(distric_)
                 
            elif price_list[i-1] == 'Heating Diesel':
                new_row.append(name_word)
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append('Heating Diesel')
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                new_row.append(brand_word) 
                new_row.append(distric_)
                   
            elif price_list[i-1] == 'Kerosene':
                new_row.append(name_word)
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append('Kerosene')
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                new_row.append(brand_word) 
                new_row.append(distric_)
            
            scraped_data.loc[len(scraped_data)] = new_row
            scraped_data['Name'] = scraped_data['Name'].apply(lambda x:x)
    
# Initialization of the scraping/processing time
start_time = time.time()

# Run the code
for u in range(0, len(urls)):
    print(u)
    
    # Creative a new row each time 
    new_row = []
    website_false = []
    
    # Read the data
    Item_url_ = urls["Url"].iloc[u]
    name_ = urls["Name"].iloc[u]
    print(name_)
    subclass_ = urls["Subclass"].iloc[u]
    division_ = urls["Division"].iloc[u]
    retailer_ = urls["Retailer"].iloc[u]
    district_  = urls["District"].iloc[u]
    
    if retailer_ == "FuelDaddy":
        results_FuelDaddy(u)  
        
# Change the type as float
scraped_data["Price"].astype(float)

# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/60, "minute")

# Export/Save the scraped data 
df.to_csv("CyFuelsPrices/CyFuelsPrices_ScrapedData.csv", index = False) 

combined_df = pd.concat([df, scraped_data], axis = 0)
combined_df.reset_index(drop = True, inplace = True)
combined_df.to_csv("CyFuelsPrices/CyFuelsPrices_ScrapedData.csv", index = False, header = True)
daily_errors.to_csv("CyFuelsPrices/CyFuelsPrices_DailyScrapingErrors.csv", index = False)
