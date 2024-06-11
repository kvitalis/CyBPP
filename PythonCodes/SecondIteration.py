import pandas as pd 
import re
import requests
import time
import xlsxwriter
import urllib.request
import json
import tabula as tb
import PyPDF2
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

print("1")
warnings.simplefilter("ignore")

#Read necessary data
df = pd.read_csv("Datasets/raw_data.csv")
urls = pd.read_csv("Datasets/DailyScrapingErrors.csv")
print("2")

#Create a null dataframe
daily_errors=pd.DataFrame(columns=["Name","Subclass","Url","Division","Retailer"])
list_=pd.DataFrame(columns=["Date","Name","Price","Subclass","Division","Retailer"])

def results_supermarketcy(urls):
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    url_new = "https://www.supermarketcy.com.cy/" + str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs,{'headers':header})
           
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        name_wrappers = soup.find('h1', {'class':"text-h6 md:text-h4 text-gray-dark font-bold mb-8 lg:mb-40 lg:max-w-520 leading-snug italic"}).text
        price_wrappers = soup.find('div', {'class':"text-primary text-24 lg:text-h3 font-bold italic my-4 lg:my-8"}).text
        value = price_wrappers.split('\xa0')[0].replace('.', '').replace(',', '.')
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_wrappers)
        new_row.append(float(value))
        new_row.append(subclass_)
        new_row.append(commotidy_)  
        new_row.append("SupermarketCy")
        list_.loc[len(list_)] = new_row
        list_["Name"] =list_["Name"].apply(lambda x:x)

"""
def results_alphamega(urls):
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
              "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
              "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
              "Accept-Encoding":"gzip, deflate, br, zstd",
              "Sec-Fetch-Mode":"navigate",
              "Upgrade-Insecure-Requests":"1",
              "Sec-Ch-Ua-Mobile":"?0",
              "Sec-Fetch-Site":"none",
              "Sec-Fetch-Dest":"document",
              "Sec-Fetch-User":"?1",
              "Sec-Ch-Ua-Platform":"macOS",
             "Cookie":"PriceAndActionsTemplate=PricesAndActionsTemplate; ProductSearchBarContentTemplate=SearchProductsTemplate; productListTemplate=ProductContainer; CookieInformationConsent=%7B%22website_uuid%22%3A%22ea90b431-dd9d-4865-8e36-58636aa46986%22%2C%22timestamp%22%3A%222023-06-15T21%3A39%3A59.041Z%22%2C%22consent_url%22%3A%22https%3A%2F%2Fwww.alphamega.com.cy%2Fel%2F%25CF%2580%25CF%2581%25CE%25BF%25CE%25B9%25CE%25BF%25CE%25BD%25CF%2584%25CE%25B1%2F%25CF%2586%25CF%2581%25CE%25B5%25CF%2583%25CE%25BA%25CE%25B1%2F%25CF%2586%25CE%25BF%25CF%2585%25CF%2581%25CE%25BD%25CE%25BF%25CF%2582%2F%25CF%2588%25CF%2589%25CE%25BC%25CE%25B9%2F%25CF%2588%25CF%2589%25CE%25BC%25CE%25B9-%25CE%25B6%25CE%25B5%25CE%25B1%25CF%2582-400-g%22%2C%22consent_website%22%3A%22alphamega.staging.dynamicweb-cms.com%22%2C%22consent_domain%22%3A%22www.alphamega.com.cy%22%2C%22user_uid%22%3A%22d3f9fbe2-b096-443f-b5e1-805599505663%22%2C%22consents_approved%22%3A%5B%22cookie_cat_necessary%22%2C%22cookie_cat_functional%22%2C%22cookie_cat_statistic%22%2C%22cookie_cat_marketing%22%2C%22cookie_cat_unclassified%22%5D%2C%22consents_denied%22%3A%5B%5D%2C%22user_agent%22%3A%22Mozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F113.0.0.0%20Safari%2F537.36%22%7D; ASP.NET_SessionId=14iuimihn4lz2ibafbjrcfvh; rsa=9E1E1A5D-2E6C-B8A6-8FB8-49C402EEA11E; _gcl_au=1.1.90441651.1708593336; _fbp=fb.2.1708593336575.123936726; _gid=GA1.3.1240817243.1708710009; rsaSession=31A85D7C-11D8-7A64-0A6D-490AAB949819; _ga=GA1.1.1031592513.1708593336; _ga_6L0WTPE54M=GS1.1.1708723542.4.1.1708725180.60.0.0; _uetsid=9686f300d27211eebbbd2b2154132f89; _uetvid=f0609fa0d16211ee8b6499903869154e",
             "Sec-Ch-Ua":'Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121'}
    
    url_new="https://www.alphamega.com.cy/en/groceries/food-cupboard/oils-vinegars-sauces-dressings/olive-oil/saint-george-cyprus-extra-virgin-olive-oil-1l"
    response = requests.get(url_new, headers=header)
    div_wapper=soup.find_all("div",{"class":"price price--product-page dw-mod"})#,"style":"display: inline;"})
    div_wapper_string = str(div_wapper)
    pattern_price = '"price":.*\,'
    pattern_name= '"name":.*\,'
    price_ini = re.findall(pattern_price,div_wapper_string)
    name_ini= re.findall(pattern_name,div_wapper_string)
    price_pattern = r'"price": "(\d+(?:,\d*)?\.\d+)"'
    name_pattern=r'"name": "(.*?)",'
    extracted_names = set()

    # Loop through the prices_list and extract the numeric values using the pattern
    for price_string in price_ini:
        match = re.search(price_pattern, price_string)
        if match:
            price=float(match.group(1).replace(',', '.'))
            print(price)
                
    for name_string in name_ini:
        match = re.search(name_pattern, name_string)
        if match:
            extracted_names.add(match.group(1))

    name = list(extracted_names)
        
    new_row= []
    new_row.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    new_row.append(name)
    new_row.append(price)
    new_row.append(subclass_)
    new_row.append(commotidy_)
    new_row.append("Alphamega")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)
"""

def results_fuelDaddy(urls):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_new = "https://www.fueldaddy.com.cy/" + str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs, {'headers':header})
    
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
            price_list=[]
            name = element_price[i].find(class_ = "brandtag cut-text fueltype-heading").get_text(strip = True)
            price = element_price[i].find(class_ = "pricetag").get_text(strip = True).replace(" €","")
            price_list.append(name)
            price_list.append(price)
        
            for i in range(1,len(price_list),2):
                new_row=[]
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                
                if price_list[i-1]=='Αμόλυβδη 95':
                    new_row.append(name_word+" - "+price_list[i-1])
                    new_row.append(float(price_list[i].replace(",",".")))
                    new_row.append("Petrol")
                    new_row.append("TRANSPORT")
            
                elif price_list[i-1]=='Αμόλυβδη 98':
                    new_row.append(name_word+" - "+price_list[i-1])
                    new_row.append(float(price_list[i].replace(",",".")))
                    new_row.append("Petrol")
                    new_row.append("TRANSPORT")
            
                elif price_list[i-1]=='Πετρέλαιο Κίνησης':
                    new_row.append(name_word+" - "+price_list[i-1])
                    new_row.append(float(price_list[i].replace(",",".")))
                    new_row.append("Diesel")
                    new_row.append("TRANSPORT")
             
                elif price_list[i-1]=='Πετρέλαιο Θέρμανσης':
                    new_row.append(name_word+" - "+price_list[i-1])
                    new_row.append(float(price_list[i].replace(",",".")))
                    new_row.append("Liquid fuels")
                    new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
               
                elif price_list[i-1]=='Κηροζίνη':
                    new_row.append(name_word+" - "+price_list[i-1])
                    new_row.append(float(price_list[i].replace(",",".")))
                    new_row.append("Liquid fuels")
                    new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
            
                new_row.append(brand_word) 
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ikea(u):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_new = "https://www.ikea.com.cy"+Item_url_
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)    
    
    if (response.status_code != 200) or ("ERROR 404" in response.text) or ("μήπως κάτι λείπει;" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
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
            new_row.append(commotidy_)
            new_row.append("IKEA")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_stefanis(u):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url_new="https://www.stephanis.com.cy/en"+str(Item_url_)
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code != 200) or ("This product is no longer available" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div",{"class":"listing-details-heading"})
        if (len(element_soup)<2):
            element_soup_1=element_soup[0]
        else:
            element_soup_1=element_soup[1]
            
        element_soup_1=element_soup_1.text
        element_soup_2=element_soup_1.replace("€","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(element_soup_2))
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("Stephanis")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cyta(u):
    q=0
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    if (response.status_code==200):
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div",{"class":"table-responsive"})
        for o in range(0,len(element_soup)):
            if "Κλήσεις προς" in element_soup[o].text:
                element_=element_soup[o]
                element_soup_1 = element_.find_all("td")
                for p in range(0, len(element_soup_1)):
                    ken=element_soup_1[p].text
                    if (ken==name_):
                        price_=element_soup_1[p+1].text.replace("€","").replace(",",".").replace(" /λεπτό","")
                        q=1
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
        new_row.append(commotidy_)
        new_row.append("CYTA")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_epic(u):
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code==200):
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup_price = soup.find_all("div",{"class":"price"})
        element_soup_name=soup.find_all("div",{"class":"mtn-name mtn-name-bb"})
        new_row=[]
       
        for q in range(0,len(element_soup_name)):
            new_row=[]
            _name_=element_soup_name[q].text.strip().replace(" ","")
            
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
                new_row.append(commotidy_)
                new_row.append("Epic")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_Athlokinisi(u):
    url="https://athlokinisi.com.cy"+Item_url_
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)   
        else:
            price_=float(element_soup[0].text.strip().replace("€",""))
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(commotidy_)
            new_row.append("Athlokinisi")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_awol(u):
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
        new_row.append("Alter Vape")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_bweel_pharmacy(u):
    url="https://bwell.com.cy/shop/health/"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404. The page you are looking for does not exist" in response.text)or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("div",{"class":"plan-price"}) 

        if (name_=="PurpleInternet") or (name_=="PurpleMaxMobile"):
            if name_=="PurpleInternet":
                qp=1
            if name_=="PurpleMaxMobile":
                qp=0
            euro_=element_soup[qp].text.count("€")
            price_=float(element_soup[qp].text.replace(" ",'').split("€")[euro_].split("/")[0])
        else:
            element_name = soup.find_all("td")

            for i in range(0,len(element_name)):
                if element_name[i].text==name_:
                    name_=element_name[i].text
                    price=element_name[i+3].text
                    price_=price.split(' ')[0].replace("€","")

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("Cablenet")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyMinistryEducation(u):
    url="http://archeia.moec.gov.cy/mc/698/"+Item_url_
    
    if "ΝΗΠΙΑΓΩΓΕΙΩΝ" in name_:
        pdf_ = tb.read_pdf(url, pages = '4',pandas_options={'header': None}, stream=True)
        pdf_ = pdf_[0]
        pdf_[2] = pdf_[2].astype('string')
        pdf = pdf_[2][1]
        price_ = float(pdf.strip('€*').replace(".", ""))
    
    if "ΔΗΜΟΤΙΚΩΝ" in name_:
        pdf_ = tb.read_pdf(url, pages = '1',pandas_options={'header': None}, stream=True)
        pdf_= pdf_[0]
        pdf_[3] = pdf_[3].astype('string')
        price_ = float(pdf_[3][26].strip('€').replace(".", ""))
                     
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
    new_row.append(commotidy_)
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
    new_row.append(commotidy_)
    new_row.append("Cyprus Post")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

"""
def results_ewholesale(u):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("span",{"data-hook":"formatted-primary-price"}) 
        price_=element_soup[0].text.replace("€","").replace(" ","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("E-wholesale")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
"""

def results_electroline(u):
    url="https://electroline.com.cy/products/"+Item_url_
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("ins",{"class":"product-price product-price--single product-price--sale-price product-price--single--sale-price"}) 
        if element_soup:
            price_=element_soup[0].text.replace("\n",'').replace("€","")
        else:
            element_soup = soup.find_all("h2",{"class":"product-price product-price--single"}) 
            price_=element_soup[0].text.replace("\n","").replace("€","")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("Electroline")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_europeanuniversitycyprus(u):
    euc = tb.read_pdf(Item_url_, pages = '2',pandas_options={'header': None}, stream=True)
    list_euc = []
    
    for i in range(0,4):
        new_row=[]
        euc[i][1] = euc[i][1].astype('string')
        
        for word in euc[i][1].to_list():
            word = word.replace(',','')
            word = int(word)
            list_euc.append(word)
    
        price_=(sum(list_euc)+21000+21900+(8940*5))/(len(list_euc)+7)
    
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
        new_row.append("Famous Sports")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_Marks_Spencer(u):
    url="https://www.marksandspencer.com/cy/regular-fit-pure-cotton-crew-neck-t-shirt/p/P60581522.html#index=0"
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("Sorry, we can't" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("span",{"class":"value"})
        price_=element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
        new_row.append("Moto Race")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_nissan(u):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(Item_url_, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("THIS IS A DEAD END..." in response.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        tree = html.fromstring(response.content)
        price_tree = tree.xpath('//iframe[@id="individualVehiclePriceJSON"]/text()')
        if price_tree:
            price_json = price_tree[0]
            price_data = json.loads(price_json)
            price_ = price_data[name_]['default']['grades']['LVL001']['gradePrice']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
                new_row.append(commotidy_)
                new_row.append("Novella")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
 
            elif (name_=="Men's Services, HAIRCUT Stylist") and (scripts_1[i].text== "MEN'S CUT"):
                price_=scripts_2[i].text.replace('€',"").replace(',','.')
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
                new_row.append(commotidy_)
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
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('div',{"class":"top_plan_box"})
        for i in range(0,len(element_name)):
            if element_name[i].text.replace("\n","")==name_:
                element_name = soup.find_all('div',{"class":"price_plan_box"})
                price_=element_name[i].text.replace("\n","").replace(" ","")
                price_=price_.split("€")
                
                if len(price_)>2:
                    price_=price_[2].replace("month","")
                else:
                    price_=price_[0]
                    
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
                        new_row.append(commotidy_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(commotidy_)
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
                        new_row.append(commotidy_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(commotidy_)
                        website_false.append(retailer_)
                        daily_errors.loc[len(daily_errors)] = website_false
                        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_ahk(u):
    response = requests.get(Item_url_)

    pdf = "PDFs/AHK.pdf"
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
    
        with open(pdf, "wb") as f:
            f.write(response.content)

        with open(pdf, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            page = pdf_reader.pages[2]
            text = page.extract_text()
    
        lines = text.split("\n")
        for line in lines:
            new_row=[]
            if name_ in line:
                ken=line.strip()
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
                    new_row.append(commotidy_)
                    new_row.append("AHK")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                else:
                    website_false.append(name_)
                    website_false.append(subclass_)
                    website_false.append(Item_url_)
                    website_false.append(commotidy_)
                    website_false.append(retailer_)
                    daily_errors.loc[len(daily_errors)] = website_false
                    daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_cera(u):
    response = requests.get(Item_url_)
    cera = tb.read_pdf(Item_url_, pages = '8',pandas_options={'header': None}, stream=True)
    amount_=cera[0][1].to_list()
    _names_=cera[0][0].to_list()
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:   
        for oo in range(0,len(_names_)-1):
            n1=_names_[oo]+" "+_names_[oo+1]
            if name_ in n1:
                price_=float(amount_[oo].replace(",","."))/100
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("Cyprus Energy Regulatory Authority")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_water(u):
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if "Nicosia" in retailer_:
        city_="Nicosia"
        element_name = soup.find_all('div',{"class":"ekit_table_body_container ekit_table_data_ ekit_body_align_center"})
        
        for qp in range(0,len(element_name)):
            if (element_name[qp].text.replace(" ","").replace("\n","")=="Πάγιο") and (name_=="Πάγιο ανά μήνα"):
                price_=element_name[1].text.replace(" ","").replace('\n',"").replace(",",".")
                price_=float(price_)/2
        
            elif (element_name[qp-2].text.replace(" ","").replace("\n","")=="1") and (element_name[qp-1].text.replace(" ","").replace("\n","")=="20") and (name_=="Κυβικά ανά μήνα"):
                price_=element_name[qp].text.replace(" ","").replace("\n","").replace(",",".")
        
    elif "Larnaca" in retailer_:
        city_="Larnaca"
        element_name = soup.find_all('td',{"colspan":"3"})
        element_name_2 = soup.find_all('table',{"border":"1","cellspacing":"3","cellpadding":"3"})
        element_name_3 = soup.find_all('td',{"style":"text-align: right;"})
    
        for ooo in range(0,len(element_name_2)):
            if (element_name[ooo].text=="Πάγιο") and (name_=="Πάγιο ανά μήνα"):
                price_=float(element_name_3[ooo].text.replace(",","."))/3
            elif (element_name[ooo].text=="Δικαίωμα Συντήρησης") and (name_=="Δικαίωμα Συντήρησης ανά μήνα"):
                price_=float(element_name_3[ooo].text.replace(",","."))/3

        element_name_4 = soup.find_all('td')
        for o in range(0,len(element_name_4)):
            if (element_name_4[o-3].text=="1") and (element_name_4[o-1].text=="15") and (name_=="Κυβικά ανά μήνα"):
                price_=float(element_name_4[o].text.replace(",","."))
    
    elif "Limassol" in retailer_:
        city_="Limassol"
        element_name = soup.find_all('table',{"class":"table table-striped table-nonfluid table-bordered table-sm"})
        element_name_2 = element_name[0].find_all('tr')
        for o in range(0,len(element_name_2)):
            if ("Πάγιο Τέλος" in element_name_2[o].text) and (name_=="Πάγιο ανά μήνα"):
                price_=element_name_2[o].text
                matches_1 = re.findall(r'\d+,\d+', price_)
                if matches_1:
                    price_ = float(matches_1[0].replace(",","."))/4
            elif ("Τέλος Συντήρησης" in element_name_2[o].text) and (name_=="Δικαίωμα Συντήρησης ανά μήνα"):
                price_=element_name_2[o].text
                matches_1 = re.findall(r'\d+,\d+', price_)
                if matches_1:
                    price_ = float(matches_1[0].replace(",","."))/4

        element_name_2 = element_name[1].find_all('td') 
        for o in range(0,len(element_name_2)):
            if (element_name_2[o-2].text=="1") and (element_name_2[o-1].text=="40") and(name_=="Κυβικά ανά μήνα"):
                price_=float(element_name_2[o].text.replace(",","."))
                #matches_2= re.findall(r'\d+,\d+', price_)
                #if matches_2:
                #    price_ = float(matches_2[0].replace(",","."))
    
    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_+" - "+city_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("Water Board")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
        website_false.append(commotidy_)
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
            new_row.append(commotidy_)
            new_row.append("Wolt")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
            new_row.append(commotidy_)
            new_row.append("Meze Tavern")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_CYgar_shop(u):
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_name = soup.find_all('div',{"class":"hM4gpp"})

    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        if element_name:
            price_value=element_name[0].text
            price_match = re.search(r'\d+\.\d+', price_value)

            if price_match:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_match.group()))
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("The CYgar shop")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_the_royal_cigars(u):
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
            new_row.append(commotidy_)
            new_row.append("The Royal Cigars")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_pydixa(u):
    response = requests.get(Item_url_)
    
    if response.status_code!=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        pdf = "PDFs/pixida.pdf"
        
        with open(pdf, "wb") as f:
            f.write(response.content)
        
        with pdfplumber.open(pdf) as pdf:
            page = pdf.pages[5]  
            text = page.extract_text()

        matches = re.findall(r'Ψαρομεζές .*?(\d+\.\d+)', text)
        
        if matches:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))        
            new_row.append(name_)
            new_row.append(float(matches[0]))
            new_row.append(subclass_)
            new_row.append(commotidy_)
            new_row.append("Pyxida")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_sewerage(u):
    values=0
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
        
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        if "Nicosia" in retailer_:
            new_row=[]
            city_="Nicosia"
            element_name = soup.find_all('li',{"style":"padding-left: 30px;"})
            
            if "Ετήσιο Τέλος" in name_:
                for i in range(0,len(element_name)):
                    price_amount=element_name[i].text
                    match = re.search(r'€(\d+,\d+)', price_amount)
                    if match:
                        value = float(match.group(1).replace(",","."))
                        values=value+values
                    else:
                        no_website(Item_url_)
                values=values/3
            
            if "Τέλος Χρήσης" in name_:
                element_name = soup.find_all('p',{"style":"padding-left: 30px;"})
                new_row=[]
                for i in range(0,len(element_name)):
                    price_amount=element_name[i].text
                    match = re.search(r'(\d+)', price_amount)

                    if match:
                        values = float(match.group(1))/100
                    else:
                        no_website(Item_url_)
        
        elif "Limassol" in retailer_:
            city_="Limassol"
            new_row=[]
            
            if "Ετήσιο Τέλος" in name_:
                element_name = soup.find_all('table',{"class":"table table-bordered"})
                element_name_2 = element_name[0].find_all('tr')[35]
                desired_lines = [element_name_2.find_all('td')[4].get_text(), element_name_2.find_all('td')[6].get_text()]

                for lines in desired_lines:
                    value=float(lines.replace(",","."))
                    values=value+values
                
                values=values/2
            
            if "Τέλος Χρήσης" in name_:
                element_name = soup.find_all('table',{"class":"table table-bordered"})
                element_name_2 = element_name[1].find_all('tr')
                element_name_2=element_name_2[len(element_name_2)-1]
                desired_lines = [element_name_2.find_all('td')[1].get_text()]
                
                for lines in desired_lines:
                    values=float(lines.replace(",","."))
                    
        elif "Larnaca" in retailer_:
            city_="Larnaca"
            new_row=[]
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

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_+" "+city_)
        new_row.append(values)
        new_row.append(subclass_)
        new_row.append(commotidy_)
        new_row.append("Sewerage Board of "+ city_)
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_toyta(u):
    if (name_=="YARIS CROSS"):
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
        if response.status_code !=200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Yaris Cross"})
            element_soup2=element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})

            for element_ in element_soup2:
                price_ = float(element_['data-price'])
            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("Toyta")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)   
    else:    
        if subclass_=="New motor cars":
            bs = BeautifulSoup(Item_url_, "html.parser")
            response = requests.get(bs)
            soup = BeautifulSoup(response.content, "html.parser")
            element_name = soup.find_all('span',{"data-test-id":"model-keyspecs-price-card-cash-price-value"})
    
            if element_name:
                price_=element_name[0].text.replace("€","").replace(",","").replace("\n","").replace(" ","")
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("Toyta")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        
        elif subclass_=="Second-hand motor cars":
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
            bs = BeautifulSoup(Item_url_, "html.parser")
            response = requests.get(bs)
            soup = BeautifulSoup(response.content, "html.parser")
            isnone = soup.find("div", {"role": "cpdqm_ignore"}).text

            if isnone==None:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
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
                    new_row.append(commotidy_)
                    new_row.append("Toyta")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                else:
                    website_false.append(name_)
                    website_false.append(subclass_)
                    website_false.append(Item_url_)
                    website_false.append(commotidy_)
                    website_false.append(retailer_)
                    daily_errors.loc[len(daily_errors)] = website_false
                    daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_ithaki(u):
    response = requests.get(Item_url_)
    pdf = "PDFs/ithaki.pdf"

    with pdfplumber.open(pdf) as pdf:
        first_page = pdf.pages[5]
        text = first_page.extract_text()
        
    pattern = r'(\d+.*?\d+\.\d{2})'
    matches = re.findall(pattern, text)
    
    for match in matches:
        new_row=[]
        website_false=[]
        if ("Ποικιλία Κρεατικών" in match) and ("Ποικιλία Κρεατικών - Larnaca" in name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)

            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
            
        elif ("Ποικιλία Θαλασσινών" in match) and ("Ποικιλία Θαλασσινών - Larnaca" in name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)

            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(commotidy_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(commotidy_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_flames(u):
    response = requests.get(Item_url_)
    pdf = "PDFs/flames.pdf"
    
    with open(pdf, "wb") as f:
        f.write(response.content)

    with pdfplumber.open(pdf) as pdf:
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

        if price_:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_[-1]))
            new_row.append(subclass_)
            new_row.append(commotidy_)
            new_row.append("Flames")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_lensescy(u):
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header})
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        table_=soup.find_all("table",{"class":"tablesorter eael-data-table center"})[0]
        if table_:
            element_=table_.find_all("div",{"class":"td-content"})
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
                        new_row.append(commotidy_)
                        new_row.append("Intercity Buses")
                        list_.loc[len(list_)] = new_row
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
        new_row.append("Evdokia Jewellery")
        list_.loc[len(list_)] = new_row

def results_centroptical(u):
    response=requests.get(Item_url_, headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
                new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
            new_row.append(commotidy_)
            new_row.append("Max 7 Taxi") 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_costastheodorou(u):
    response = requests.get(Item_url_)

    if (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(commotidy_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_=soup.find_all("p",{"class":"price"})
        price_=element_[0].text.replace("€","")
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(commotidy_)
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
        website_false.append(commotidy_)
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
        new_row.append(commotidy_)
        new_row.append("Leroy Merlin") 
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

#Calculation of the processing time
start_time = time.time()

#Run the code
for u in range(0,len(urls)):
    print(u)
    
    #Create null row each time 
    new_row=[]
    website_false=[]
    
    #Read the data
    Item_url_=urls["Url"].iloc[u]
    name_=urls["Name"].iloc[u]
    subclass_=urls["Subclass"].iloc[u]
    commotidy_=urls["Division"].iloc[u]
    retailer_=urls["Retailer"].iloc[u]

    if retailer_=="SupermarketCy":
        results_supermarketcy(u)
    #elif retailer_=="Alphamega":
        #results_alphamega(u)
    elif retailer_=="Fuel Daddy":
        results_fuelDaddy(u)
    elif retailer_=="IKEA":
        results_ikea(u)
    elif retailer_=="Stephanis":
        results_stefanis(u)
    elif retailer_=="CYTA":
        results_cyta(u)
    elif retailer_=="Epic":
        results_epic(u)
    elif retailer_=="Athlokinisi":
        results_Athlokinisi(u)
    elif retailer_=="AWOL":
        results_awol(u)
    elif retailer_=="Alter Vape":
        results_alter_Vape(u)
    elif retailer_=="Bwell Pharmacy":
        results_bweel_pharmacy(u)
    elif retailer_=="Cablenet":
        results_cablenet(u)
    elif retailer_=="Cyprus Ministry of Education, Sport and Youth":
        results_CyMinistryEducation(u)
    elif retailer_=="Cyprus Post":
        results_CyPost(u)
    #elif retailer_=="E-wholesale":
     #   results_ewholesale(u)
    elif retailer_=="Electroline":
        results_electroline(u)
    elif retailer_=="European University Cyprus":
        results_europeanuniversitycyprus(u)
    elif retailer_=="FamousSports":
        results_famoussport(u)
    elif retailer_=="Marks&Spencer":
        results_Marks_Spencer(u)
    elif retailer_=="MotoRace":
        results_moto_race(u)
    elif retailer_=="Nissan":
        results_nissan(u)
    elif retailer_=="Novella":
        results_novella(u)
    elif retailer_=="NUMBEO":
        results_numbeo(u)
    elif retailer_=="Primetel":
        results_primetel(u)
    elif retailer_=="Rio Cinema":
        results_rio(u)
    elif retailer_=="AHK":
        results_ahk(u)
    elif retailer_=="Cyprus Energy Regulatory Authority":
        results_cera(u)
    elif (retailer_=="Water Board of Larnaca") or (retailer_=="Water Board of Limassol") or (retailer_=="Water Board of Nicosia"):
        results_water(u)
    elif retailer_=="Wolt":
        results_wolt(u)
    elif retailer_=="Vasos Psarolimano":
        results_vasos(u)
    elif retailer_=="Meze Tavern":
        results_meze(u)
    elif retailer_=="The CYgar shop":
        results_CYgar_shop(u)
    elif retailer_=="The royal cigars":
        results_the_royal_cigars(u)
    elif (retailer_=="Sewerage Board of Nicosia") or (retailer_=="Sewerage Board of Limassol")or (retailer_=="Sewerage Board of Larnaca"):
        results_sewerage(u)
    elif retailer_=="Pyxida":
        results_pydixa(u)
    elif retailer_=="Toyta":
        results_toyta(u)
    elif retailer_=="Ithaki":
        results_ithaki(u)
    elif retailer_=="Flames":
        results_flames(u)
    elif retailer_=="LensesCY":
        results_lensescy(u)
    elif retailer_=="Intercity Buses":
        results_intercity(u)  
    elif retailer_=="Parga":
        results_parga(u)
    elif retailer_=="Evdokia Jewellery":
        results_evdokia(u)
    elif retailer_=="Centroptical":
        results_centroptical(u)
    elif retailer_=="Premier Laundry":
        results_premier(u)
    elif retailer_=="Cyprus Transport":
        results_cyprus_transport(u)
    elif retailer_=="Music Avenue":
        results_musicavenue(u)
    elif retailer_=="Max 7 Taxi":
        results_max_7_tax(u)
    elif retailer_=="leroymerlin":
        results_leroymerlin(u)
    elif retailer_=="Costas Theodorou":
        results_costastheodorou(u)

#Manually added data
"""
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Aygo-X")
new_row.append(float(17700.0))
new_row.append("New motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("YARIS CROSS")
new_row.append(float(28500.0))
new_row.append("New motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Aygo - Aygo 1.0 x-wave x-shift")
new_row.append(float(13980.00))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Yaris - Yaris 1.5 HSD Style+")
new_row.append(float(13780.00))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Yaris - Yaris 1.5 Active CVT")
new_row.append(float(19600.00))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Aygo X - Aygo X play Canvas CVT(fleet)")
new_row.append(float(19240.0))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Toyota Aygo X - Aygo X play Canvas CVT(fleet)")
new_row.append(float(18720.0))
new_row.append("Second-hand motor cars")
new_row.append("TRANSPORT")
new_row.append("Toyta") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
"""
#Change the type as float
list_["Price"].astype(float)

combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
combined_df.to_csv("Datasets/raw_data.csv", index=False, header=True)

annual_errors=pd.read_csv("Datasets/MonthlyScrapingErrors.csv")
daily_errors["Date"]=datetime.now().strftime('%Y-%m-%d')
combined_annual=pd.concat([annual_errors, daily_errors], axis=0)
combined_annual.to_csv("Datasets/MonthlyScrapingErrors.csv", index=False , header=True)
