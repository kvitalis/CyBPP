## Important libraries
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

## Ignore specific warning
warnings.simplefilter("ignore")

## Read necessary data
df_data = pd.read_csv("CyFuelsPrices/Fuels_ScrapedData.csv")
df_stats = pd.read_csv("CyFuelsPrices/Fuels_PriceStatistics.csv")

## Date setup
today = datetime.today().strftime("%Y-%m-%d")
#today = '2025-02-13'
print(today)

df_date = df_data[df_data["Date"] == today]
new_row = []

## Fuels Prices Statistics

#Unleaded 95
df_type = df_date[df_date["Fuel Type"] == "Unleaded 95"]
unleaded95_avg = round(df_type["Price"].mean(),3)
print(unleaded95_avg)

#Unleaded 95
df_type = df_date[df_date["Fuel Type"] == "Unleaded 98"]
unleaded98_avg = round(df_type["Price"].mean(),3)
print(unleaded98_avg)

#Diesel
df_type = df_date[df_date["Fuel Type"] == "Diesel"]
diesel_avg = round(df_type["Price"].mean(),3)
print(diesel_avg)

#Heating Diesel
df_type = df_date[df_date["Fuel Type"] == "Heating Diesel"]
heatingdiesel_avg = round(df_type["Price"].mean(),3)
print(heatingdiesel_avg)

#Kerosene
df_type = df_date[df_date["Fuel Type"] == "Kerosene"]
kerosene_avg = round(df_type["Price"].mean(),3)
print(kerosene_avg)

## Save and export the fuels prices statistics calculations
df_stats.loc[len(df_stats)] = [today, unleaded95_avg, unleaded98_avg, diesel_avg, heatingdiesel_avg, kerosene_avg]
df_stats.to_csv("CyFuelsPrices/Fuels_PriceStatistics.csv", index = False)

## Visualizations/Plots
fuels_prices_stats = pd.read_csv("CyFuelsPrices/Fuels_PriceStatistics.csv")

#Evolution of the daily AVERAGE fuels prices
plt.figure(figsize=(12, 6))
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded95.CyprusAverage'], label='Unleaded 95 - Cyprus Average', marker='o', color='red')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded98.CyprusAverage'], label='Unleaded 98 - Cyprus Average', marker='o', color='blue')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Diesel.CyprusAverage'], label='Diesel - Cyprus Average', marker='o', color='black')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['HeatingDiesel.CyprusAverage'], label='Heating Diesel - Cyprus Average', marker='o', color='brown')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Kerosene.CyprusAverage'], label='Kerosene - Cyprus Average', marker='o', color='green')
plt.xlabel('Date')
plt.ylabel('Price (€/L)')
plt.title('Evolution of the daily average fuels prices in Cyprus')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('CyFuelsPrices/Fuels_Prices_Average_Evolution.png')
plt.show()

