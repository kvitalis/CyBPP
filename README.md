
# The Cyprus' Billion Prices Project

## Overview

The Cyprus 'Billion Prices Project' (https://thebillionpricesproject.com/) is inspired by an academic initiative at MIT and Harvard that uses prices collected from hundreds of online large retailers around the world on a daily basis to conduct research in macro and international economics. 

In particular, the Cyprus BPP involves web-scraping of prices of around 2200 goods and services from about 50 retailers in Cyprus on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) Inflation using standard methods. 

## Python Codes

### ScrapingCode (temporary name)

Since the main objective of this project is the collection and analysis of the online prices of representative products (goods and services) in the Cypriot market for Consumer Price Index (CPI) Inflation estimation, the 'ScrapingCode.py' file deals with the web scraping of the prices data and its storage. At the same time, emphasis is given on the products for which the data has not been collected for some reason.

This Python file is called daily from the workflow file 'RunDailyScraping.yml' around 09:00 (UTC Time) and it stores the scraped data of the products in the fixed/pre-selected and representative CPI basket into the 'raw_data.csv' file (temporary name). The storage is done in the form of a table and has the following order and structure: Date, Name, Price, Subclass, Division and Retailer.

### SecondIteration (temporary name)

As mentioned before, there is a need to collect the values from the first test. One of the main reasons why this is done with 100% accurated, is when the companies' websites is unavailable (either for maintenance reasons or due to traffic reasons). To address this specific issue, the price collection procedure is invoked a second time during the day at 15:00 (UTC time) only for the products for which the daily price was not collected in the preceding procedure. It is important to mention that the file that call this process is the file of SecondIteration.yml.

### Calculations (temporary name)

This file performs all the calculations needed for the construction of the General CPI and the estimation of CPI Inflation on a daily basis using standard methods in line with the Billion Prices Project. This Python file is called from the workflow file 'Calculations.yml' around 16:00 (UTC time) every day.

### Visualizations (tempory name)

In the above file, the fluctuations of inflation are presented graphically on a daily basis, along with the changes in CPI represented as a time series.All the output information storage as a image file on Datasets folder. File is called from the file Vizualization.yml (Tempory name), and the time is 18:00 (UTC Time).

## Retailers

In accordance with the statistical superiority of Cyprus and the representativeness of each retailer within various subclasses, presented below are the 52 selected retailers chosen for the development of the data collection code.

It is important to mention that there are retailers that are representative within the Cypriot market, but it was unexpected to collect data from their websites due to the following reasons: firstly, some retailers do not have websites; secondly, some have websites but possess robust IT knowledge and employ measures to block any attempt to scrape data from their websites.

1. Adventure Without Limits (AWOL) https://www.awol.com.cy/ 

2. Alter Vape https://altervape.eu/ 

3. Athlokinisi https://athlokinisi.com.cy/ 

4. Bwell Pharmacy https://bwell.com.cy/ 

5. Cablenet	https://cablenet.com.cy/

6. Centroptical https://centroptical-cyprus.com/

7. Costas Theodorou https://costastheodorou.com.cy/

8. Cyprus Energy Regulation Authority (CERA) https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf 

9. Cyprus Ministry of Education, Sport and Youth https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

10. Cyprus Post	https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf

11. Cyprus Public Transport https://www.publictransport.com.cy/

12. Cyprus Telecommunications Authority (CYTA)	https://www.cyta.com.cy/personal 

13. Electricity Authority of Cyprus (EAC) https://www.eac.com.cy/EN/Pages/default.aspx

14. Electroline	https://electroline.com.cy/ 

15. Epic https://www.epic.com.cy/en/page/start/home 

16. European University Cyprus	https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf

17. Evdokia Jewellery https://evdokiajewellery.com/

18. E-WHOLESALE	https://www.ewsale.com/tsigaro 

19. Famous Sports	https://www.famousports.com/en 

20. Flames Restaurant and Bar https://flamesrestaurantbar.com/
    
21. FuelDaddy (Agip, EKO, Eni, Esso, Fill n GO, Petrolina, Shell, Staroil, Total Plus)	https://www.fueldaddy.com.cy/en 

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

40. Sewerage Board of Limassol-Amathus (SBLA)	https://www.sbla.com.cy/Sewage-Charges 

41. Sewerage Board of Nicosia (SBN) https://www.sbn.org.cy/el/apoxeteftika-teli 

42. Sewerage and Drainage Board of Larnaca (LSDB) https://www.lsdb.org.cy/en/services/financial-information/sewage-charges/ 

43. Stephanis https://www.stephanis.com.cy/en 

44. SupermarketCy https://www.supermarketcy.com.cy/ 

45. The CYgar Shop https://www.thecygarshop.com/ 

46. The Royal Cigars https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos

47. Toyota https://www.toyota.com.cy/

48. Vassos Psarolimano https://www.tripadvisor.com.gr/Restaurant_Review-g262055-d1101684-Reviews-Vassos_Psarolimano-Ayia_Napa_Famagusta_District.html

49. Water Board of Nicosia (WBN) https://www.wbn.org.cy/%CE%BA%CE%B1%CF%84%CE%B1%CE%BD%CE%B1%CE%BB%CF%89%CF%84%CE%AE%CF%82/%CE%B4%CE%B9%CE%B1%CF%84%CE%B9%CE%BC%CE%AE%CF%83%CE%B5%CE%B9%CF%82/ 

50. Water Board of Larnaca (LWB) https://www.lwb.org.cy/en/charges-and-fees.html 

51. Water Board of Limassol (WBL) https://www.wbl.com.cy/el/water-rates 

52. Wolt (Costa Coffee, Starbucks, Caffè Nero, Pizza Hut, McDonald’s, Ocean Basket, KFC) https://wolt.com/en/cyp 

## GitHub Actions

The project utilizes GitHub Actions to automate the web data scraping and Index calculation processes. The repository contains the following YML files within the ./github/workflows directory:

### RunDailyScraping.yml: 
This workflow file schedules the execution of the 'ScrapingCode.py' script around 09:00 (UTC time) every day.
### SecondIteration.yml: 
....
### Calculations.yml: 
This workflow file schedules the execution of the 'Calculations.py' script around 16:00 (UTC time) every day.
### Visualizations.yml: 
This workflow file schedules the execution of the 'Visualizations.py' script around 16:45 (UTC time) every day.
