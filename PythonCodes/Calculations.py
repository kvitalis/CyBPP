# Important Libraries
import pandas as pd 
import warnings
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import datetime, timedelta

# Ignore specific warning
warnings.simplefilter("ignore")

today=datetime.today().strftime("%Y-%m-%d")
#today='2024-07-24'

#CALCULATIONS

#Read necessary data 
raw_data_=pd.read_csv("Datasets/raw_data.csv", parse_dates=['Date'], date_parser=lambda x:pd.to_datetime(x, format='%Y-%m-%d'))
#raw_data_['Date'] = pd.to_datetime(raw_data_['Date'], format='%Y-%m-%d')
cpi_division=pd.read_csv("Results/CPI-Subclass-Division.csv")
weight_=pd.read_csv("Datasets/Weights_Cystat.csv")
index_=pd.read_csv("Datasets/Reference_Values.csv")
_cpi_=pd.read_csv("Results/CPI-Division.csv")

#DIVISION CPI
row_data_today=raw_data_[raw_data_["Date"]==today]
row_data_1=row_data_today[["Subclass","Price"]]
group=row_data_1.groupby("Subclass").mean()
group.reset_index(inplace=True)
group_df = pd.DataFrame(group)

group_df = group_df[group_df["Subclass"] != "Electricity"] #dont take into account the electricity subclass
group_df = group_df[group_df["Subclass"] != "Water supply"] #dont take into account the Water supply subclass
group_df = group_df[group_df["Subclass"] != "Sewage collection"] #dont take into account the Sewage Collection subclass
group_df = group_df.reset_index(drop=True) #Reset index of the above three subclasses

#Electricity
electricity=row_data_today[row_data_today["Subclass"]=="Electricity"]
ele_price_=electricity["Price"].sum()
new_row=[]
new_row.append("Electricity")
new_row.append(ele_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

#Water Board
waterboard=row_data_today[row_data_today["Subclass"]=="Water supply"]

larnaca_=0
larnaca_count=0
nicosia_=0
nicosia_count=0
limassol_=0
limassol_count=0

for i in range(0,len(waterboard)):
    if "Larnaca" in waterboard.iloc[i]["Name"]:
        larnaca_+=waterboard.iloc[i]["Price"]
        larnaca_count=1
    if "Nicosia" in waterboard.iloc[i]["Name"]:
        nicosia_+=waterboard.iloc[i]["Price"]
        nicosia_count=1
    if "Limassol" in waterboard.iloc[i]["Name"]:
        limassol_+=waterboard.iloc[i]["Price"]
        limassol_count=1
        
wat_price_= (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
new_row=[]
new_row.append("Water supply")
new_row.append(wat_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

#Sewage collection
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
        larnaca_count=1
    if "Nicosia" in sewagecollection.iloc[i]["Name"]:
        nicosia_+=sewagecollection.iloc[i]["Price"]
        nicosia_count=1
    if "Limassol" in sewagecollection.iloc[i]["Name"]:
        limassol_+=sewagecollection.iloc[i]["Price"]
        limassol_count=1
        
sew_price_= (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
new_row=[]
new_row.append("Sewage collection")
new_row.append(sew_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

#weight_=pd.read_csv("Datasets/Weights_Cystat.csv")
df_1 = pd.merge(group_df, weight_, on='Subclass')
df_1["Weight_Price_Subclass"]=df_1["Price"]*df_1["Weight"]

df_2=df_1.groupby("Subclass").sum()
df_2.reset_index(inplace=True)

df_3=pd.merge(df_2, weight_, on='Subclass')
#df_3.to_csv("Results/ken.csv", index=False)
df_3=df_3[["Subclass","Division_x","Price","Weight_Price_Subclass","Weight_x"]]
df_3.rename(columns={'Weight_x': 'Weight','Division_x':'Division'}, inplace=True)

df_4=df_3.groupby("Division").sum()
df_4.reset_index(inplace=True)
df_4.rename(columns={'Weight_Price_Subclass': 'Weight_Price_Division_today'}, inplace=True)

df_5 = pd.merge(index_, df_4, on='Division')
df_5["CPI Division"]=(df_5["Weight_Price_Division_today"]/df_5["Weight_Price_Division_Index"])*100
df_5=df_5[["Division","CPI Division","Weight_Price_Division_today"]]
df_5.rename(columns={'Weight_Price_Division_today': 'Weight_Price_Division'}, inplace=True)
df_5["Date"]=today

cols = list(df_5.columns)
cols.insert(0, cols.pop(cols.index('Date')))
df_5 = df_5[cols]
df_5['Date'] = pd.to_datetime(df_5['Date']) 

df_5_a = pd.concat([df_5, _cpi_])
df_5_a['Date'] = pd.to_datetime(df_5_a['Date'])
df_5_a = df_5_a.sort_values(by='Date').reset_index(drop=True)
df_5_a.to_csv("Results/CPI-Division.csv",index=False)

del df_5["Date"]

df_6=pd.merge(df_1, df_5, on='Division')
df_6["Date"]= None
df_6=df_6[["Date","Subclass","Division","Price","Weight","Weight_Price_Subclass","Weight_Price_Division","CPI Division"]]
df_6["Date"] =today

combined_df = pd.concat([cpi_division, df_6], axis=0)
combined_df.to_csv("Results/CPI-Subclass-Division.csv",index=False)

#General CPI Inflation
df_99=index_[["Division","Weight"]]

#Cleaning Data
df_101=df_6[["Division","CPI Division"]]
df_102 = df_101.drop_duplicates()

#Merge dataframes
df_103 = pd.merge(df_102, df_99, on='Division')
df_103["New"]=df_103["CPI Division"]*df_103["Weight"]
Cpi_general=df_103["New"].sum()

#Read csv file
df_104=pd.read_csv("Results/CPI-General-Inflation.csv")

#Creat null list and add information
new_row=[]
new_row.append(today)
new_row.append(Cpi_general)
new_row.append(None)

#Combine the two dataframes
df_105 = pd.DataFrame([new_row], columns=['Date', 'CPI General', 'Inflation (%)'])
df_106= pd.concat([df_104, df_105],ignore_index=True)
df_106['Inflation (%)']= 100*(df_106['CPI General'] - df_106['CPI General'].shift(1)) / df_106['CPI General'].shift(1)
df_106.to_csv("Results/CPI-General-Inflation.csv", index=False)

## LAST THURSDAY (*this corresponds to the monthly observation*)
#Current date
current_date = datetime.now().strftime("%Y-%m-%d")

#Read importnat files
df_=pd.read_csv("Results/CPI-General-Inflation.csv")
df_monthly_data=pd.read_csv("Results/Monthly-CPI-General-Inflation.csv")
df_montly_division=pd.read_csv("Results/Monthly-CPI-Division.csv")

#Function's calculation of last Thursday
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days=7)).month:
        return True
    return False

#Call the function
if is_last_thursday(current_date):
    df_current_date = df_[df_["Date"] == current_date]
    
    #Monthly-CPI-Division
    df_montly_division=pd.concat([df_5, df_montly_division], ignore_index=True)
    df_montly_division = df_montly_division.sort_values(by ='Date')

    prior_df=df_montly_division[len(df_montly_division)-24:len(df_montly_division)-12]
    current_df=df_montly_division[len(df_montly_division)-12:len(df_montly_division)]
    unique_divisions = df_montly_division['Division'].unique()

    for unique_ in unique_divisions:
        df_1=float(prior_df[prior_df["Division"]==unique_]["CPI Division"])
        df_2=float(current_df[current_df["Division"]==unique_]["CPI Division"])
        calculation=((df_2-df_1)/df_1)*100
    
        index_list = current_df[current_df["Division"]==unique_]["CPI Division"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        df_montly_division.loc[float_index_list,"Monthly Change (%)"]=calculation

    df_montly_division.to_csv("Results/Monthly-CPI-Division.csv",index=False)

    #Monthly-CPI-General-Inflation
    df_monthly_data = pd.concat([df_current_date, df_monthly_data], ignore_index=True)
    df_monthly_data = df_monthly_data.sort_values(by ='Date')
    df_monthly_data["Inflation (%)"] = 100 * (df_monthly_data['CPI General'] - df_monthly_data['CPI General'].shift(1)) / df_monthly_data['CPI General'].shift(1)    
    df_monthly_data.to_csv("Results/Monthly-CPI-General-Inflation.csv", index=False)
else:
    pass

def cystat(last_results):
    
    #Read importnat files
    cystat_=pd.read_csv("CyStat/CPI_Offline_Vs_Online.csv")
    online_per_=pd.read_csv("Results/Monthly-CPI-General-Inflation.csv")
    
    #Main part of web scrapping 
    url_new="https://www.cystat.gov.cy/el/SubthemeStatistics?id=47"
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_1=soup.find_all("div",{"class":"col-12 col-md-12 col-lg-6 col-xl-6"})

    #Calculation of Month
    current_date = datetime.now()
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    current_month =current_date.month-1
    current_year = current_date.year
    current_day = current_date.day
    date = datetime(current_year, current_month,current_day)
    date_=format_date(date, 'MMMM', locale='el')

    #Fix the month
    if (current_month==6) or (current_month==7):
        _date_=date_[:4]
    elif (current_month==5):
        _date_="Μάιος"
    else:
        _date_=date_[:3]

    #Specifed the index of website
    for jj in range(0,len(element_1)):
        if "Δείκτης Τιμών Καταναλωτή - Πληθωρισμός" in element_1[jj].text:
            if _date_ in element_1[jj].text:
                match = re.search(r'%\s*(\S+)', element_1[jj].text)
                if match:
                    percentage_value = match.group(1)
                    if percentage_value==_date_:
                        corrent_jj=jj

    #Identified the correct document for the current month
    anchors = element_1[int(corrent_jj)].find_all('a')
    hrefs = [a.get('href') for a in anchors]
    for href in hrefs:
        url_href=href
        

    #Main part of the documents
    url_months="https://www.cystat.gov.cy/el"+url_href
    bs = BeautifulSoup(url_months, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_soup = soup.find_all("a")
    for i in soup.find_all('a'):
        if i.find('span') and "Λήψη Αρχείου Word" in i.find('span').text:
            url = i['href']

    response = requests.get(url)
    if response.status_code == 200:
        with open('CyStat/'+str(current_month)+'.docx', 'wb') as file:
            file.write(response.content)

    doc = Document('CyStat/Consumer_Price_Index-'+str(current_month)+'.docx')
    doc_text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                doc_text += cell.text + "\t"
            doc_text += "\n"  

    pattern = r"Γενικός Δείκτης Τιμών Καταναλωτή\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})"
    match = re.search(pattern, doc_text)

    pattern1 = r"Τρόφιμα και μη Αλκοολούχα Ποτά\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})"
    match1 = re.search(pattern1, doc_text)

    if match:
        cpi_month = match.groups()
        cpi_month=float(cpi_month[1].replace(",","."))
        
        #identified the month CPI General
        online_per_['Date'] = pd.to_datetime(online_per_['Date'])
        date_to_find =last_results
        index = online_per_.index[online_per_['Date'] == date_to_find].tolist()
        values_12=float(online_per_.loc[index,"CPI General"])
        
        calcu_1= (cpi_month*100) /float(117.72)
        calcu_2= (values_12*100) /float(77.89)

        df_new_empty_ = pd.DataFrame()
        df_new_empty_.loc[0,"Period"]=str(_date_)+"-24"
        df_new_empty_.loc[0,"Official (2015=100)"]= float(cpi_month)
        df_new_empty_.loc[0,"Online (27/06/2024=77.89)"]=values_12
        df_new_empty_.loc[0,"Official (27/06/2024=100)"]=calcu_1
        df_new_empty_.loc[0,"Online (27/06/2024=100)"]=calcu_2
        
        df_tables = pd.concat([cystat_, df_new_empty_], ignore_index=True)
        df_tables.loc[len(df_tables)-1,"Official Inflation (%)"] = 100 * (df_tables.loc[len(df_tables)-1,"Official (27/06/2024=100)"] - df_tables.loc[len(df_tables)-2,"Official (27/06/2024=100)"]) / df_tables.loc[len(df_tables)-2,"Official (27/06/2024=100)"]
        df_tables.loc[len(df_tables)-1,"Online Inflation (%)"] = 100 * (df_tables.loc[len(df_tables)-1,"Online (27/06/2024=77.89)"] - df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"]) / df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"]
        df_tables.to_csv("CyStat/General_CPI_Offline_Vs_Online.csv",index=False)
        
    if match1:
        values_after_gd = match1.groups()
        #print(values_after_gd[1])
