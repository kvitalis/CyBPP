import pandas as pd
import matplotlib.pyplot as plt

df_=pd.read_csv("CPI and Inflation Results/CPI-General-Inflation.csv")

plt.figure(figsize=(10, 6))
plt.plot(df_['Date'], df_['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

for i, txt in enumerate(df_['Inflation (%)']):
    plt.annotate(f'{txt:.2f}', (df_['Date'][i], df_['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Cyprus' Inflation (%)", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('CPI and Inflation Results/Inflation.png')
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(df_['Date'], df_['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')

for i, txt in enumerate(df_['CPI General']):
    plt.annotate(f'{txt:.5f}', (df_['Date'][i], df_['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('CPI General')
plt.title("Cyprus' CPI General", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('CPI and Inflation Results/CPI_General.png')
plt.show()
