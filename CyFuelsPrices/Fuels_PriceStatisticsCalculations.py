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

### Fuels Prices Statistics

## Unleaded 95
df_type = df_date[df_date["Fuel Type"] == "Unleaded 95"]
#Mean/Average
unleaded95_avg = round(df_type["Price"].mean(),3)
print(unleaded95_avg)
#Minimum
unleaded95_min = round(df_type["Price"].min(),3)
print(unleaded95_min)
#Maximum
unleaded95_max = round(df_type["Price"].max(),3)
print(unleaded95_max)
#Median/2nd Quartile
unleaded95_q2 = round(df_type["Price"].median(),3)
print(unleaded95_q2)

## Unleaded 98
df_type = df_date[df_date["Fuel Type"] == "Unleaded 98"]
#Mean/Average
unleaded98_avg = round(df_type["Price"].mean(),3)
print(unleaded98_avg)
#Minimum
unleaded98_min = round(df_type["Price"].min(),3)
print(unleaded98_min)
#Maximum
unleaded98_max = round(df_type["Price"].max(),3)
print(unleaded98_max)
#Median/2nd Quartile
unleaded98_q2 = round(df_type["Price"].median(),3)
print(unleaded98_q2)

## Diesel
df_type = df_date[df_date["Fuel Type"] == "Diesel"]
#Mean/Average
diesel_avg = round(df_type["Price"].mean(),3)
print(diesel_avg)
#Minimum
diesel_min = round(df_type["Price"].min(),3)
print(diesel_min)
#Maximum
diesel_max = round(df_type["Price"].max(),3)
print(diesel_max)
#Median/2nd Quartile
diesel_q2 = round(df_type["Price"].median(),3)
print(diesel_q2)

## Heating Diesel
df_type = df_date[df_date["Fuel Type"] == "Heating Diesel"]
#Mean/Average
heatingdiesel_avg = round(df_type["Price"].mean(),3)
print(heatingdiesel_avg)
#Minimum
heatingdiesel_min = round(df_type["Price"].min(),3)
print(heatingdiesel_min)
#Maximum
heatingdiesel_max = round(df_type["Price"].max(),3)
print(heatingdiesel_max)
#Median/2nd Quartile
heatingdiesel_q2 = round(df_type["Price"].median(),3)
print(heatingdiesel_q2)

## Kerosene
df_type = df_date[df_date["Fuel Type"] == "Kerosene"]
#Mean/Average
kerosene_avg = round(df_type["Price"].mean(),3)
print(kerosene_avg)
#Minimum
kerosene_min = round(df_type["Price"].min(),3)
print(kerosene_min)
#Maximum
kerosene_max = round(df_type["Price"].max(),3)
print(kerosene_max)
#Median/2nd Quartile
kerosene_q2 = round(df_type["Price"].median(),3)
print(kerosene_q2)

## Save and export the fuels prices statistics calculations
df_stats.loc[len(df_stats)] = [today, unleaded95_avg, unleaded98_avg, diesel_avg, heatingdiesel_avg, kerosene_avg, unleaded95_min, unleaded98_min, diesel_min, heatingdiesel_min, kerosene_min, unleaded95_max, unleaded98_max, diesel_max, heatingdiesel_max, kerosene_max, unleaded95_q2, unleaded98_q2, diesel_q2, heatingdiesel_q2, kerosene_q2]
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

#Evolution of the daily MINIMUM fuels prices
plt.figure(figsize=(12, 6))
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded95.CyprusMin'], label='Unleaded 95 - Cyprus Minimum', marker='o', color='red')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded98.CyprusMin'], label='Unleaded 98 - Cyprus Minimum', marker='o', color='blue')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Diesel.CyprusMin'], label='Diesel - Cyprus Minimum', marker='o', color='black')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['HeatingDiesel.CyprusMin'], label='Heating Diesel - Cyprus Minimum', marker='o', color='brown')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Kerosene.CyprusMin'], label='Kerosene - Cyprus Minimum', marker='o', color='green')
plt.xlabel('Date')
plt.ylabel('Price (€/L)')
plt.title('Evolution of the daily minimum fuels prices in Cyprus')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('CyFuelsPrices/Fuels_Prices_Minimum_Evolution.png')
plt.show()

#Evolution of the daily MAXIMUM fuels prices
plt.figure(figsize=(12, 6))
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded95.CyprusMax'], label='Unleaded 95 - Cyprus Maximum', marker='o', color='red')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded98.CyprusMax'], label='Unleaded 98 - Cyprus Maximum', marker='o', color='blue')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Diesel.CyprusMax'], label='Diesel - Cyprus Maximum', marker='o', color='black')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['HeatingDiesel.CyprusMax'], label='Heating Diesel - Cyprus Maximum', marker='o', color='brown')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Kerosene.CyprusMax'], label='Kerosene - Cyprus Maximum', marker='o', color='green')
plt.xlabel('Date')
plt.ylabel('Price (€/L)')
plt.title('Evolution of the daily maximum fuels prices in Cyprus')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('CyFuelsPrices/Fuels_Prices_Maximum_Evolution.png')
plt.show()

#Evolution of the daily MEDIAN fuels prices
plt.figure(figsize=(12, 6))
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded95.CyprusMedian'], label='Unleaded 95 - Cyprus Median', marker='o', color='red')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Unleaded98.CyprusMedian'], label='Unleaded 98 - Cyprus Median', marker='o', color='blue')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Diesel.CyprusMedian'], label='Diesel - Cyprus Median', marker='o', color='black')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['HeatingDiesel.CyprusMedian'], label='Heating Diesel - Cyprus Median', marker='o', color='brown')
plt.plot(fuels_prices_stats['Date'], fuels_prices_stats['Kerosene.CyprusMedian'], label='Kerosene - Cyprus Median', marker='o', color='green')
plt.xlabel('Date')
plt.ylabel('Price (€/L)')
plt.title('Evolution of the daily median fuels prices in Cyprus')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.savefig('CyFuelsPrices/Fuels_Prices_Median_Evolution.png')
plt.show()
