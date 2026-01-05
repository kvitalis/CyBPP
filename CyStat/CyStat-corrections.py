# Important libraries
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

### GENERAL Consumer Price Index

# Read csv files
df_1 = pd.read_csv(r"CyStat/General-CPI-Offline-VS-Online.csv")
df_1 = df_1.rename(columns = {"Period": "Date"})

df_2 = pd.read_csv(r"Results/Monthly/Monthly-CPI-General-Inflation.csv")
df_2['Date'] = pd.to_datetime(df_2['Date'], errors='coerce')
df_2['Date'] = df_2['Date'].dt.strftime('%Y-%m')

# Match the corresponding columns for ONLINE between the two csv files/datasets
df_1 = pd.merge(df_1, df_2, on='Date', how='inner')
df_1["Online (27/06/2024=77.89)"] = round( df_2["CPI General"], 2 ) 
df_1["Online Inflation (%)"] = round( df_2["Inflation (%)"], 2 )
del df_1['CPI General'] 
del df_1['Inflation (%)'] 
df_1 = df_1.rename(columns = {"Date": "Period"})

# Rebase the Official and Online GENERAL CPI in order to compare them
base_value = df_1.loc[df_1["Period"] == "2024-06", "Official (2015=100)"].iloc[0]
base_value_2 = df_1.loc[df_1["Period"] == "2024-06", "Online (27/06/2024=77.89)"].iloc[0]
df_1["Official (27/06/2024=100)"] = round( (df_1["Official (2015=100)"] / base_value * 100), 2 )
df_1["Online (27/06/2024=100)"] = round( (df_1["Online (27/06/2024=77.89)"] / base_value_2 * 100), 2 )

# Calculate GENERAL CPI Inflation 
#df_1["Official Inflation (%)"] = round((df_1["Official (27/06/2024=100)"].pct_change() * 100),2)
#df_1["Online Inflation (%)"] = round((df_1["Online (27/06/2024=77.89)"].pct_change() * 100),2)

df_1.to_csv(r"CyStat/General-CPI-Offline-VS-Online-Correct.csv", index=False)

## Visualize the results for GENERAL CPI
df_gen_cpi = pd.read_csv(r"CyStat/General-CPI-Offline-VS-Online-Correct.csv")

#Plot: Official vs Online GENERAL CPI
plt.figure(figsize=(12, 6))
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Official (2015=100)'], label='Official (2015=100)', marker='o', color='red')
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Online (27/06/2024=77.89)'], label='Online (27/06/2024=77.89)', marker='o', color='blue')
plt.xlabel('Period')
plt.ylabel('General CPI')
plt.title('Official vs Online General CPI')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig("CyStat/General_Offline_Vs_Online/Official-vs-Online-General-CPI-Correct.png")

#Plot: Official vs Online GENERAL CPI *rebased*
plt.figure(figsize=(12, 6))
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Official (27/06/2024=100)'], label='Official', marker='o', color='red')
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Online (27/06/2024=100)'], label='Online', marker='o', color='blue')
plt.xlabel('Period')
plt.ylabel('General CPI (27/06/2024=100)')
plt.title('Official vs Online General CPI (rebased)')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig("CyStat/General_Offline_Vs_Online/Official-vs-Online-General-CPI-rebased-Correct.png")

#Plot: Official vs Online GENERAL CPI Inflation
plt.figure(figsize=(12, 6))
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Official Inflation (%)'], label='Official/Offline', marker='o', color='red')
plt.plot(df_gen_cpi['Period'], df_gen_cpi['Online Inflation (%)'], label='Online', marker='o', color='blue')
plt.xlabel('Period')
plt.ylabel('Inflation (%)')
plt.title('Official vs Online Inflation')
plt.legend()
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig("CyStat/General_Offline_Vs_Online/Official-vs-Online-Inflation-Correct.png")

### DIVISION Consumer Price Index

# Read csv files
df_3 = pd.read_csv(r"CyStat/Division-CPI-Offline-VS-Online.csv")

df_3['Division'] = df_3['Division'].str.strip()
df_3['Division'] = (df_3['Division'].str.strip().str.replace('\u00a0',' ',regex=False))
df_3['Division'] = (df_3['Division'].str.normalize('NFKD').str.strip())
del df_3['Online CPI']
df_3['new_column'] = df_3['Period']+'#'+df_3['Division']

df_4 = pd.read_csv(r"Results/Monthly/Monthly-CPI-Division.csv")

df_4['Date'] = pd.to_datetime(df_4['Date'])
df_4['Date'] = df_4['Date'].dt.strftime('%Y-%m')
df_4['new_column'] = df_4['Date']+'#'+df_4['Division']
df_4['Division'] = df_4['Division'].str.strip()
df_4['Division'] = (df_4['Division'].str.strip().str.replace('\u00a0', ' ', regex=False))
df_4['Division'] = (df_4['Division'].str.normalize('NFKD').str.strip())
df_4 = df_4[['new_column', 'CPI Division']]

# Match the corresponding columns for ONLINE between the two csv files/datasets
merged_df = pd.merge(df_3, df_4, on='new_column', how='inner') 
merged_df = merged_df.rename(columns={'CPI Division': 'Online CPI'})

del merged_df['new_column']

merged_df = merged_df[['Period', 'Division', 'Official CPI', 'Online CPI', 'Official Monthly Change (%)', 'Online Monthly Change (%)']]
merged_df['Online CPI'] = round( merged_df['Online CPI'], 2 ) 

# Calculate DIVISION CPI Inflation
merged_df = merged_df.sort_values(['Division', 'Period'])
merged_df['Official Monthly Change (%)'] = (merged_df.groupby('Division')['Official CPI'].pct_change() * 100)
merged_df['Online Monthly Change (%)'] = (merged_df.groupby('Division')['Online CPI'].pct_change() * 100)

merged_df.to_csv(r"CyStat/Division-CPI-Offline-VS-Online-Correct.csv", index= False)

## Visualize the results for DIVISION CPI
df_div_cpi = pd.read_csv(r"CyStat/Division-CPI-Offline-VS-Online-Correct.csv")

df_div_cpi["Period"] = pd.to_datetime(df_div_cpi["Period"], format="%Y-%m", errors="coerce")
divisions = df_div_cpi["Division"].unique()

#Plots: Official vs Online CPI per DIVISION
for div in divisions:
    
    df_new = pd.DataFrame(columns = ["Date", "Offline CPI", "Online CPI"])
    df_div = df_div_cpi[df_div_cpi["Division"] == div][["Period", "Official CPI", "Online CPI"]].reset_index(drop=True)

    base_value = df_div.loc[0, "Official CPI"]

    for i in range(len(df_div)):
        date = df_div.loc[i, "Period"]
        offline_cpi = (df_div.loc[i, "Official CPI"] / base_value) * 100
        online_cpi = df_div.loc[i, "Online CPI"]

        df_new.loc[len(df_new)] = [date, offline_cpi, online_cpi]

    df_new["Date"] = pd.to_datetime(df_new["Date"])

    plt.figure(figsize=(10, 6))
    plt.plot(df_new["Date"], df_new["Offline CPI"], marker="o", label="Official")
    plt.plot(df_new["Date"], df_new["Online CPI"], marker="o", label="Online")
    plt.title(div)
    plt.xlabel("Date")
    plt.ylabel("CPI (rebased)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(df_new["Date"], df_new["Date"].dt.strftime("%Y-%m"), rotation=90)
    filename = div.replace(" ", "_").replace(",", "") + "_CPI_rebased_Correct.png"
    plt.savefig(rf"CyStat/Division_Offline_Vs_Online/{filename}", dpi=300)
    
#Plots: Official vs Online CPI Inflation per DIVISION
for div in divisions:
    
    df_div = df_div_cpi[df_div_cpi["Division"] == div].copy()
    df_div["Date"] = pd.to_datetime(df_div["Period"], format="%Y-%m")

    plt.figure(figsize=(10, 6))
    plt.plot(df_div["Date"], df_div["Official Monthly Change (%)"], marker="o", label="Official")
    plt.plot(df_div["Date"], df_div["Online Monthly Change (%)"], marker="o", label="Online")
    plt.title(div)
    plt.xlabel("Date")
    plt.ylabel("Monthly Inflation (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(df_div["Date"], df_div["Date"].dt.strftime("%Y-%m"), rotation=90)
    filename = div.replace(" ", "_").replace(",", "") + "_Inflation_Correct.png"
    plt.savefig(rf"CyStat/Division_Offline_Vs_Online/{filename}", dpi=300)
    
