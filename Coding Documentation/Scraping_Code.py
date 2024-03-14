# John John
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

warnings.simplefilter("ignore")

filename="/Users/kendeas/Desktop/CypERN/04.Billion Prices Cyprus/Testing_.xlsx"

df = pd.read_excel(filename)
urls=pd.read_excel("/Users/kendeas/Desktop/CypERN/04.Billion Prices Cyprus/Product_urls.xlsx")
no_website=[]
list_=pd.DataFrame(columns=["Date","Name","Price","Subclass","Comitidy","Retailer"])


def results_ikea(u):
    new_row = []
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    Item_url_=urls["Item.url"].iloc[u]
    url_new = "https://www.ikea.com.cy"+Item_url_
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)    
    if (response.status_code != 200) or ("ERROR 404" in response.text) or ("μήπως κάτι λείπει;" in response.text):
        no_website.append(response)
        pass
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
            new_row.append(comitidy_)
            new_row.append("IKEA")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
            

for u in range(0,len(urls)):
    Item_url_=urls["Item.url"].iloc[u]
    name_=urls["Name"].iloc[u]
    subclass_=urls["subclass"].iloc[u]
    comitidy_=urls["Division"].iloc[u]
    retailer_=urls["Retailer"].iloc[u]
    if retailer_=="IKEA":
        results_ikea(u)
        
df = pd.concat([df, list_], ignore_index=True)
df.to_excel(filename, index=False) 
