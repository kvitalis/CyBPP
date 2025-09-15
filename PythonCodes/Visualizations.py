#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import datetime, timedelta 

"""
#Import data
df_daily = pd.read_csv("Results/Daily-CPI-General-Inflation.csv")

plt.figure(figsize=(10, 6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

## Plot the time evolution of the daily CPI Inflation

# Show on the horizontal x-axis only the date of the first day per month 
df_daily['Date'] = pd.to_datetime(df_daily['Date'])
plt.figure(figsize=(12,6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], marker='o')

for date, cpi in zip(df_daily['Date'], df_daily['Inflation (%)']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords="offset points", xytext=(0,10), ha='center')

locator = mdates.DayLocator(bymonthday=1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-Inflation.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily['Inflation (%)']):
    plt.annotate(f'{txt:.2f}', (df_daily['Date'][i], df_daily['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-Inflation.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], linestyle='-', marker='o', color='b', label='CPI General')
'''

## Plot the time evolution of the daily General CPI

# Show on the horizontal x-axis only the date of the first day per month
df_daily['Date'] = pd.to_datetime(df_daily['Date'])
plt.figure(figsize=(12,6))
plt.plot(df_daily['Date'], df_daily['CPI General'], marker='o')

for date, cpi in zip(df_daily['Date'], df_daily['CPI General']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords="offset points", xytext=(0,10), ha='center')

locator = mdates.DayLocator(bymonthday=1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('CPI General (27/06/2024 = base = 77.89)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-CPI-General.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily['CPI General']):
    plt.annotate(f'{txt:.2f}', (df_daily['Date'][i], df_daily['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('CPI General (27/06/2024 = base)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily-CPI-General.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily['Date'], df_daily['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')
'''

#========================================================================================================================
# LAST THURSDAY (*this corresponds to the monthly observation*)
#========================================================================================================================

#Current date
#current_date = '2024-09-26'
current_date = datetime.today().strftime("%Y-%m-%d")

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

    #Plot the time evolution of the monthly CPI Inflation
    for i, txt in enumerate(df_monthly['Inflation (%)']):
        plt.annotate(f'{txt:.2f}', (df_monthly['Date'][i], df_monthly['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
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

    #Plot the time evolution of the monthly General CPI 
    for i, txt in enumerate(df_monthly['CPI General']):
        plt.annotate(f'{txt:.2f}', (df_monthly['Date'][i], df_monthly['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
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
"""

#Plots: Official vs Online *rebased* CPI per Division
df_ = pd.read_csv(r"CyStat/Division-CPI-Offline-VS-Online.csv")
df_["Period"] = pd.to_datetime(df_["Period"], format="%Y-%m", errors="coerce")
division_ = df_['Division'].unique()

for div_ in division_:
    df_new = pd.DataFrame(columns=["Date", "Offline CPI", "Online CPI"])
    df_1 = df_[df_["Division"] == div_]
    df_1 = df_1[["Period" , "Official CPI" , "Online CPI"]]
    df_1 = df_1.reset_index(drop=True)
    df_1["Period"] = pd.to_datetime(df_1["Period"], format="%Y-%m")

    df_1_first_vales_ = df_1.loc[ 0 , 'Official CPI']

    for jj in range(0,len(df_1)-1):
        new_row_= []
        values_0 = df_.loc[ ((jj*12)+jj) , "Period"]
        values_1 = (df_1.loc[jj , 'Official CPI'] / df_1_first_vales_)*100
        values_2 = (df_1.loc[jj , 'Online CPI'])
        new_row_.append(values_0)
        new_row_.append(float(values_1))
        new_row_.append(float(values_2))
        print(new_row_)
        df_new.loc[len(df_new)] = new_row_
        df_new["Date"] = df_new["Date"].apply(lambda x:x)
        df_new["Date"] = pd.to_datetime(df_new["Date"], format="%Y-%m", errors="coerce")

    plt.figure(figsize=(10, 6))
    plt.plot(df_new["Date"], df_new["Offline CPI"], marker="o", color="blue", label="Offline")
    plt.plot(df_new["Date"], df_new["Online CPI"], marker="o", color="red", label="Online")
        
    plt.title(f"{div_}")
    plt.xlabel("Date")
    plt.ylabel("CPI (rebased)")
    plt.legend()
    plt.grid(True)
    plt.xticks(df_new["Date"], df_new["Date"].dt.strftime("%Y-%m"), rotation=90)
    plt.show()
                      
    filename = div_.replace(" ", "_").replace(",", "") + "_CPI_rebased.png"
    full_path = f"CyStat/Division_Offline_Vs_Online/"
    path_ = full_path + filename
    plt.savefig(path_, dpi=300)
    plt.show()

#Plots: Official vs Online Inflation per Division    
division_ = pd.read_csv("CyStat/Division-CPI-Offline-VS-Online.csv")
division_name_ = division_["Division"].unique()

for jj in division_name_ :
    division_1 = division_[division_["Division"] == jj]       
    division_name = division_1["Division"].iloc[0]
    division_1["Date"] = pd.to_datetime(division_1["Period"], format="%Y-%m")
           
    plt.figure(figsize=(10, 6))
    plt.plot(division_1 ["Date"], division_1["Official Monthly Change (%)"], marker="o", color="blue", label="Official")
    plt.plot(division_1 ["Date"], division_1["Online Monthly Change (%)"], marker="o", color="red", label="Online")
                  
    # Τίτλος και labels
    plt.title(jj)
    plt.xlabel("Date")
    plt.ylabel("Monthly Inflation (%)")
    plt.legend()
    plt.grid(True)
    
    # Ετικέτες άξονα Χ μόνο με μήνα-έτος
    plt.xticks(division_1["Date"], division_1["Date"].dt.strftime("%Y-%m"), rotation=90)
                      
    filename = division_name.replace(" ", "_").replace(",", "") + "_Inflation.png"
    full_path = f"CyStat/Division_Offline_Vs_Online/"
    path_ = full_path + filename
    plt.savefig(path_, dpi=300)
    plt.show()
