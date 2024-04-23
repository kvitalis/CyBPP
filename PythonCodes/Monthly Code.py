import pandas as pd
from datetime import datetime, timedelta

#Current date
current_date = datetime.now().strftime("%Y-%m-%d")

#Read importnat files
df_=pd.read_csv("Results/CPI-General-Inflation.csv")
df_montly_data=pd.read_csv("Results Monthly/CPI-General-Inflation-Monthly.csv")

#Fuction's calculation of last Thursday
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days=7)).month:
        return True
    return False

if is_last_thursday(current_date):
    df_current_date=df_[df_["Date"]==current_date]
    df_montly_data = df_montly_data.append(df_current_date, ignore_index=True)
    df_montly_data["Inflation]=None
    df_montly_data.to_csv("Results Monthly/CPI-General-Inflation-Monthly.csv")
else:
    pass
