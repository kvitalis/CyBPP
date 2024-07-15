
# The Cyprus' Billion Prices Project

## Overview

The 'Billion Prices Project - BPP' (https://thebillionpricesproject.com/) is an academic initiative at MIT and Harvard that uses prices collected from hundreds of online large retailers around the world on a daily basis to conduct research in macro and international economics. 

Here, the BPP methodology is for the first time in the Cypriot economy applied and involves web-scraping of prices of around 2200 goods and services from over 50 retailers in Cyprus on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) Inflation by using standard methods. 

## Python Codes

### 1. Web Scraping

Since the main objective of this project is the calculation of the Consumer Price Index (CPI) Inflation using the online prices of products (goods and services) in the fixed/pre-selected and representative CPI basket, the first step is the collection of the products' data and its storage. The 'WebScraping.py' file deals with the web scraping of this data. This Python file, which is called daily from the workflows file 'WebScraping.yml' at around 09:00 (UTC time), firstly reads the 'ProductsUrls.csv' file (Datasets), then collects the data available online, and finally stores it in the 'raw_data.csv' file (Datasets). The storage is done in the form of a table and has the following order and structure: Date, Name, Price, Subclass, Division and Retailer.

At the same time, emphasis is given on the products for which the data has not been scraped for some reason, e.g. at the time of web-scraping a retailer's website is unavailable either for maintenance reasons or due to traffic reasons. The data of these products are stored in the 'DailyScrapingErrors.csv' file (Datasets) to be retrieved in a subsequent scraping process. 

### 2. Second Iteration 

As mentioned above, there is a need to retrieve the data of the products that was not scraped during the initial procedure. Hence, we run a second scraping iteration  through the 'SecondIteration.py' file about 6 hours after the first scraping. This Python file reads only the 'DailyScrapingErrors.csv' file (Datasets), then it scrapes the available data and finaly stores it in the 'raw_data.csv' file (Datasets). After the second iteration procedure, any data which remains unavailable is stored in the 'MonthlyScrapingErrors.csv' file (Datasets). The 'SecondIteration.py' file is called from the workflows file 'SecondIteration.yml' at around 15:00 (UTC time) every day.

### 3. Calculations 

This Python file, which is called from the workflows file 'Calculations.yml' around 16:00 (UTC time) every day, performs all the calculations needed for the construction of the General CPI and the estimation of CPI Inflation on a daily basis using standard methods in line with the Billion Prices Project. To do so, the 'Calculations.py' file first reads the 'raw_data.csv' file (Datasets), then performs the appropriate calculations using standard techniques and the 'Weights_Cystat.csv' and 'Reference_Values.csv' files (Datasets), and finally stores the results in the 'CPI-Subclass-Division.csv', 'CPI-Division.csv', and 'CPI-General-Inflation.csv' files (Results).

### 4. Visualizations 

Finally, the 'Visualizations.py' reads the 'CPI-General-Inflation.csv' file and constructs the plots of the time evolution of General CPI and Inflation in Cyprus in png formats (Results). This Python file is called from the workflows file 'Visualizations.yml' at around 17:00 (UTC time) every day.

## Online Retailers

According to the representativeness of each product and its retailer within the Cypriot market, presented below are the 53 selected online retailers chosen for the development of the Cyprus CPI basket. It is important to mention that there are retailers which are representative within the Cypriot market, but it is unexpected to collect data from their websites due to the following main reasons: (i) some retailers do not have websites, and (ii) some have websites but possess robust IT knowledge and employ measures to block any attempt to scrape data from their websites.

1. Adventure Without Limits (AWOL) https://www.awol.com.cy/ 

2. Alter Vape https://altervape.eu/ 

3. Athlokinisi https://athlokinisi.com.cy/ 

4. Bwell Pharmacy https://bwell.com.cy/ 

5. Cablenet	https://cablenet.com.cy/

6. Centroptical https://centroptical-cyprus.com/

7. Costas Theodorou https://costastheodorou.com.cy/

8. Cyprus Energy Regulation Authority (CERA) https://www.cera.org.cy/el-gr/katanalotes  

9. Cyprus Ministry of Education, Sport and Youth https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

10. Cyprus Post	https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf

11. Cyprus Public Transport https://www.publictransport.com.cy/

12. Cyprus Telecommunications Authority (CYTA)	https://www.cyta.com.cy/personal 

13. Electricity Authority of Cyprus (EAC) https://www.eac.com.cy/EL/regulatedactivities/supply/tariffs/Pages/supply-tariffs.aspx

14. Electroline	https://electroline.com.cy/ 

15. Epic https://www.epic.com.cy/en/page/start/home 

16. European University Cyprus	https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf

17. Evdokia Jewellery https://evdokiajewellery.com/

18. E-Wholesale https://www.ewsale.com/

19. Famous Sports https://www.famousports.com/en 

20. Flames Restaurant and Bar https://flamesrestaurantbar.com/
    
21. FuelDaddy (Agip, EKO, Eni, Esso, Fill n GO, Jackoson, Petrolina, Shell, Staroil, Total Plus)	https://www.fueldaddy.com.cy/en 

22. IKEA https://www.ikea.com.cy/

23. Intercity Buses https://intercity-buses.com/en/

24. Ithaki Garden https://www.tripadvisor.com.gr/Restaurant_Review-g190379-d7269566-Reviews-Ithaki_Garden-Larnaca_Larnaka_District.html

25. Lenses CY https://www.lensescy.com/

26. Leroy Merlin https://www.leroymerlin.com.cy/gr/  

27. Marks & Spencer	https://www.marksandspencer.com/cy/

28. Max 7 Taxi https://www.max7taxi.com/

29. MEZE Taverna Restaurant https://www.mezetaverna.com/
    
30. Moto Race https://www.motorace.com.cy/

31. Music Avenue https://www.musicavenue.com.cy/  

32. Nissan https://www.nissan.com.cy/ 

33. Novella Hair Mode https://novella.com.cy/ 

34. NUMBEO https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR

35. Parga Book Center https://www.parga.com.cy/

36. Premier Laundry Services Ltd https://premierlaundry.com.cy/#/ 

37. Primetel https://primetel.com.cy/en

38. Pyxida Fish Tavern https://pyxidafishtavern.com/

39. Rio Cinemas http://www.riocinemas.com.cy/ 

40. Sewerage Board of Limassol-Amathus (SBLA) https://eoalemesos.org.cy/el/fees

41. Sewerage Board of Nicosia (SBN) https://www.sbn.org.cy/el/apoxeteftika-teli 

42. Sewerage and Drainage Board of Larnaca (LSDB) https://eoal.org.cy/exypiretisi/teli/teli-chrisis-nerou/  

43. Stephanis https://www.stephanis.com.cy/en

44. Stock Center -- The Used Cars Experts https://www.stock-center.com.cy/ 

45. SupermarketCy https://www.supermarketcy.com.cy/ 

46. The CYgar Shop https://www.thecygarshop.com/ 

47. The Royal Cigars https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos

48. Toyota https://www.toyota.com.cy/

49. Vassos Psarolimano https://www.tripadvisor.com.gr/Restaurant_Review-g262055-d1101684-Reviews-Vassos_Psarolimano-Ayia_Napa_Famagusta_District.html

50. Water Board of Nicosia (WBN) https://www.wbn.org.cy/%CE%BA%CE%B1%CF%84%CE%B1%CE%BD%CE%B1%CE%BB%CF%89%CF%84%CE%AE%CF%82/%CE%B4%CE%B9%CE%B1%CF%84%CE%B9%CE%BC%CE%AE%CF%83%CE%B5%CE%B9%CF%82/ 

51. Water Board of Larnaca (LWB) https://www.lwb.org.cy/en/charges-and-fees.html 

52. Water Board of Limassol (WBL) https://www.wbl.com.cy/el/water-rates 

53. Wolt (Costa Coffee, Starbucks, Caffè Nero, Pizza Hut, McDonald’s, Ocean Basket, KFC) https://wolt.com/en/cyp 

## GitHub Actions

The project utilizes GitHub Actions to automate the web data scraping and Index calculation processes. The repository contains the following YML files within the ./github/workflows directory:

### 1. WebScraping.yml: 
This workflow file schedules the execution of the 'WebScraping.py' script at around 09:00 (UTC time) every day.
### 2. SecondIteration.yml: 
This workflow file schedules the execution of the 'SecondIteration.py' script at around 15:00 (UTC time) every day.
### 3. Calculations.yml: 
This workflow file schedules the execution of the 'Calculations.py' script at around 16:00 (UTC time) every day.
### 4. Visualizations.yml: 
This workflow file schedules the execution of the 'Visualizations.py' script at around 17:00 (UTC time) every day.
