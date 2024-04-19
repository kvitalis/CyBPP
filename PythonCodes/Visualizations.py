import pandas as pd
import matplotlib.pyplot as plt

df_=pd.read_csv("CPI and Inflation Results/CPI-General-Inflation.csv")

plt.figure(figsize=(10, 6))
plt.plot(df_['Date'], df_['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

for i, txt in enumerate(df_['Inflation (%)']):
    plt.annotate(f'{txt:.2f}', (df_['Date'][i], df_['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Evolution of Daily CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('CPI and Inflation Results/Inflation_Daily.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df_['Date'], df_['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')

for i, txt in enumerate(df_['CPI General']):
    plt.annotate(f'{txt:.5f}', (df_['Date'][i], df_['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('CPI General (08/04/2024 = base)')
plt.title("Evolution of Daily General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('CPI and Inflation Results/CPI_General_Daily.png')
plt.show()
