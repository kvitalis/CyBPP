#Important libraries
import pandas as pd 
import re
import requests
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from docx import Document
from babel.dates import format_date
from datetime import date, timedelta , datetime

#Important function
def cystat(last_results):
    
    #Read important files
    general_cpi=pd.read_csv("CyStat/General-CPI-Offline-VS-Online.csv")
    monthly_gen_cpi=pd.read_csv("Results/Monthly-CPI-General-Inflation.csv")
   
    #Main part of the web scraping 
    url_new="https://www.cystat.gov.cy/el/SubthemeStatistics?id=47"
    bs = BeautifulSoup(url_new, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_1=soup.find_all("div",{"class":"col-12 col-md-12 col-lg-6 col-xl-6"})
    
    #Calculation of the month
    current_date = datetime.now()
    current_date = current_date.strftime("%Y-%m-%d")
    if isinstance(current_date, str):
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
    correction_day = current_date - timedelta(days=7)
    
    current_month =correction_day.month
    current_year = correction_day.year
    current_day = correction_day.day
    
    date = datetime(current_year, current_month,current_day)
    date_=format_date(date, 'MMMM', locale='el')

    #Fix the month
    if (current_month==6) or (current_month==7):
        _date_=date_[:4]
    elif (current_month==5):
        _date_="Μάιος"
    else:
        _date_=date_[:3]
   
    #Specify the index of website
    for jj in range(0,len(element_1)):
        if "Δείκτης Τιμών Καταναλωτή - Πληθωρισμός" in element_1[jj].text:
            if _date_ in element_1[jj].text:
                match = re.search(r'%\s*(\S+)', element_1[jj].text)
                if match:
                    percentage_value = match.group(1)
                    if percentage_value==_date_:
                        corrent_jj=jj

    #Identify the correct document for the current month
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
        with open('CyStat/Consumer_Price_Index-'+str(current_month)+'.docx', 'wb') as file:
            print("Yes/Ok")
            file.write(response.content)
    
    doc = Document('CyStat/Consumer_Price_Index-'+str(current_month)+'.docx')
    doc_text = ""
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                doc_text += cell.text + "\t"
            doc_text += "\n"  
    print(doc_text)
    pattern = r"Γενικός Δείκτης Τιμών Καταναλωτή\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})"
    match = re.search(pattern, doc_text)

    if match:
        cpi_month = match.groups()
        cpi_month=float(cpi_month[1].replace(",","."))
        cpi_month = round(cpi_month, 2)
        
        #identified the month CPI General
        monthly_gen_cpi['Date'] = pd.to_datetime(monthly_gen_cpi['Date'])
        date_to_find = last_results
        index = monthly_gen_cpi.index[monthly_gen_cpi['Date'] == date_to_find].tolist()
        values_12 = float(monthly_gen_cpi.loc[index,"CPI General"])
        values_12 = round(values_12, 2)
        
        #rebase the General CPI
        rebase_offline = (cpi_month*100) / float(117.72)
        rebase_online = (values_12*100) / float(77.89)

        df_new_empty_ = pd.DataFrame()
        
        correction_day = current_date - timedelta(days=7)
        
        df_new_empty_.loc[0,"Period"] = correction_day.strftime("%Y-%m")
        df_new_empty_.loc[0,"Official (2015=100)"]= round(float(cpi_month),2)
        df_new_empty_.loc[0,"Online (27/06/2024=77.89)"] = values_12
        df_new_empty_.loc[0,"Official (27/06/2024=100)"] = round(rebase_offline,2)
        df_new_empty_.loc[0,"Online (27/06/2024=100)"] = round(rebase_online,2)
        df_new_empty_.loc[0,"Official Inflation (%)"] = None
        df_new_empty_.loc[0,"Online Inflation (%)"] = None
        
        df_tables = pd.concat([general_cpi, df_new_empty_], ignore_index=True)
        df_tables.loc[len(df_tables)-1,"Official Inflation (%)"] = round(100 * (df_tables.loc[len(df_tables)-1,"Official (2015=100)"] - df_tables.loc[len(df_tables)-2,"Official (2015=100)"]) / df_tables.loc[len(df_tables)-2,"Official (2015=100)"],2)
        df_tables.loc[len(df_tables)-1,"Online Inflation (%)"] = round(100 * (df_tables.loc[len(df_tables)-1,"Online (27/06/2024=77.89)"] - df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"]) / df_tables.loc[len(df_tables)-2,"Online (27/06/2024=77.89)"],2)
        df_tables.to_csv("CyStat/General-CPI-Offline-VS-Online.csv",index=False)

    #Offline/Official CPI per Division
    
    division_cpi = pd.read_csv("CyStat/Division-CPI-Offline-VS-Online.csv")
    
    pattern_list=[r"Τρόφιμα και μη Αλκοολούχα Ποτά\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Αλκοολούχα Ποτά και Καπνός\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Ένδυση και Υπόδηση\s+([\d,]+)\s+([\d,]+)",
                  r"Στέγαση, Ύδρευση, Ηλεκτρισμός και Υγραέριο\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Επίπλωση, Οικιακός Εξοπλισμός και Προΐόντα Καθαρισμού\s+([\d,]+)\s+([\d,]+)",
                  r"Υγεία\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Μεταφορές\s+(\d+,\d+)\s+(\d+,\d+)",
                  r"Επικοινωνίες\s+([\d,]+)\s+([\d,]+)",
                  r"Αναψυχή και Πολιτισμός\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Εκπαίδευση\s+(\d+,\d+)\s+(\d+,\d+)",
                  r"Εστιατόρια και Ξενοδοχεία\s+(\d{3},\d{2})\s+(\d{3},\d{2})\s+(\d{1},\d{2})\s+([-]?\d{1},\d{2})\s+(\d{1},\d{2})",
                  r"Άλλα Αγαθά και Υπηρεσίες\s+([\d,]+)\s+([\d,]+)"
    ]
    
    division_name=["FOOD AND NON-ALCOHOLIC BEVERAGES",
                   "ALCOHOLIC BEVERAGES AND TOBACCO",
                   "CLOTHING AND FOOTWEAR",
                   "HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS",
                   "FURNISHING, HOUSEHOLD EQUIPMENT AND SUPPLIES",
                   "HEALTH",
                   "TRANSPORT",
                   "COMMUNICATION",
                   "RECREATION AND CULTURE",
                   "EDUCATION",
                   "RESTAURANTS AND HOTELS",
                   "MISCELLANEOUS GOODS AND SERVICES"   
    ]
    
    for i in range(0,len(pattern_list)):
        match_ = re.search(pattern_list[i], doc_text)
        if (i!=4 or i!=7): 
            if match_:
                values_after_gd = match_.groups()
                division_=values_after_gd[1].replace(",",".")
        else:
            if match_:
                values_after_gd = match_.groups(2)
                division_=values_after_gd[1].replace(",",".")
         
        new_row = []
        correction_day = current_date - timedelta(days=7)
        new_row.append(correction_day.strftime("%Y-%m"))
        new_row.append(division_name[i])
        new_row.append(float(division_))
        new_row.append(None)
        new_row.append(None)
        new_row.append(None)
        division_cpi.loc[len(division_cpi)] = new_row
    
    prior_df = division_cpi[len(division_cpi)-24:len(division_cpi)-12]
    current_df = division_cpi[len(division_cpi)-12:len(division_cpi)]
    unique_divisions = division_cpi['Division'].unique()
        
    for unique_ in unique_divisions: 
        df_1 = float(prior_df[prior_df["Division"] == unique_]["Official CPI"])
        df_2 = float(current_df[current_df["Division"] == unique_]["Official CPI"])
        official_change = ((df_2 - df_1)/df_1) * 100  #change (%) of CPI per Division 
    
        index_list = current_df[current_df["Division"]==unique_]["Official CPI"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        division_cpi.loc[float_index_list, "Official Monthly Change (%)"] = round(official_change,2)
    
    #Online CPI per Division
    daily_cpi_online=pd.read_csv("Results/Daily-CPI-Division.csv")
    daily_cpi_online=daily_cpi_online[daily_cpi_online["Date"]==correction_day.strftime("%Y-%m-%d")]

    unique_values=daily_cpi_online["Division"].unique()
    for i in range(0,len(unique_values)):
        indices=division_cpi[division_cpi["Division"]==unique_values[i].strip()].index
        values_1234=daily_cpi_online[daily_cpi_online["Division"]==unique_values[i]]["CPI Division"]
        print(values_1234.values[0])
        division_cpi.loc[indices[-1],"Online CPI"]=values_1234.values[0]

    prior_df = division_cpi[len(division_cpi)-24:len(division_cpi)-12]
    current_df = division_cpi[len(division_cpi)-12:len(division_cpi)]
    unique_divisions = division_cpi['Division'].unique()

    for unique_ in unique_divisions: 
        df_3 = float(prior_df[prior_df["Division"] == unique_]["Online CPI"])
        df_4 = float(current_df[current_df["Division"] == unique_]["Online CPI"])
        online_change = ( (df_4 - df_3) / df_3 ) * 100  #change (%) of CPI per Division 

        index_list = current_df[current_df["Division"]==unique_]["Online CPI"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        division_cpi.loc[float_index_list, "Online Monthly Change (%)"] = round(online_change,2)

    division_cpi.to_csv("CyStat/Division-CPI-Offline-VS-Online.csv",index=False)

    #Construct the plots
    cystat_gen_cpi=pd.read_csv("CyStat/General-CPI-Offline-VS-Online.csv")

    #Plot: Official vs Online General CPI
    plt.figure(figsize=(12, 6))
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Official (2015=100)'], label='Official (2015=100)', marker='o', color='red')
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Online (27/06/2024=77.89)'], label='Online (27/06/2024=77.89)', marker='o', color='blue')
    plt.xlabel('Period')
    plt.ylabel('General CPI')
    plt.title('Official vs Online General CPI')
    plt.legend()
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.savefig('CyStat/Official-vs-Online-General-CPI.png')
    plt.show()
    
    #Plot: Official vs Online General CPI (rebased)
    plt.figure(figsize=(12, 6))
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Official (27/06/2024=100)'], label='Official', marker='o', color='red')
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Online (27/06/2024=100)'], label='Online', marker='o', color='blue')
    plt.xlabel('Period')
    plt.ylabel('General CPI (27/06/2024=100)')
    plt.title('Official vs Online General CPI (rebased)')
    plt.legend()
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.savefig('CyStat/Official-vs-Online-General-CPI-rebased.png')
    plt.show()
    
    #Plot: Official vs Online Inflation
    plt.figure(figsize=(12, 6))
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Official Inflation (%)'], label='Official/Offline', marker='o', color='red')
    plt.plot(cystat_gen_cpi['Period'], cystat_gen_cpi['Online Inflation (%)'], label='Online', marker='o', color='blue')
    plt.xlabel('Period')
    plt.ylabel('Inflation (%)')
    plt.title('Official vs Online Inflation')
    plt.legend()
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.savefig('CyStat/Official-vs-Online-Inflation.png')
    plt.show()

def is_first_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date - timedelta(days=7)).month:
        last_results = date - timedelta(days=7)
        last_results = last_results.strftime("%Y-%m-%d")
        cystat(last_results)
    else:
        print("TODAY IS NOT THE FIRST THURSDAY OF THE MONTH")

#Call the function
current_date = datetime.now().strftime("%Y-%m-%d")
is_first_thursday(current_date)    
