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
df = pd.read_csv("Datasets/Raw-Data-24q4.csv")
#df = pd.read_csv("Datasets/Raw-Data-2025Q1.csv")
#df = pd.read_csv("Datasets/Raw-Data.csv")
urls = pd.read_csv("Datasets/Daily-Scraping-Errors.csv")

# Create a null data frame
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns = ["Date","Name","Price","Subclass","Division","Retailer"])

# Define the web-scraping functions for the target retailers

def results_supermarketcy(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url_new = "https://www.supermarketcy.com.cy/" + str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs,{'headers':header})
           
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        name_wrappers = soup.find('h1', {'class':"text-h6 md:text-h4 text-gray-dark font-bold mb-8 lg:mb-40 lg:max-w-520 leading-snug italic"}).text
        price_wrappers = soup.find('div', {'class':"text-primary text-24 lg:text-h3 font-bold italic my-4 lg:my-8"}).text
        value = price_wrappers.split('\xa0')[0].replace('.', '').replace(',', '.')
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_wrappers)
        new_row.append(float(value))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("SupermarketCy")
        list_.loc[len(list_)] = new_row
        list_["Name"] =list_["Name"].apply(lambda x:x)

'''
def results_alphamega(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header})
           
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div",{"class":"content-row__item__body padding-size-none padding-position-around margin-sm margin-position- dw-mod"})
        # Extract the script tag content
        script_tag = element_soup[0].find('script')
        if script_tag:
            script_content = script_tag.string or script_tag.get_text()
            # Use regex to extract 'ecomm_totalvalue'
            match = re.search(r"'ecomm_totalvalue':\s*([\d.]+)", script_content)
            if match:
                total_value = float(match.group(1))
                print(total_value)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(total_value)
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Alphamega")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)   
'''

def results_fuelDaddy(u):
    
    new_row=[]
    price_list=[]
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_new = "https://www.fueldaddy.com.cy/" + str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs, {'headers':header})
        
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div", {"class":"col-md-7 pump-info-right"})
        for brand_name in element_soup:
            brand = brand_name.find_all(class_ = "col-sm-9")[1]
            for brand_name in brand:
                brand_word = brand_name.get_text(strip = True).upper()
            
        if brand_word:
            if brand_word=="Πετρολίνα" or (brand_word=="ΠΕΤΡΟΛΊΝΑ"):
                brand_word="PETROLINA"
        else:
            brand_word="PETROLINA"
            
        name = element_soup[0].find_all("div",{"class" : "col-sm-9"})
        name_word=name[0].text.strip().replace("\n","")
        element_price = soup.find_all("div", {"class":"price-item"})
        
        for i in range(len(element_price)):
            name = element_price[i].find(class_ = "brandtag cut-text fueltype-heading").get_text(strip = True)
            price = element_price[i].find(class_ = "pricetag").get_text(strip = True).replace(" €","")
            price_list.append(name)
            price_list.append(price)
        
        for i in range(1,len(price_list),2):
            new_row=[]
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    
            if price_list[i-1]=='Unleaded 95':
                new_row.append(name_word+" - "+"Αμόλυβδη 95")
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                
            elif price_list[i-1]=='Unleaded 98':
                new_row.append(name_word+" - "+'Αμόλυβδη 98')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                
            elif price_list[i-1]=='Diesel':
                new_row.append(name_word+" - "+'Πετρέλαιο Κίνησης')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Diesel")
                new_row.append("TRANSPORT")
                 
            elif price_list[i-1]=='Heating Diesel':
                new_row.append(name_word+" - "+'Πετρέλαιο Θέρμανσης')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                   
            elif price_list[i-1]=='Kerosene':
                new_row.append(name_word+" - "+'Κηροζίνη')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                
            new_row.append(brand_word) 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_IKEA(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)  

    if (response.status_code != 200): #or ("ERROR 404" in response.text) or ("μήπως κάτι λείπει;" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        
    else:
        if ("Προσθήκη στο καλάθι" in response.text) or ("Ενημέρωση διαθεσιμότητας" in response.text):
            soup = BeautifulSoup(response.content, "html.parser")
            element_soup = soup.find_all("span",{"class":"price__sr-text"})
        
            if (element_soup):
                element_soup_1=element_soup[0]
                element_soup_2=element_soup_1.text
                element_soup_3 = element_soup_2.replace('€', '').replace(",",".").strip()
                if "Τρέχουσα τιμή" in element_soup_3:
                    element_soup_3=element_soup_3.replace("Τρέχουσα τιμή  ","").replace(",",".")
            
                if "Αρχική τιμή" in element_soup_3:
                    element_soup_3=element_soup_3.replace("Αρχική τιμή  ","").replace(",",".")
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(element_soup_3))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("IKEA")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_stephanis(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_new = "https://www.stephanis.com.cy/en"+str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code != 200) or ("This product is no longer available" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div",{"class":"listing-details-heading"})
        
        if (len(element_soup) < 2):
            element_soup_1 = element_soup[0]
        else:
            element_soup_1 = element_soup[1]
            
        element_soup_2 = element_soup_1.text
        price_ = element_soup_2.replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Stephanis")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CYTA(u):
    
    q=0
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code==200):
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Wired/Wireless telephone services	
        element_soup = soup.find_all("div",{"class":"table-responsive"})
        for o in range(0,len(element_soup)):
            if "Κλήσεις προς" in element_soup[o].text:
                element_ = element_soup[o]
                element_soup_1 = element_.find_all("td")
                for p in range(0, len(element_soup_1)):
                    ken=element_soup_1[p].text
                    if (ken==name_):
                        price_=element_soup_1[p+1].text.replace("€","").replace(",",".").replace(" /λεπτό","")
                        q=1
        
        # Internet access provision services	
        if (q==0):
            element_soup = soup.find_all("div",{"class":"card-body px-1"})
            qq=0
            for o in range(0,len(element_soup)):
                text = element_soup[o].get_text()
                price_pattern = r'€(\d+(?:,\d+)?)' 
                matches = re.findall(price_pattern, text)
            
                if (matches) and (qq==0):
                    price_ = matches[0].replace(",",".")
                    qq=1
                    q=1
        
        # Bundled telecommunication services
        if (q==0):
            element_soup = soup.find_all("h4",{"class":"text-24 text-center mb-0 pb-0"})
            text = element_soup[0].get_text()
            price_pattern = r'€(\d+(?:,\d+)?)'  
            matches = re.findall(price_pattern, text) 

            if matches:
                price_ = matches[0].replace(",",".")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("CYTA")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
        
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_epic(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code==200):
        
        if (name_=="To fixed telephony lines of other providers")|(name_=="To mobile telephony lines of other providers"):
            
            element_ = soup.find_all("table",{"class":"yellow-top-zebra"})
            name_1 = element_[0].find_all("th")
            price_1 = element_[0].find_all("td")
            
            for i in range(0,len(name_1)):
                new_row=[]
                
                if (name_1[i].text==name_):
                    price_=price_1[i-2].text.replace("€","")
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Epic")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                else:
                    pass

        elif (name_=="5G Unlimited Max Plus")|(name_=="5G Unlimited Max"):

            element_ = soup.find_all("div",{"class":"price"})
            new_row = []
            
            if name_ == "5G Unlimited Max Plus":
                price_ = element_[0].text.replace("€","")
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Epic")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
                
            if name_ == "5G Unlimited Max":
                price_ = element_[1].text.replace("€","")
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Epic")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)        
        
        else:
            element_soup_price = soup.find_all("div",{"class":"price"})
            element_soup_name = soup.find_all("div",{"class":"mtn-name mtn-name-bb"})
            new_row = []
            
            for q in range(0,len(element_soup_name)):
                new_row = []
                _name_ = element_soup_name[q].text.strip().replace(" ","")
                
                if _name_=="InternetandTelephony10":
                    qp=0
                if _name_=="InternetandTelephony20":
                    qp=2
                if _name_=="InternetandTelephony50":
                    qp=6
            
                if _name_==name_.replace(" ",""):
                    price_=element_soup_price[qp].text.replace("€","").replace(" ","")
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(_name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Epic")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
    
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_Athlokinisi(u):
    
    url="https://athlokinisi.com.cy"+Item_url_
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("span",{"class":"ammount"})
        
        if not element_soup:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x) 
        else:
            price_=float(element_soup[0].text.strip().replace("€",""))
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Athlokinisi")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_AWOL(u):
    
    p=0
    price_="0"
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url="https://www.awol.com.cy/"+Item_url_
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_soup = soup.find_all("span",{"class":"price price--sale"})
    
    if element_soup:
        p=0
    else:
        element_soup = soup.find_all("span",{"class":"price"})   
        
    if ((response.status_code !=200) or ("Page Not Found" in response.text)):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x) 
    else:
        if element_soup[0] is not None:
            amounts_list = element_soup[0].text.split('€')
            if len(amounts_list) > 2:
                price_ = amounts_list[2]
            if len(amounts_list) <= 2:
                price_ = amounts_list[1] 
        price_= price_.replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("AWOL")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_alter_Vape(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")

    if ("Page not found" in response.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("span",{"class":"price"})
        price_1=element_soup[0].text.replace("\n","")
        if "Sale price" in price_1:
            price_1=price_1.replace("Sale price€","").replace(",",'.')

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_1))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Alter Vape")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_bwell_pharmacy(u):
    
    url="https://bwell.com.cy/shop/"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404. The page you are looking for does not exist" in response.text)or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("span",{"class":"woocommerce-Price-amount amount"})
        element_soup_1=element_soup[1].text
        price_=element_soup_1.replace("€","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Bwell Pharmacy")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cablenet(u):
    
    name_=urls["Name"].iloc[u]
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("div",{"class":"plan-price"}) 
        # Internet access provision services	
        if (name_=="PurpleInternet") or (name_=="PurpleMaxMobile"): 
            if name_=="PurpleInternet":
                qp=1
        # Bundled telecommunication services
            if name_=="PurpleMaxMobile":
                qp=0
            euro_=element_soup[qp].text.count("€")
            price_=float(element_soup[qp].text.replace(" ",'').split("€")[euro_].split("/")[0])
        else: 
            # Wireless telephone services	
            element_name = soup.find_all("td")
            for i in element_name:
                if i.text==name_:
                    value_=element_name[18].text
                    price_=value_.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")
                if i.text==name_:
                    value_=element_name[23].text
                    price_=value_.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Cablenet")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyMinistryEducation(u):
    url="http://archeia.moec.gov.cy/mc/698/"+Item_url_
    
    if "ΝΗΠΙΑΓΩΓΕΙΩΝ" in name_:
        pdf_ = tb.read_pdf(url, pages = '4',pandas_options={'header': None}, stream=True)
        pdf_ = pdf_[0]
        
        #Annual cost
        pdf_[3] = pdf_[3].astype('string')
        pdf = pdf_[3][1]
        price_1 = float(pdf.strip('€*').replace(".", ""))

        #Other cost
        pdf_[5] = pdf_[5].astype('string')
        pdf = pdf_[5][0]
        price_2 = float(pdf.replace("τέλος εγγραφής ","").strip('€*').replace(".", ""))

        pdf_[5] = pdf_[5].astype('string')
        pdf = pdf_[5][2]
        price_3 = float(pdf.replace("βιβλία και στολές ","").strip('€*').replace(".", ""))
        
        #Total
        price_=price_1+price_2+price_3
    
    if "ΔΗΜΟΤΙΚΩΝ" in name_:
        pdf_ = tb.read_pdf(url, pages = '1',pandas_options={'header': None}, stream=True)
        pdf_ = pdf_[0]

        #Annual cost
        for i in range(0,7):
            pdf_[i] = pdf_[i].astype('string')

        price_1 = float(pdf_[1][25].strip('€*').replace(".", ""))+float(pdf_[2][25].strip('€*').replace(".", ""))+float(pdf_[3][25].strip('€*').replace(".", "").split(" €")[0])+float(pdf_[3][25].strip('€*').replace(".", "").split(" €")[1])+float(pdf_[4][25].strip('€*').replace(".", ""))+float(pdf_[5][25].strip('€*').replace(".", ""))
        price_1=price_1/6

        #Other cost
        pdf = pdf_[6][24]
        price_2 = float(pdf.replace("τέλος εγγραφής ","").strip('€*').replace(".", ""))

        pdf = pdf_[6][26]
        price_3 = float(pdf.replace("βιβλία και στολές ","").strip('€*').replace(".", ""))
        
        #Total
        price_=price_1+price_2+price_3
                     
    if ("Nicosia" in name_) and ("ΜΕΣΗΣ" in name_):
        pdf_ = tb.read_pdf(url, pages = '1',pandas_options={'header': None}, stream=True)
        pdf_ = pdf_[0]

        for i in range(2,7):
            pdf_[i] = pdf_[i].astype('string')
            if subclass_=="Secondary education":
                value_1=(float(pdf_[2][4].replace("€",'').replace(".","")))
                value_2=(float(pdf_[3][4].replace("€",'').replace(".","")))
                value_3=(float(pdf_[4][4].replace("€",'').replace(".","")))
                value_4=(float(pdf_[5][4].replace("€",'').replace(".","")))
                value_5=(float(pdf_[6][4].replace("€",'').replace(".","")))
                value_6=(float(pdf_[7][4].replace("€",'').replace(".","")))
                price_ = float(value_1 + value_2 + value_3 + value_4 + value_5 + value_6) / 6

            if subclass_=="Post-secondary non-tertiary education (ISCED 4)":
                pdf_[8] = pdf_[8].astype('string')
                value_7 = (float(pdf_[8][4].replace("€",'').replace(".",""))) 
                price_ = float(value_7)
    
    if ("Limassol" in name_) and ("ΜΕΣΗΣ" in name_):
        pdf_ = tb.read_pdf(url, pages = '2',pandas_options={'header': None}, stream=True)
        pdf_=pdf_[0]
        
        for i in range(2,7):
            pdf_[i] = pdf_[i].astype('string')
            if subclass_=="Secondary education":
                value_1=(float(pdf_[2][15].replace("€",'').replace(".","")))
                value_2=(float(pdf_[3][15].replace("€",'').replace(".","")))
                value_3=(float(pdf_[4][15].replace("€",'').replace(".","")))
                value_4=(float(pdf_[5][15].replace("€",'').replace(".","")))
                value_5=(float(pdf_[6][15].replace("€",'').replace(".","")))
                value_6=(float(pdf_[7][15].replace("€",'').replace(".","")))
                price_ = float(value_1 + value_2 + value_3 + value_4 + value_5 + value_6) / 6

            if subclass_=="Post-secondary non-tertiary education (ISCED 4)":
                pdf_[8] = pdf_[8].astype('string')
                value_7 = (float(pdf_[8][15].replace("€",'').replace(".",""))) 
                price_ = float(value_7)
    
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Cyprus Ministry of Education, Sport and Youth")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyPost(u):
    
    if ("ΜΕΜΟΝΩΜΕΝΩΝ" in name_):
        p=6
        d=2
        if ("50 γρ." in name_):
            qp=14
        elif ("500 γρ." in name_):
            qp=21
        elif ("2000 γρ." in name_):
            qp=44
        
    if ("ΔΕΜΑΤΩΝ" in name_):
        p=11
        d=1
        if ("0.5 κιλό" in name_):
            qp=2
        elif("15 κιλά" in name_):
            qp=17
        elif ("30 κιλά" in name_):
            qp=32
          
    pdf_ = tb.read_pdf(Item_url_, pages = p,pandas_options={'header': None}, stream=True)[0]
    pdf_[d]=pdf_[d].astype('string')
    price_=pdf_[d][qp].split(' ')[0].replace(',','.')
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Cyprus Post")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ewholesale(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x) 
    
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div",{"class":"hM4gpp"}) 
        price_= element_soup[0].text.replace("€Τιμή","").replace(" ","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("E-wholesale")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_electroline(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("ins",{"class":"product-price product-price--single product-price--sale-price product-price--single--sale-price"}) 
        
        if element_soup:
            price_ = element_soup[0].text.replace("\n",'').replace("€","")
        else:
            element_soup = soup.find_all("h2",{"class":"product-price product-price--single"}) 
            price_ = element_soup[0].text.replace("\n","").replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Electroline")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_europeanuniversitycyprus(u):
    
    euc = tb.read_pdf(Item_url_, pages = '2',pandas_options={'header': None}, stream=True)
    list_euc = []
    
    for i in range(0,5):
        new_row=[]
        euc[i][1] = euc[i][1].astype('string')
        
        for word in euc[i][1].to_list():
            word = word.replace(',','')
            word = int(word)
            list_euc.append(word)
    
    price_=(sum(list_euc)+21000+21900)/(len(list_euc)+2)
    
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("European University Cyprus")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_famoussport(u):
    
    url = "https://www.famousports.com/en"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code !=200) or ("Oops! Page Not Found!" in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("h2",{"class":"product-price product-price--single"}) 
        element_soup = soup.find_all("strong",{"class":"text-xl lg:text-2xl font-bold tracking-tight"})
        price_=element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Famous Sports")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_Marks_Spencer(u):
    
    url="https://www.marksandspencer.com/cy"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("Sorry, we can't" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)   
    else:
        element_soup = soup.find_all("span",{"class":"list-pricecolour"})
        price_=element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Marks & Spencer")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_moto_race(u):
    
    url="https://www.motorace.com.cy/"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)  
    else:
        element_soup = soup.find_all("span",{"class":"price"})
        price_=element_soup[0].text.replace(",","").replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Moto Race")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_nissan(u):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(Item_url_, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("THIS IS A DEAD END..." in response.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        tree = html.fromstring(response.content)
        price_tree = tree.xpath('//iframe[@id="individualVehiclePriceJSON"]/text()')
        
        if price_tree:
            price_json = price_tree[0]
            price_data = json.loads(price_json)
            if "LVL001" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL001']['gradePrice']
            if "LVL004" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL004']['gradePrice']
            if "LVL005" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL005']['gradePrice']
            if name_ == "NISSAN JUKE 1.6lt 143HP N-CONNECTA 2-TONE":
                price_ = price_data["juke_2019"]['default']['grades']['LVL001']['gradePrice']
        
        print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Nissan")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
            
def results_novella(u):
    
    new_row=[]
    website_false=[]
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if ("404 Page Not Found." in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        scripts_1 = soup.find_all('td',{'class':'column-1'},string=True)
        scripts_2 = soup.find_all('td',{'class':'column-2'},string=True)
 
        for i in range(0,len(scripts_1)):
            new_row=[]
            website_false=[]
            
            if (scripts_1[i].text=="LADIES CUT") and (name_=="Women's Services, HAIRCUT Stylist"):
                price_=scripts_2[i].text.replace('€',"").replace(',','.')
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Novella")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
 
            elif (name_=="Men's Services, HAIRCUT Stylist") and (scripts_1[i].text== "MEN'S CUT"):
                price_=scripts_2[i].text.replace('€',"").replace(',','.')
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Novella")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_numbeo(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")

    if ("Status code: 404" in soup.text)or(response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all('tr',{"class":"tr_standard"})
        for o in range(0,len(element_soup)):
            ken=element_soup[o].text.replace("\n","").replace(" ","")
            if "Cyprus" in ken:
                result = re.sub(r'^.*?(Cyprus)', r'\1', ken).replace("Cyprus","").replace("$","").replace(" ","")
                price_=round((float(result)/1.08),2)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Numbeo")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_primetel(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")

    if ("Pay my bill" in soup.text)or(response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        # Internet access provision services & Bundled telecommunication services	
        if (name_=="HomeFiber 60 MBPS")|(name_=="HomeFiber 100 MBPS")|(name_=="HomeFiber 150 MBPS")|(name_=="GIGA Unlimited")|(name_=="GIGA Unlimited Plus")|(name_=="GIGA Unlimited MAX"):
            element_ = soup.find_all('div',{"class":"top_plan_box"})
            
            for i in range(0,len(element_)):
                
                if element_[i].text.replace("\n","") == name_ :
                    element_ = soup.find_all('div',{"class":"price_plan_box"}) 	
                    price_=element_[i].text.replace("\n","").replace(" ","")
                    price_=price_.split("€")
                    
                    if len(price_)>2:
                        price_=price_[2].replace("month","")
                    else:
                        price_=price_[0]          
                    
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x) 
                
                else:
                    pass
        
        # Wired & Wireless Telephone Services           
        elif (name_=="Calls to other providers landline")|(name_=="Calls to other providers mobile"):
            
            element_ = soup.find_all("table",{"id":"call_rates"},{"class":"table-striped table-bordered dt-responsive table-hover nowrap dataTable dtr-inline data_table_resp"})
            element_td = element_[0].find_all("td")
                
            if name_ == "Calls to other providers landline" :
                    price_ = element_td[9].text.replace("\n","").replace(" ","").replace("€","").replace("/minute","")
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                    
            if name_ == "Calls to other providers mobile" :
                    price_ = element_td[11].text.replace("\n","").replace(" ","").replace("€","").replace("/minute.Minimumcharge1minute","")
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_rio(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found!" in soup.text)or(response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('p',{"style":"text-align: center;"})
        for i in range(0,len(element_name)):
            if name_ in element_name[i].text:
                if "3D" in element_name[i].text:
                    match = re.search(r'(\S+)\s*€(\d+)', element_name[i].text)

                    if match:
                        new_row=[]
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(name_+" 3D")
                        new_row.append(float(match.group(2)))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(division_)
                        website_false.append(retailer_)
                        daily_errors.loc[len(daily_errors)] = website_false
                        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)     
                else:
                    amount_match = re.search(r'€(\d+)', element_name[i].text)

                    if amount_match:
                        price_ = amount_match.group(1)
                        new_row=[]
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(name_)
                        new_row.append(float(price_))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(division_)
                        website_false.append(retailer_)
                        daily_errors.loc[len(daily_errors)] = website_false
                        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
"""
def results_AHK(u):
    response = requests.get(Item_url_)
    pdf_AHK = "PDFs/AHK_Mar2024.pdf"
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        with open(pdf_AHK, "wb") as f:
            f.write(response.content)
        with open(pdf_AHK, "rb") as f:
            #pdf_reader = PyPDF2.PdfReader(f)
            pdf_reader = pypdf.PdfReader(f)
            page = pdf_reader.pages[2]
            text = page.extract_text()
    
        lines = text.split("\n")
       
        for line in lines:
            new_row = []
            if name_ in line:
                ken = line.strip()
                match = re.search(r'\d+,\d+', ken)
                if match:
                    
                    if "για" in ken:
                        price_ = float(match.group(0).replace(",","."))/100
                    else:
                        price_ = float(match.group(0).replace(",","."))
                        
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(price_)
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("AHK")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                else:
                    website_false.append(name_)
                    website_false.append(subclass_)
                    website_false.append(Item_url_)
                    website_false.append(division_)
                    website_false.append(retailer_)
                    daily_errors.loc[len(daily_errors)] = website_false
                    daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
"""
def results_AHK(u):
    pdf_AHK = "PDFs/AHK_Nov2024.pdf"
    
    with open(pdf_AHK, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        page = pdf_reader.pages[2]
        text = page.extract_text()
    lines = text.split("\n")
       
    for line in lines:
        new_row = []
        if name_ in line:
            ken = line.strip()
            match = re.search(r'\d+,\d+', ken)
            if match:     
                if "για" in ken:
                    price_ = float(match.group(0).replace(",","."))/100
                else:
                    price_ = float(match.group(0).replace(",","."))   
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("AHK")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_CERA(u):
    
    response = requests.get(Item_url_)
    CERA = tb.read_pdf(Item_url_, pages = '8',pandas_options={'header': None}, stream=True)
    amount_=CERA[0][1].to_list()
    _names_=CERA[0][0].to_list()
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:   
        for oo in range(0,len(_names_)-1):
            n1=_names_[oo]+" "+_names_[oo+1]
            if name_ == n1:
                price_=float(amount_[oo])/100
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Cyprus Energy Regulatory Authority")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_water(u):
    price_=""
    
    if "Nicosia" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        city_="Nicosia"
        if name_=="Πάγιο ανά μήνα":
            element_=soup.find_all("div",{"id":"ekit-table-container-9f0855a_wrapper"})
            pattern = r"Πάγιο(\d{2},\d{2})"
            text = element_[0].get_text()
            match = re.search(pattern, text)
        
            if match:
                price_ = match.group(1)
                price_=float((price_).replace(",","."))/2
                print(price_)

        if name_=="Κυβικά ανά μήνα":
            element_=soup.find_all("td",{"class":"elementor-repeater-item-93fd68b ekit_table_data_"})
            price_=element_[0].text.replace(",",".")
    
    if "Larnaca" in retailer_:
        city_="Larnaca"
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        element_=soup.find_all("table",{"class":"table-format-left"})
        text_=element_[0].text
        element_1 = re.search(r'Πάγιο(\d+,\d+)',text_)
        element_2 = re.search(r'Δικαίωμα Συντήρησης(\d+,\d+)',text_)
        element_3 = re.search(r'1Μέχρι15(\d+,\d+)',text_)
        
        if name_=="Πάγιο ανά μήνα":
            if element_1:
                price_1 = element_1.group(1).replace(",",".")
                price_=float(price_1)/3
                
        if name_=="Δικαίωμα Συντήρησης ανά μήνα":
            if element_2:
                price_1=element_2.group(1).replace(",",".")
                price_=float(price_1)/3
                
        if name_=="Κυβικά ανά μήνα":
            if element_3:
                price_1=element_3.group(1).replace("16","").replace(",",".")
    
    if "Limassol" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        city_="Limassol"
        
        if name_=="Πάγιο ανά μήνα":
            element_=soup.find_all("div",{"class":"acd-des"})
            element_1=element_[2].find_all("td")
            price_=element_1[3].text.replace("\n","").replace(",",".")
            price_=float(price_)/4
        
        if name_=="Δικαίωμα Συντήρησης ανά μήνα":
            element_=soup.find_all("div",{"class":"acd-des"})
            element_1=element_[2].find_all("td")
            price_=element_1[5].text.replace("\n","").replace(",",".")
            price_=float(price_)/4
            
        if name_=="Κυβικά ανά μήνα":
            element_=soup.find_all("div",{"class":"acd-des"})
            element_1=element_[2].find_all("td")
            price_=element_1[11].text.replace("\n","").replace(",",".")
    
    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_+" - "+city_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Water Board")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_wolt(u):
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('span',{"data-test-id":"product-modal.price"})
        
        if element_name:
            price_=element_name[0].text.replace("€","")
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Wolt")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false

def results_vasos(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header},verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('p',{"class":"slider-text3"})
        price_=element_name[0].text.replace("\n","").replace(" ","")
        price_ = ''.join(filter(str.isdigit, price_))
        price_ = float(price_) / 100
        
    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Vasos Psarolimano")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(comidity_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_meze(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header},verify=False)
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)    
    else:
        element_name = soup.find_all('div',{"class":"mprm-simple-view-column mprm-first"})
        for i in range(0,len(element_name)):
            if ("Meat Meze" in element_name[i].text) and ("Meat Meze" in name_):
                element_name_2 = element_name[i].find_all('li',{"class":"mprm-flex-item mprm-price"})
                price_=element_name_2[0].text.replace("€","")

        for i in range(0,len(element_name)):
            
            if "Fish Meze" in element_name[i].text and ("Fish Meze" in name_):
                element_name_2 = element_name[i].find_all('li',{"class":"mprm-flex-item mprm-price"})
                price_=element_name_2[0].text.replace("€","")
        
        if price_:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Meze Tavern")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_CYgar_shop(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('div',{"class":"hM4gpp"})
        price_ = element_name[0].text.replace('€','').replace('Price','')
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("The CYgar shop")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_the_royal_cigars(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('div',{"class":"itemDetailsPrice"})
        if element_name:
            price_amount=element_name[0].text.replace("€","")
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_amount))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("The Royal Cigars")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_pydixa(u):
    
    pdf_pixida = "PDFs/Pixida-Nic-En-Mar2023.pdf"
    '''
    response = requests.get(Item_url_)
    if response.status_code!=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
    with open(pdf_pixida, "wb") as f:
        f.write(response.content)
    '''
    with pdfplumber.open(pdf_pixida) as pdf:
        page = pdf.pages[5]  
        text = page.extract_text()

    matches = re.findall(r'Ψαρομεζές .*?(\d+\.\d+)', text)
    if matches:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))        
        new_row.append(name_)
        new_row.append(float(matches[0]))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Pyxida")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_sewerage(u):
    
    values=0
    
    if "Nicosia" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        new_row=[]
        city_="Nicosia"
        if "Ετήσιο Τέλος" in name_:  
            element_=soup.find_all("div",{"class":"elementor-element elementor-element-f737ced elementor-widget elementor-widget-text-editor"})
            element_1=element_[0].find_all("li")
            for i in range(0,len(element_1)):
                price_amount=element_1[i].text
                match = re.search(r'€(\d+,\d+)', price_amount)
                if match:
                    value = float(match.group(1).replace(",","."))
                    values=value+values
            values=values/3
        
        if "Τέλος Χρήσης" in name_:
            element_=soup.find_all("div",{"class":"elementor-element elementor-element-dbb217e elementor-widget elementor-widget-text-editor"})
            new_row=[]
            for i in range(0,len(element_)):
                price_amount=element_[i].text
                match = re.search(r'(\d+)', price_amount)
                if match:
                    values = float(match.group(1))/100
                      
    if "Limassol" in retailer_:
        city_="Limassol"
        new_row=[]
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
            
        if "Ετήσιο Τέλος" in name_:
            if "SSL handshake failed" in soup.text:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
            else:
                element_name = soup.find_all('table',{"class":"table table-striped"})
                element_name_2 = element_name[0].find_all('tr')
                element_name_2=element_name_2[len(element_name_2)-1]
                desired_lines = [element_name_2.find_all('td')[4].get_text(), element_name_2.find_all('td')[6].get_text()]

                for lines in desired_lines:
                    value=float(lines.replace(",","."))
                    values=value+values
                
                values=values/2
            
        if "Τέλος Χρήσης" in name_:
            element_name = soup.find_all('table',{"class":"table table-striped"})
            element_name_2 = element_name[1].find_all('tr')
            element_name_2=element_name_2[len(element_name_2)-1]
            desired_lines = [element_name_2.find_all('td')[1].get_text()]
                
            for lines in desired_lines:
                values=float(lines.replace(",","."))
    
    if "Larnaca" in retailer_:
        city_="Larnaca"
        new_row=[]
        """
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('table',{"width":"649"})
        element_name_2 = element_name[0].find_all('tr')
        element_name_2=element_name_2[len(element_name_2)-2]

        if "Ετήσιο Τέλος" in name_:
            desired_lines = [element_name_2.find_all('td')[2].get_text(),element_name_2.find_all('td')[4].get_text(),element_name_2.find_all('td')[6].get_text()]

            for lines in desired_lines:
                value=float(lines.replace(",","."))
                values=value+values

            values=values/3

        elif "Τέλος Χρήσης" in name_:
            desired_lines = [element_name_2.find_all('td')[8].get_text()]
            for lines in desired_lines:
                values=float(lines.replace(",","."))
        """
    if values!=0:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_+" "+city_)
        new_row.append(values)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Sewerage Board of "+ city_)
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

'''
def results_toyota(u):
    
    if name_ == "The New Toyota Yaris Cross":
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
        if response.status_code != 200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Yaris Cross"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
            
    if name_ == "The New Toyota Yaris":
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
        if response.status_code != 200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Yaris"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        
    if name_ == "Toyota Aygo X":
            
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
        if response.status_code != 200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            #element_soup = soup.find_all('p',{"class":"t-milli-headline mb-0 text-normal cmp-mega-menu__price-wrapper d-flex"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            #price_ = float(element_soup2[0]['data-price'])
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Aygo x"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
                  
    #if subclass_=="Second-hand motor cars":
        
        #1st way
        """ 
        query ={"component":"used-stock-cars-v2","fetches":[
        {"fetchType":"fetchUscVehiclePrice","vehicleForSaleId":"4077c595-5c2c-42bd-8133-203d770ad125","context":"used","uscEnv":"production"}
        ]}
        headers = {"Host": "usc-webcomponents.toyota-europe.com","User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0","Accept": "*/*","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br, zstd","Content-Type": "application/json","Content-Length": "180","Origin": "https://www.toyota.com.cy","Connection": "keep-alive","Referer": "https://www.toyota.com.cy/","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "cross-site","Priority": "u=6","TE": "trailers"
        }
        response = requests.get(Item_url_,{'headers':headers})
        r = requests.post("https://usc-webcomponents.toyota-europe.com/v1/api/data/cy/en?brand=toyota&uscEnv=production", json=query, headers=headers)
        price_=r.json()['fetches'][0]['result']['fetchResult'] ['sellingPriceInclVAT']
        """
        
        #2nd way
        """
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        isnone = soup.find("div", {"role": "cpdqm_ignore"}).text

        if isnone==None:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        else:
            data = json.loads(isnone)
            price_ = data['vehicle']['result']['price']['sellingPriceInclVAT']
            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Toyota")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
            """
'''

def results_toyota(u): 

    if (name_ == "The New Toyota Yaris Cross") | (name_ == "The New Toyota Yaris") | (name_ == "Toyota Aygo X"):
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
        if response.status_code != 200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            # Find the div with the relevant data attribute
            data_div = soup.find('div', class_='dnb-sales-hero-outer-container').find('div', attrs={'data-component-props': True})
            # Extract the value of the data-component-props attribute
            data_component_props = data_div['data-component-props']    
            # Unescape the JSON string
            data_component_props = data_component_props.replace('&quot;', '"')    
            # Parse the JSON data
            data = json.loads(data_component_props)
            # Extract the TotalPrice from financeConfig
            finance_config_str = data['salesHeroDto'].get('financeConfig', '')
            finance_config = json.loads(finance_config_str)
            price_ = finance_config.get('TotalPrice')
            
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_) 
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ithaki(u):
    
    pdf_ithaki = "PDFs/ithaki-2024.pdf"

    with pdfplumber.open(pdf_ithaki) as pdf:
        first_page = pdf.pages[5]
        text = first_page.extract_text()
        
    pattern = r'(\d+.*?\d+\.\d{2})'
    matches = re.findall(pattern, text)
    
    for match in matches:
        new_row = []
        website_false = []
        
        if ("Ποικιλία Κρεατικών" in match) and ("Ποικιλία Κρεατικών για 2 άτομα - Larnaca"== name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)

            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        
        elif ("Ποικιλία Θαλασσινών" in match) and ("Ποικιλία Θαλασσινών για 2 άτομα - Larnaca"==name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)

            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_flames(u):

    #Mixed Grill 
    if name_ == "Mixed Grill for 2 persons - Famagusta":
        pdf_flames1 = "PDFs/flames-grill-specialities-Mar2024.pdf"
    
        with pdfplumber.open(pdf_flames1) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()

        lines = text.split('\n')
        desired_line = None
    
        for line in lines:
    
            if "Mixed Grill" in line:
                desired_line = line.strip()  
    
        if desired_line:
            pattern = r'(\d+\.\d{2})$'
            price_ = re.findall(pattern, desired_line)

    #Flames Special Cyprus (Meze)
    if name_ == "Meat Meze for 2 persons - Famagusta":
        pdf_flames2 = "PDFs/flames-cyprus-dishes-Mar2024.pdf"
    
        with pdfplumber.open(pdf_flames2) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
    
        lines = text.split('\n')
        desired_line = None
    
        for line in lines:
    
            if "Flames Special Cyprus (Meze)" in line:
                position = lines.index("Flames Special Cyprus (Meze)")
                correct_line = lines[position+1]
                desired_line = correct_line.strip()  
    
        if desired_line:
            pattern = r'(\d+\.\d{2})$'
            price_ = re.findall(pattern, desired_line)

    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_[-1]))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Flames")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_lensescy(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('div',{"class":"product-price"})
        price_=element_name[0].text.replace("€","").replace(" ","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append("Corrective eye-glasses and contact lenses")
        new_row.append("HEALTH")
        new_row.append("LensesCY")
        list_.loc[len(list_)] = new_row

def results_intercity(u):
    
    url="https://intercity-buses.com/en/routes/"+str(Item_url_)
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(url,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        table_=soup.find_all("table",{"class":"tablesorter eael-data-table center"})[0]
        if table_:
            element_=table_.find_all("div",{"class":"td-content-wrapper"}) 
            for ii in range(0,2):
                new_row=[]
                if ii%2 ==0:
                    name_=element_[ii].text.replace(" ","").replace("\n","").replace("\t","")
                    price_=element_[ii+1].text.replace(" ","").replace("\n","").replace("\t","").replace("€","")
                    if (price_=="NOTAVAILABLE") or (price_=='ΔΕΝΔΙΑΤΙΘΕΤΑΙ'):
                        pass
                    else:
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(name_+Item_url_)
                        new_row.append(float(price_))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Intercity Buses")
                        list_.loc[len(list_)] = new_row
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
            
def results_parga(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_,{'headers':header})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_=soup.find_all('span',{'class':'productPriceStore'})
        price_=element_[1].text.replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Parga")
        list_.loc[len(list_)] = new_row

def results_evdokia(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_,{'headers':header})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        price_element = soup.find('p', class_='price')
        bdi_element = price_element.find('bdi')
        price_=bdi_element.text.replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Evdokia Jewellery")
        list_.loc[len(list_)] = new_row

def results_centroptical(u):
    
    response=requests.get(Item_url_, headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        price_element = soup.find('p', class_ = 'price')
        bdi_element = price_element.find('bdi')
        price_=bdi_element.text.replace("€","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Centroptical")
        list_.loc[len(list_)] = new_row

def results_premier(u):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Origin': 'https://premierlaundry.com.cy',
        'Connection': 'keep-alive',
        'Referer': 'https://premierlaundry.com.cy/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',}

    params = { }
    json_data = {'email': 'kendeas123@gmail.com','password': 'Kendeas',}
    response = requests.post('https://cleancloudapp.com/webapp/public/api/auth/login/16130',params=params,headers=headers,json=json_data,)
    data = response.json()
    user_id = data['id']
    token = data['token']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-CC-User': str(user_id), 
        'X-CC-Token': token, 
        'Origin': 'https://premierlaundry.com.cy',
        'Connection': 'keep-alive',
        'Referer': 'https://premierlaundry.com.cy/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',}

    params = {'ccascv': '0.20327901592645015',}
    json_data = {'priceListId': 0,}
    response = requests.post('https://cleancloudapp.com/webapp/public/api/store/products',params=params,headers=headers,json=json_data,)
    all_data_products = response.json()
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        products = all_data_products['Products']
        names = [item['name'] for item in products]
        price = [item["price"] for item in products]
    
        for i in range(len(names)):
            
            if name_==names[i]:
                new_row.append(datetime.today().strftime("%Y-%m-%d"))
                new_row.append(names[i])
                new_row.append(float(price[i]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Premier Laundry")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cyprus_transport(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url = 'https://www.publictransport.com.cy/cms/page/cash-tickets'
    response = requests.get(url, headers=header)
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        wrapper = soup.find_all('tbody')[0]
        data = []
        for row in wrapper.find_all('tr'):
            row_data = []
            for cell in row.find_all(['td', 'th']):
                row_data.append(cell.get_text().strip())
            data.append(row_data)
        df1 = pd.DataFrame(data)
        df1.columns = ['Ticket type', 'Paper Ticket (CASH)','Plastic ANONYMOUS Card', 'Plastic PERSONALISED Motion Bus Card - Normal Charge', 'Plastic PERSONALISED Motion Bus Card - Beneficiaries of 50%' ]
        df1 = df1.drop(0)
        df1 = df1.drop(1)
        df1 = df1.drop(6)
        df1 = df1.set_index('Ticket type')
        new_list = []
        
        for column in df1.columns:  
            
            for index in df1.index:
                value = df1.loc[index, column]
                new_row = {'Date': datetime.now().strftime('%Y-%m-%d'), 'Name': f'{column} / {index}', 'Price': value, 'Subclass' : 'Passenger transport by bus and coach', "Division" : 'TRANSPORT', "Retailer": 'Cyprus Public Transport'}  # Create a new row with the concatenated column name and index value
                new_list.append(new_row)
        
        df2 = pd.DataFrame.from_records(new_list)
        df_cy_transport = df2[df2["Price"] != "-"]
        df_cy_transport["Price"] = df_cy_transport["Price"].str.replace('€', '')
        df_cy_transport['Price'] = df_cy_transport['Price'].astype(float)
        df_cy_transport.reset_index(drop = True, inplace = True)

        for index, row in df_cy_transport.iterrows():
            if row['Name']==name_:
                list_.loc[len(list_)] = row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_musicavenue(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        name = soup.find('h1', class_ = 'product-title')
        new_row.append(name_)
        price_=soup.find_all("bdi")[1].text.replace("€", "").replace(",", "")
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Musicavenue")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_max_7_tax(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        table_ = soup.find('table', {"class" :'tbl',"style":"width: 100%;","border":"1","frame":"void","cellspacing":"1","cellpadding":"3","align":"center"})
        table_=table_.text
        if "Initial charge" in name_:
            pattern = r'Initial charge\s+([\d,]+)\s+([\d,]+)'
        if "Fare per Km" in name_:
            pattern = r'Fare per Km\s+([\d,]+)\s+([\d,]+)'  
        matches = re.findall(pattern, table_)
        charges_ = [float(charge.replace(',', '.')) for charge in matches[0]]
        
        for i in range(0,2):
            if i==0:
                add_="Fixed"
            if i==1:
                add_="Variable"
            new_row=[]
            new_row.append(datetime.today().strftime("%Y-%m-%d"))
            new_row.append(name_+add_)
            new_row.append(float(charges_[i]))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Max 7 Taxi") 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_costastheodorou(u):
    response = requests.get(Item_url_)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all("p",{"class":"price"})
        price_ = element_name[0].text.replace("€","").split('\xa0')[0]
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Costas Theodorou")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_leroymerlin(u):
    
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_,{'headers':header})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200 or ("Η σελίδα που αναζητάτε δεν βρέθηκε." in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_=soup.find_all("span",{"class":"priceBigMain"})
        price_=element_[0].text.replace("€","").replace(" ","").replace(",",".")
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Leroy Merlin") 
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def stock_center_results(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)

    if (response.status_code != 200) or ("Το όχημα αυτό δεν είναι πλέον διαθέσιμο" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_price_ = soup.find_all("div",{"class":"price"})
        price_ = element_price_[0].text.replace("Τιμή μετρητοίς","").replace(" ","").replace("\t","").replace("\n","").replace(".","").replace("€","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Stock Center")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cheapbasket(u):
    
    url = "https://cheapbasket.com.cy/product/" + Item_url_
    response = requests.get(url)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        if ("New Products" in soup.get_text()):
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        else:
            element_ = soup.find_all("div",{"class":"shop-detail-right klb-product-right"})
            element_price = element_[0].find_all("span",{"class":"woocommerce-Price-amount amount"})
            price_ = element_price[0].text.replace("€","").replace(" ","").replace(",",".")
            
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Cheap Basket")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_opacy(u):
    
    url_ = "https://opa.cy/product/" + Item_url_
    response = requests.get(url_)
    
    if (response.status_code != 200) or ("Oops! It seems we are missing something." in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        element_ = soup.find_all("span",{"class":"product-span price"})
        price_ = element_[0].text.replace("Price: €","")
        
        if (name_=="Tomatoes Ripe for Salsa")|(name_=="Cucumbers fleid")|(name_=="Red Onions")|(name_=="Cucumbers Greenhouse")|(name_=="Cherry Tomatos"):
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_)*2) #since the price of the above 5 products is per 500g, we multiply *2 to have Eur/Kg 
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Opa")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Opa")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

# Run the code
for u in range(0, len(urls)):
    print(u)
    
    # Create a new row each time 
    new_row = []
    website_false = []
    
    # Read the data
    Item_url_ = urls["Url"].iloc[u]
    name_ = urls["Name"].iloc[u]
    print(name_)
    subclass_ = urls["Subclass"].iloc[u]
    division_ = urls["Division"].iloc[u]
    retailer_ = urls["Retailer"].iloc[u]

    if retailer_=="SupermarketCy":
        results_supermarketcy(u)
    #elif retailer_=="Alphamega":
        #results_alphamega(u)    
    #elif retailer_=="Cheap Basket":
        #results_cheapbasket(u)
    #elif retailer_=="Opa":
        #results_opacy(u)    
    elif retailer_=="Fuel Daddy":
        results_fuelDaddy(u)
    elif retailer_=="Costas Theodorou":
        results_costastheodorou(u)
    elif retailer_=="Parga":
        results_parga(u)    
    elif retailer_=="leroymerlin":
        results_leroymerlin(u)   
    elif retailer_=="IKEA":
        results_IKEA(u)
    elif retailer_=="Stephanis":
        results_stephanis(u)
    elif retailer_=="Electroline":
        results_electroline(u)
    elif retailer_=="CYTA":
        results_CYTA(u)
    elif retailer_=="Cablenet":
        results_cablenet(u)  
    elif retailer_=="Primetel":
        results_primetel(u)    
    elif retailer_=="Epic":
        results_epic(u)
    elif retailer_=="Athlokinisi":
        results_Athlokinisi(u)
    elif retailer_=="FamousSports":
        results_famoussport(u) 
    elif retailer_=="Marks&Spencer":
        results_Marks_Spencer(u)    
    elif retailer_=="Bwell Pharmacy":
        results_bwell_pharmacy(u)
    elif retailer_=="Novella":
        results_novella(u) 
    elif retailer_=="Evdokia Jewellery":
        results_evdokia(u)
    elif retailer_=="LensesCY":
        results_lensescy(u)    
    elif retailer_=="Centroptical":
        results_centroptical(u)
    elif retailer_=="Premier Laundry":
        results_premier(u)
    elif retailer_=="Music Avenue":
        results_musicavenue(u)    
    elif retailer_=="Rio Cinema":
        results_rio(u)    
    elif retailer_=="Cyprus Ministry of Education, Sport and Youth":
        results_CyMinistryEducation(u)
    elif retailer_=="European University Cyprus":
        results_europeanuniversitycyprus(u)    
    elif retailer_=="Cyprus Post":
        results_CyPost(u)
    elif retailer_=="AHK":
        results_AHK(u)
    elif retailer_=="Cyprus Energy Regulatory Authority":
        results_CERA(u)
    elif (retailer_=="Water Board of Larnaca") or (retailer_=="Water Board of Limassol") or (retailer_=="Water Board of Nicosia"):
        results_water(u)
    elif (retailer_=="Sewerage Board of Nicosia") or (retailer_=="Sewerage Board of Larnaca") or (retailer_=="Sewerage Board of Limassol"):
        results_sewerage(u)    
    elif retailer_=="MotoRace":
        results_moto_race(u)
    elif retailer_=="AWOL":
        results_AWOL(u)    
    elif retailer_=="Toyota":
        results_toyota(u)    
    elif retailer_=="Nissan":
        results_nissan(u)
    elif retailer_=="Stock Center":
        stock_center_results(u)    
    elif retailer_=="Alter Vape":
        results_alter_Vape(u)    
    elif retailer_=="The CYgar shop":
        results_CYgar_shop(u)
    elif retailer_=="The royal cigars":
        results_the_royal_cigars(u)  
    elif retailer_=="E-wholesale":
        results_ewholesale(u)    
    elif retailer_=="NUMBEO":
        results_numbeo(u)
    elif retailer_=="Wolt":
        results_wolt(u)
    elif retailer_=="Vasos Psarolimano":
        results_vasos(u)
    elif retailer_=="Meze Tavern":
        results_meze(u)    
    elif retailer_=="Pyxida":
        results_pydixa(u)
    elif retailer_=="Ithaki":
        results_ithaki(u)
    elif retailer_=="Flames":
        results_flames(u)
    elif retailer_=="Intercity Buses":
        results_intercity(u)  
    elif retailer_=="Cyprus Transport":
        results_cyprus_transport(u)
    elif retailer_=="Max 7 Taxi":
        results_max_7_tax(u)    

#================================================================================
# Manually added data            

"""
#Stock Center - The Used Car Experts (https://www.stock-center.com.cy/el/searchresults/?cg=&mk=&md=&yf=2000&yt=2024&km=0&cf=0&ct=1600&et=&pf=0&pt=15000&mp=0&ar=#page_1)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("NISSAN MICRA 1.0 PETROL AUTOMATIC 1000cc 2")
new_row.append(float(12500))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Stock Center") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Toyota (https://www.toyota.com.cy/new-cars)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Aygo X")
new_row.append(float(17700))
new_row.append("New motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyota") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("The New Toyota Yaris")
new_row.append(float(24900))
new_row.append("New motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyota") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("The New Toyota Yaris Cross")
new_row.append(float(27900))
new_row.append("New motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyota") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Intercity Buses (https://intercity-buses.com/en/routes/)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)nicosia-limassol-limassol-nicosia/")
new_row.append(float(5.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)larnaca-nicosia-nicosia-larnaca/")
new_row.append(float(4.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)nicosia-ayia-napa-paralimni-ayia-napa-paralimni-nicosia/")
new_row.append(float(5.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)nicosia-paphos-paphos-nicosia/")
new_row.append(float(7.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)larnaca-limassol-limassol-larnaca/")
new_row.append(float(4.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)larnaca-ayia-napa-paralimni-paralimni-ayia-napa-larnaca/")
new_row.append(float(4.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)limassol-paphos-paphos-limassol/")
new_row.append(float(4.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)paralimni-ayia-napa-larnaca-paphos-paphos-larnaca-ayia-napa-paralimni/")
new_row.append(float(9.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("OneWay(Paperticketfromthedriverorwiththemotioncarde-wallet)larnaca-limassol-paphos-paphos-limassol-larnaca/")
new_row.append(float(8.0))
new_row.append("Passenger transport by bus and coach")
new_row.append("TRANSPORT")
new_row.append("Intercity Buses") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#AHK (https://www.eac.com.cy/EL/RegulatedActivities/Supply/tariffs/Pages/supply-tariffs.aspx)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κόστος Ενέργειας για κάθε παρεχόμενη μονάδα")
new_row.append(float(0.1035))
new_row.append("Electricity")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("AHK") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κόστος Δικτύου για κάθε παρεχόμενη μονάδα")
new_row.append(float(0.0305))
new_row.append("Electricity")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("AHK") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κόστος Επικουρικών Υπηρεσιών  για κάθε παρεχόμενη μονάδα")
new_row.append(float(0.0065))
new_row.append("Electricity")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("AHK") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κόστος Προμήθειας")
new_row.append(float(6.08))
new_row.append("Electricity")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("AHK") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

## Primetel (https://primetel.com.cy/telephony-services)
#Wired telephone services 
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Calls to other providers landline")
new_row.append(float(0.03))
new_row.append("Wired telephone services")
new_row.append("COMMUNICATION")
new_row.append("Primetel") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Wireless telephone services 
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Calls to other providers landline")
new_row.append(float(0.095))
new_row.append("Wireless telephone services")
new_row.append("COMMUNICATION")
new_row.append("Primetel") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Water Board of Nicosia
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Πάγιο ανά μήνα - Nicosia")
new_row.append(float(5.5))
new_row.append("Water supply")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water Board") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
            
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κυβικά ανά μήνα - Nicosia")
new_row.append(float(1.0))
new_row.append("Water supply")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water Board") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Water Board of Larnaca
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Πάγιο ανά μήνα - Larnaca")
new_row.append(float(3.35))
new_row.append("Water supply")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water Board") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Δικαίωμα Συντήρησης ανά μήνα - Larnaca")
new_row.append(float(1.9))
new_row.append("Water supply")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water Board") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
"""

#Water Board of Larnaca
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κυβικά ανά μήνα - Larnaca")
new_row.append(float(1.0))
new_row.append("Water supply")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water Board") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Sewerage Board of Larnaca (https://eoal.org.cy/exypiretisi/teli/apocheteftika-teli/)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Ετήσιο Τέλος Larnaca")
new_row.append(float(0.4433333333333333))
new_row.append("Sewage collection")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage Board of Larnaca") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
            
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Τέλος Χρήσης Larnaca")
new_row.append(float(0.5))
new_row.append("Sewage collection")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage Board of Larnaca") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Epic (https://www.epic.com.cy/en/page/H1r10tnT/internet-telephony)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Internet and Telephony 10")
new_row.append(float(24.99))
new_row.append("Internet access provision services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Internet and Telephony 20")
new_row.append(float(29.99))
new_row.append("Internet access provision services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Internet and Telephony 50")
new_row.append(float(39.99))
new_row.append("Internet access provision services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("To fixed telephony lines of other providers")
new_row.append(float(0.03))
new_row.append("Wired telephone services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("To mobile telephony lines of other providers")
new_row.append(float(0.05))
new_row.append("Wireless telephone services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Epic (https://www.epic.com.cy/en/page/H1Q5Ad3p/mobile-plans)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("5G Unlimited Max Plus")
new_row.append(float(24.99))
new_row.append("Bundled telecommunication services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("5G Unlimited Max")
new_row.append(float(19.99))
new_row.append("Bundled telecommunication services")
new_row.append("COMMUNICATION")
new_row.append("Epic") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Meze Taverna (https://mezetaverna.com/wp-content/uploads/2024/11/MEZE-TAVERNA-ENGLISH-MENU.pdf)
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Meat Meze for 2 persons - Limassol")
new_row.append(float(22))
new_row.append("Restaurants, cafes and dancing establishments")
new_row.append("RESTAURANTS AND HOTELS")
new_row.append("Meze Tavern") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Fish Meze for 2 persons - Limassol")
new_row.append(float(25))
new_row.append("Restaurants, cafes and dancing establishments")
new_row.append("RESTAURANTS AND HOTELS")
new_row.append("Meze Tavern") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

###########################################################################################################################
# Christmas Offers 
###########################################################################################################################

#Primetel (https://primetel.com.cy/giga-unlimited --> https://primetel.com.cy/giga-unlimited-xmas24-en) 
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("GIGA Unlimited")
new_row.append(float(14.99))
new_row.append("Bundled telecommunication services")
new_row.append("COMMUNICATION")
new_row.append("Primetel") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("GIGA Unlimited Plus")
new_row.append(float(17.99))
new_row.append("Bundled telecommunication services")
new_row.append("COMMUNICATION")
new_row.append("Primetel") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("GIGA Unlimited MAX")
new_row.append(float(22.99))
new_row.append("Bundled telecommunication services")
new_row.append("COMMUNICATION")
new_row.append("Primetel") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#===============================================================================

# Change the type as float
list_["Price"].astype(float)

# Export/Save the scraped data
combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
#combined_df.to_csv("Datasets/Raw-Data.csv", index=False, header=True)
combined_df.to_csv("Datasets/Raw-Data-24q4.csv", index=False, header=True)
#combined_df.to_csv("Datasets/Raw-Data-2025Q1.csv", index=False, header=True)

monthly_errors=pd.read_csv("Datasets/Monthly-Scraping-Errors.csv")
daily_errors["Date"]=datetime.now().strftime('%Y-%m-%d')
combined_monthly=pd.concat([monthly_errors, daily_errors], axis=0)
combined_monthly.to_csv("Datasets/Monthly-Scraping-Errors.csv", index=False , header=True)
