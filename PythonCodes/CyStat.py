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
import tabula
import datetime

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
from tabula import read_pdf
import fitz
from docx import Document
from io import StringIO
from babel.dates import format_date
from datetime import date, timedelta

#Important funcition
def cystat(last_results):
    
    #Read importnat files
    cystat_=pd.read_csv("/Users/kendeas/Desktop/CPI_Offline_Vs_Online.csv")
    online_per_=pd.read_csv("/Users/kendeas/Desktop/Monthly-CPI-General-Inflation.csv")
    
    #Main part of web scrapping 
    url_new="https://www.cystat.gov.cy/el/SubthemeStatistics?id=47"
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_1=soup.find_all("div",{"class":"col-12 col-md-12 col-lg-6 col-xl-6"})

    #Calculation of Month
    current_date = datetime.now()
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    current_month =current_date.month-1
    current_year = current_date.year
    current_day = current_date.day
    date = datetime(current_year, current_month,current_day)
    date_=format_date(date, 'MMMM', locale='el')

    #Fix the month
    if (current_month==6) or (current_month==7):
        _date_=date_[:4]
    elif (current_month==5):
        _date_="Μάιος"
    else:
        _date_=date_[:3]

    #Specifed the index of website
    for jj in range(0,len(element_1)):
        if "Δείκτης Τιμών Καταναλωτή - Πληθωρισμός" in element_1[jj].text:
            if _date_ in element_1[jj].text:
                match = re.search(r'%\s*(\S+)', element_1[jj].text)
                if match:
                    percentage_value = match.group(1)
                    if percentage_value==_date_:
                        corrent_jj=jj

    #Identified the correct document for the current month
    anchors = element_1[int(corrent_jj)].find_all('a')
    hrefs = [a.get('href') for a in anchors]
    for href in hrefs:
        url_href=href
        

    #Main part of the documents
    url_months="https://www.cystat.gov.cy/el"+url_href
    bs = BeautifulSoup(url_months, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_soup = soup.find_all("a")
    for i in soup.find_all('a'):
        if i.find('span') and "Λήψη Αρχείου Word" in i.find('span').text:
            url = i['href']

    response = requests.get(url)
    if response.status_code == 200:
        with open('/Users/kendeas/Desktop/Consumer_Price_Index-'+str(current_month)+'.docx', 'wb') as file:
            file.write(response.content)

    doc = Document('/Users/kendeas/Desktop/Consumer_Price_Index-'+str(current_month)+'.docx')
    doc_text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                doc_text += cell.text + "\t"
            doc_text += "\n"  

    pattern = r"Γενικός Δείκτης Τιμών Καταναλωτή\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})"
    match = re.search(pattern, doc_text)

    pattern1 = r"Τρόφιμα και μη Αλκοολούχα Ποτά\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})"
    match1 = re.search(pattern1, doc_text)

    if match:
        cpi_month = match.groups()
        cpi_month=float(cpi_month[1].replace(",","."))
        
        #identified the month CPI General
        online_per_['Date'] = pd.to_datetime(online_per_['Date'])
        date_to_find =last_results
        index = online_per_.index[online_per_['Date'] == date_to_find].tolist()
        values_12=float(online_per_.loc[index,"CPI General"])
        
        calcu_1= (cpi_month*100) /float(117.72)
        calcu_2= (values_12*100) /float(77.89)

        df_new_empty_ = pd.DataFrame()
        df_new_empty_.loc[0,"Period"]=str(_date_)+"-24"
        df_new_empty_.loc[0,"Official (2015=100)"]= float(cpi_month)
        df_new_empty_.loc[0,"Online (27/06/2024=77.89)"]=values_12
        df_new_empty_.loc[0,"Official (27/06/2024=100)"]=calcu_1
        df_new_empty_.loc[0,"Online (27/06/2024=100)"]=calcu_2
        
        df_tables = pd.concat([cystat_, df_new_empty_], ignore_index=True)
        df_tables.loc[len(df_tables)-1,"Official (%)"] = 100 * (df_tables.loc[len(df_tables)-1,"Official (27/06/2024=100)"] - df_tables.loc[len(df_tables)-2,"Official (27/06/2024=100)"]) / df_tables.loc[len(df_tables)-2,"Official (27/06/2024=100)"]
        df_tables.loc[len(df_tables)-1,"Online (%)"] = 100 * (df_tables.loc[len(df_tables)-1,"Online (27/06/2024=77.89)"] - df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"]) / df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"]
        df_tables.to_excel("/Users/kendeas/Desktop/CPI_Offline_Vs_Online.xlsx",index=False)
        
    if match1:
        values_after_gd = match1.groups()
        #print(values_after_gd[1])

def is_first_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date - timedelta(days=7)).month:
        last_results=date - timedelta(days=7)
        last_results = last_results.strftime("%Y-%m-%d")
        cystat(last_results)
    else:
        pass

#Call function
current_date = datetime.now().strftime("%Y-%m-%d")
is_first_thursday(current_date)    
