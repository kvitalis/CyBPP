#Import libraries
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import datetime, timedelta 

#Import data
df_daily = pd.read_csv("Results/Daily-CPI-General-Inflation.csv")

plt.figure(figsize=(10, 6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

for i, txt in enumerate(df_daily['Inflation (%)']):
    plt.annotate(f'{txt:.3f}', (df_daily['Date'][i], df_daily['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-Inflation.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df_daily['Date'], df_daily['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')

for i, txt in enumerate(df_daily['CPI General']):
    plt.annotate(f'{txt:.3f}', (df_daily['Date'][i], df_daily['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('CPI General (27/06/2024 = base)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-CPI-General.png')
plt.show()

#========================================================================================================================
# LAST THURSDAY (*this corresponds to the monthly observation*)
#========================================================================================================================

#Current date
#current_date = '2024-09-26'
current_date = today_date.strftime("%Y-%m-%d")

#Read data
df_monthly = pd.read_csv("Results/Monthly-CPI-General-Inflation.csv")

#Function to run every last Thursday per month
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days=7)).month:
        return True
    return False

if is_last_thursday(current_date):
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['Date'], df_monthly['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')
    
    for i, txt in enumerate(df_monthly['Inflation (%)']):
        plt.annotate(f'{txt:.3f}', (df_monthly['Date'][i], df_monthly['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.xlabel('Date')
    plt.ylabel('Inflation (%)')
    plt.title("Monthly Evolution of CPI Inflation in Cyprus", fontsize=18)
    plt.xticks(rotation=90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Results/Monthly-Inflation.png')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['Date'], df_monthly['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')
    
    for i, txt in enumerate(df_monthly['CPI General']):
        plt.annotate(f'{txt:.3f}', (df_monthly['Date'][i], df_monthly['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.xlabel('Date')
    plt.ylabel('CPI General (27/06/2024 = base)')
    plt.title("Monthly Evolution of General CPI in Cyprus", fontsize=18)
    plt.xticks(rotation=90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Results/Monthly-CPI-General.png')
    plt.show()
else:
    pass
