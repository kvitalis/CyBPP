
# Important Libraries
import pandas as pd 
from datetime import datetime
import warnings
from datetime import datetime, timedelta

# Ignore specific warning
warnings.simplefilter("ignore")

print("0")

today=datetime.today().strftime("%Y-%m-%d")

#Read necessacry data
raw_data_=pd.read_csv("StoredScrapedData/raw_data.csv")
cpi_division=pd.read_excel("CPI and Inflation Results/CPI-Division.xlsx")
weight_=pd.read_excel("CPI and Inflation Results/Weight_.xlsx")
index_=pd.read_excel("CPI and Inflation Results/Index_2024-04-08.xlsx")

# CPI/ Division

row_data_today=raw_data_[raw_data_["Date"]==today]
group=row_data_today.groupby("Subclass").mean()
group.reset_index(inplace=True)
group_df = pd.DataFrame(group)

group_df = group_df[group_df["Subclass"] != "Electricity"]
group_df = group_df[group_df["Subclass"] != "Water supply"]
group_df = group_df[group_df["Subclass"] != "Sewage collection"]
group_df = group_df.reset_index(drop=True)

print("1")

#Electricity
electricity=row_data_today[row_data_today["Subclass"]=="Electricity"]
ele_price_=electricity["Price"].sum()
new_row=[]
new_row.append("Electricity")
new_row.append(ele_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

print("2")

waterboard=row_data_today[row_data_today["Subclass"]=="Water supply"]

larnaca_=0
nicosia_=0
limassol_=0

for i in range(0,len(waterboard)):
    if "Larnaca" in waterboard.iloc[i]["Name"]:
        larnaca_+=waterboard.iloc[i]["Price"]
    if "Nicosia" in waterboard.iloc[i]["Name"]:
        nicosia_+=waterboard.iloc[i]["Price"]
    if "Limassol" in waterboard.iloc[i]["Name"]:
        limassol_+=waterboard.iloc[i]["Price"]
        
wat_price_=(larnaca_+nicosia_+limassol_)/3
new_row=[]
new_row.append("Water supply")
new_row.append(wat_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

print("3")

sewagecollection=row_data_today[row_data_today["Subclass"]=="Sewage collection"]

larnaca_=0
larnaca_count=0
nicosia_=0
nicosia_count=0
limassol_=0
limassol_count=0

for i in range(0,len(sewagecollection)):
    if "Larnaca" in sewagecollection.iloc[i]["Name"]:
        larnaca_+=sewagecollection.iloc[i]["Price"]
        larnaca_count+=1
    if "Nicosia" in sewagecollection.iloc[i]["Name"]:
        nicosia_+=sewagecollection.iloc[i]["Price"]
        nicosia_count+=1
    if "Limassol" in sewagecollection.iloc[i]["Name"]:
        limassol_+=sewagecollection.iloc[i]["Price"]
        limassol_count+=1
        
sew_price_=((larnaca_/larnaca_count)+(nicosia_/nicosia_count)+(limassol_/limassol_count))/3
new_row=[]
new_row.append("Sewage collection")
new_row.append(sew_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

print("4")

weight_=pd.read_excel("CPI and Inflation Results/03.00.Weight_.xlsx")
df_1 = pd.merge(group_df, weight_, on='Subclass')
df_1["Weight_Price_Subclass"]=df_1["Price"]*df_1["Weight"]

print("5")

df_2=df_1.groupby("Subclass").sum()
df_2.reset_index(inplace=True)

df_3=pd.merge(df_2, weight_, on='Subclass')
df_3=df_3[["Subclass","Division","Price","Weight_Price_Subclass","Weight_x"]]
df_3.rename(columns={'Weight_x': 'Weight'}, inplace=True)

print("6")

df_4=df_3.groupby("Division").sum()
df_4.reset_index(inplace=True)
df_4.rename(columns={'Weight_Price_Subclass': 'Weight_Price_Division_today'}, inplace=True)

print("7")

df_5 = pd.merge(index_, df_4, on='Division')
df_5["CPI Division"]=(df_5["Weight_Price_Division_today"]/df_5["Weight_Price_Division_Index"])*100
df_5=df_5[["Division","CPI Division","Weight_Price_Division_today"]]
df_5.rename(columns={'Weight_Price_Division_today': 'Weight_Price_Division'}, inplace=True)

print("8")

df_6=pd.merge(df_1, df_5, on='Division')
df_6["Date"]= None
df_6=df_6[["Date","Subclass","Division","Price","Weight","Weight_Price_Subclass","Weight_Price_Division","CPI Division"]]
df_6["Date"] =today

print("9")

combined_df = pd.concat([cpi_division, df_6], axis=0)
combined_df.to_excel("CPI and Inflation Results/CPI-Division.xlsx",index=False)

# CPI/ General /Infation

df_99=index_[["Division","Weight"]]

#Cleaning Data
df_101=df_6[["Division","CPI Division"]]
df_102 = df_101.drop_duplicates()

print("10")

#Merged dataframes
df_103 = pd.merge(df_102, df_99, on='Division')
df_103["New"]=df_103["CPI Division"]*df_103["Weight"]
Cpi_general=df_103["New"].sum()/100

#Read excel file
df_104=pd.read_excel("CPI and Inflation Results/CPI-General-Inflation.xlsx")

print("11")

#Creatited null list and add information
new_row=[]
new_row.append(today)
new_row.append(Cpi_general)
new_row.append(None)

print("12")

#Combinted the two dataframe
df_105 = pd.DataFrame([new_row], columns=['Date', 'CPI General', 'Inflation'])
df_106= pd.concat([df_104, df_105],ignore_index=True)
df_106['Inflation']= (df_106['CPI General'] - df_106['CPI General'].shift(1)) / df_106['CPI General'].shift(1)
df_106.to_excel("CPI-General-Inflation.xlsx", index=False)
