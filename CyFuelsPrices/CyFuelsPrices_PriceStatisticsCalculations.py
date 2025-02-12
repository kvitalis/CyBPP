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
df_data = pd.read_csv("CyFuelsPrices/CyFuelsPrices_ScrapedData.csv")
df_stats = pd.read_csv("CyFuelsPrices/CyFuelsPrices_PriceStatistics.csv")

df_12=df_data[df_data["Date"]=="2025-02-11"]
df_23 = df_12[df_12["Fuel Type"] == "Unleaded 95"]
average_price_value_23=df_23.mean()
print(average_price_value_23)

#fuel_group = df_data.groupby("Fuel Type").mean()
#average_price = fuel_group["Price"].mean()
#print(average_price)
#df_stats.loc[len(df_stats)]=[,,,,,]
