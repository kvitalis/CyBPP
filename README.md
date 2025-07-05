# The Cyprus Billion Prices Project (CyBPP)

## Overview

The *Billion Prices Project* ([BPP](https://thebillionpricesproject.com/)) is an academic initiative at MIT and Harvard that uses prices collected from hundreds of online large retailers around the world on a daily basis to conduct research in macro and international economics. 

Here, the BPP methodology is for the first time in the Cypriot economy applied and involves web-scraping of prices of around 2200 goods and services from over 55 retailers in Cyprus on a daily basis. The scraped data is then used to calculate the *Consumer Price Index (CPI)* Inflation by using standard methods. 

## Python Codes

### 1. Web Scraping

The main objective of CyBPP is the calculation of the CPI Inflation using the online prices of products (goods and services) in a fixed/pre-selected and representative basket of Cypriot consumers. In doing so, the first step is the collection of the products' necessary data and its storage. The *WebScraping.py* file deals with the web scraping of this data. This Python file, which is called daily from the workflows file *WebScraping.yml* at around 08:00 (UTC time), firstly reads the *Products-Urls.csv* file (Datasets), then collects/scrapes the data available online, and finally stores it in the *Raw-Data.csv* file (Datasets); we note that for size reasons, we divide this full dataset file into quarterly subsets starting from 2024Q3 (27/06/2024 - 26/09/2024). The storage is done in a tabular form with the following order and structure: Date, Name, Price, Subclass, Division and Retailer. Some basic summary statistics of the reference/base CPI basket/dataset are presented in the *Descriptive-Statistics.docx* file.

At the same time, emphasis is given on the products for which the data has not been scraped for some reason. For instance, at the time of web-scraping the retailer's website is unavailable either for maintenance or traffic reasons. The info of these products is stored in the *Daily-Scraping-Errors.csv* file (Datasets) to be retrieved in a subsequent scraping process. 

### 2. Second Iteration 

As mentioned above, there is a need to retrieve the data of the products that was not scraped during the initial procedure. Hence, we run a second scraping iteration  through the *SecondIteration.py* file several hours after the first scraping. This Python file reads only the *Daily-Scraping-Errors.csv* file (Datasets), then it scrapes the available data and finaly stores it in the *Raw-Data.csv* file (Datasets). After the second iteration procedure, any data which remains unavailable is stored in the *Monthly-Scraping-Errors.csv* file (Datasets); this file is useful for the allocation of products that are no longer available (e.g. seasonal or out-of-stock products) and their replacement with the most similar available at the time. The *SecondIteration.py* file is called from the workflows file *SecondIteration.yml* at around 13:00 (UTC time) every day.

### 3. Calculations 

This Python file, which is called from the workflows file *Calculations.yml* around 14:00 (UTC time) every day, performs all the calculations needed for the construction of the General CPI and the estimation of CPI Inflation on a daily basis using standard methods in line with BPP. To do so, the *Calculations.py* file first reads the *Raw-Data.csv* file (Datasets), then performs the appropriate calculations using standard techniques as well as the *Weights-Cystat.csv* and *Reference-Values.csv* files (Datasets), and finally stores the results in the *Daily-CPI-Subclass-Division.csv*, *Daily-CPI-Division.csv*, and *Daily-CPI-General-Inflation.csv* files (Results), respectively.

### 4. Visualizations 

Finally, the *Visualizations.py* reads the *Daily-CPI-General-Inflation.csv* file and constructs the plots of the time evolution of General CPI and Inflation in Cyprus in PNG formats (Results). This Python file is called from the workflows file *Visualizations.yml* at around 15:00 (UTC time) every day.

## Online Retailers

According to the representativeness of each product and its retailer within the Cypriot market, presented below are the 56 selected online retailers chosen for the development of the Cyprus's CPI basket. It is important to mention that there are retailers which are representative within the Cypriot market, but it is infeasible to collect data on their products due to the following main reasons: (i) some retailers do not have websites, and (ii) some online retailers possess robust IT knowledge and employ measures to block any attempt to scrape data from their websites.

1. Adventure Without Limits (AWOL) https://www.awol.com.cy/ 

2. Alter Vape https://altervape.eu/ 

3. Athlokinisi https://athlokinisi.com.cy/ 

4. Bwell Pharmacy https://bwell.com.cy/ 

5. Cablenet	https://cablenet.com.cy/

6. Centroptical https://centroptical-cyprus.com/

7. Christos Grill & Seafood https://christosgrillandseafood.com/wp-content/uploads/2025/02/MENU-2025-night.pdf 

8. Costas Theodorou https://costastheodorou.com.cy/

9. Cyprus Energy Regulation Authority (CERA) https://www.cera.org.cy/el-gr/katanalotes/details/times-ilektrismou  

10. Cyprus Ministry of Education, Sport and Youth https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

11. Cyprus Post	https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf

12. Cyprus Public Transport https://www.publictransport.com.cy/

13. Cyprus Telecommunications Authority (CYTA)	https://www.cyta.com.cy/personal 

14. Electricity Authority of Cyprus (EAC) https://www.eac.com.cy/EL/regulatedactivities/supply/tariffs/Pages/supply-tariffs.aspx

15. Electroline	https://electroline.com.cy/ 

16. Epic https://www.epic.com.cy/en/page/start/home 

17. European University Cyprus	https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf

18. Evdokia Jewellery https://evdokiajewellery.com/

19. E-Wholesale https://www.ewsale.com/

20. Famous Sports https://www.famousports.com/en 

21. Flames Restaurant and Bar https://flamesrestaurantbar.com/
    
22. FuelDaddy (Agip, EKO, Eni, Esso, Fill n GO, Jackoson, Petrolina, Shell, Staroil, Total Plus) https://www.fueldaddy.com.cy/en through the Consumer Protection Service https://eforms.eservices.cyprus.gov.cy/MCIT/MCIT/PetroleumPrices

23. IKEA https://www.ikea.com.cy/

24. Intercity Buses https://intercity-buses.com/en/

25. Ithaki Garden https://www.tripadvisor.com.gr/Restaurant_Review-g190379-d7269566-Reviews-Ithaki_Garden-Larnaca_Larnaka_District.html

26. Lenses CY https://www.lensescy.com/

27. Leroy Merlin https://www.leroymerlin.com.cy/gr/  

28. Marks & Spencer	https://www.marksandspencer.com/cy/

29. Max 7 Taxi https://www.max7taxi.com/

30. MEZE Taverna Restaurant https://www.mezetaverna.com/
    
31. Moto Race https://www.motorace.com.cy/

32. Music Avenue https://www.musicavenue.com.cy/  

33. Nissan https://www.nissan.com.cy/ 

34. Novella Hair Mode https://novella.com.cy/ 

35. NUMBEO https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR

36. Pagkratios Traditional Tavern https://www.pagkratios.com/menu/

37. Parga Book Center https://www.parga.com.cy/

38. Piatsa Gourounaki https://piatsaexpress.com/menu/ 

39. Premier Laundry Services Ltd https://premierlaundry.com.cy/#/ 

40. Primetel https://primetel.com.cy/en

41. Pyxida Fish Tavern https://pyxidafishtavern.com/

42. Rio Cinemas http://www.riocinemas.com.cy/ 

43. Sewerage Board of Limassol-Amathus (SBLA) https://eoalemesos.org.cy/el/fees

44. Sewerage Board of Nicosia (SBN) https://ndlgo.org.cy/sewage/sewer-fees/ 

45. Sewerage and Drainage Board of Larnaca (LSDB) https://eoal.org.cy/exypiretisi/teli/apocheteftika-teli/

46. Stephanis https://www.stephanis.com.cy/en

47. Stock Center -- The Used Cars Experts https://www.stock-center.com.cy/ 

48. SupermarketCy https://www.supermarketcy.com.cy/ 

49. The CYgar Shop https://www.thecygarshop.com/ 

50. The Royal Cigars https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos

51. Toyota https://www.toyota.com.cy/

52. Vassos Psarolimano https://www.tripadvisor.com.gr/Restaurant_Review-g262055-d1101684-Reviews-Vassos_Psarolimano-Ayia_Napa_Famagusta_District.html

53. Water Board of Nicosia (WBN) https://ndlgo.org.cy/water-supply/consumer/pricing/ 

54. Water Board of Larnaca (LWB) https://eoal.org.cy/exypiretisi/teli/teli-chrisis-nerou/
    
55. Water Board of Limassol (WBL) https://eoalemesos.org.cy/el/fees 

56. Wolt (Costa Coffee, Starbucks, Caffè Nero, Pizza Hut, McDonald’s, Ocean Basket, KFC) https://wolt.com/en/cyp 

## GitHub Actions

The project utilizes GitHub Actions to automate the web data scraping and Index calculation processes. The repository contains the following YML files within the *.github/workflows* directory:

### 1. WebScraping.yml: 
This workflow file schedules the execution of the *WebScraping.py* script at around 08:00 (UTC time) every day.
### 2. SecondIteration.yml: 
This workflow file schedules the execution of the *SecondIteration.py* script at around 14:00 (UTC time) every day.
### 3. Calculations.yml: 
This workflow file schedules the execution of the *Calculations.py* script at around 15:00 (UTC time) every day.
### 4. Visualizations.yml: 
This workflow file schedules the execution of the *Visualizations.py* script at around 16:00 (UTC time) every day.

## Comparison with the Cyprus Statistical Service (CyStat)

The official/offline CPI Inflation measurement is conducted by the *Cyprus Statistical Service* ([CyStat](https://www.cystat.gov.cy/en/MethodologicalDetails?m=2090)). CyStat publishes the (offline) CPI data on the first Thursday of each month, reflecting the inflation rate for the preceding month. This regular release provides an official and comprehensive overview of price changes in the economy, which is crucial for understanding the cost of living and economic conditions in Cyprus.

CyStat collects the prices of goods and services only in urban districts of Nicosia, Larnaca, Limassol and Paphos. For each city, the fluctuations in the product prices each month, are weighted according to their population. Specifically, the weights for the four districts are: Nicosia 42%, Limassol 30%, Larnaca 18%, and Paphos 10%. 

The prices of 805 goods and services are recorded once every month, except for some seasonal products (e.g. vegetables and fruits), meat and fuels, whose prices are collected every week (every Thursday). From January 2016 and onwards, the CPI reference period (base year) is 2015.

The 'CyStat' folder includes all the necessary files for the results comparison between CyBPP and CyStat on a monthly basis. In particular, the *CyStat.py* file, which is called from the workflows file *CyStat.yml* on the first Thursday of each month, initially locates the CPI-Inflation report file in the CyStat's website (https://www.cystat.gov.cy/en/SubthemeStatistics?id=47), then collects the official/offline monthly data on the general/total and per division/category CPIs as presented in Table 1 of the report, and finally stores it along with the corresponding CyBPP online data in the *General-CPI-Offline-VS-Online.csv* and *Division-CPI-Offline-VS-Online.csv* files, respectively. In the *Official-vs-Online-General-CPI.png* and *Official-vs-Online-Inflation.png* files, we show the evolution of the monthly General CPI and Inflation of Cyprus, respectively, as estimated by CyBPP (online data) and CyStat (offline data). Since the two Indices have different reference/base periods, for comparability reasons we rebase them to have the value of 100 in 27/06/2024 and plot them in *Official-vs-Online-General-CPI-rebased.png* file.

*The following is not done yet: Similarly, we present the evolution of the offline and online monthly CPI per Division in the Division-CPI-Offline-VS-Online.png file.* 
