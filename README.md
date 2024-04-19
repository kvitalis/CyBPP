
# Billion Prices Cyprus Scrape Project

## Overview

The Billion Prices Cyprus Scrape project involves scraping prices of around 2300 products from 50 retailers on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) against a reference basket.

## Scraping Code(temporary name)

The main objective of this project is to collect and analyze the prices of the Cypriot market in various qualities. The specific Python file has been acquired for the collection process of these prices and their storage. At the same time, emphasis is placed on the products for which the prices have not been collected for some reason.

The above file do you call daily from the file RunDailyScraping.yml at 09:00 (UTC Time) and is storaged the prices to the raw_data.csv file (temporary name). The storage is done in the form of a table and has the following order and structural variables: Date,Product Name, Product Price, Subclass, Division and Retailers.

## SecondIteration (temporary name)

As mentioned before, there is a need to collect the values from the first test. One of the main reasons why this is done with 100% accurated, is when the companies' websites is unavailable (either for maintenance reasons or due to traffic reasons). To address this specific issue, the price collection procedure is invoked a second time during the day at 15:00 (UTC Time) only for the products for which the daily price was not collected in the preceding procedure. It is important to mention that the file that call this process is the file of SecondIteration.yml.

## Calculation (temporary name)

The existence of the particular file is just as important because it calculates the CPI as well as the daily inflation. These calculations are made exactly as guided by the OneMillionPriceProject. This file is called from the file Calculation.yml, and the time is 16:00 (UTC Time).

## Visualizations (tempory name)

In the above file, the fluctuations of inflation are presented graphically on a daily basis, along with the changes in CPI represented as a time series.All the output information storage as a image file on Datasets folder. File is called from the file Vizualization.yml (Tempory name), and the time is 18:00 (UTC Time).

## Retailers:

In accordance with the statistical superiority of Cyprus and the representativeness of each retailer within various subclasses, presented below are the 52 selected retailers chosen for the development of the data collection code.

It is important to mention that there are retailers that are representative within the Cypriot market, but it was unexpected to collect data from their websites due to the following reasons: firstly, some retailers do not have websites; secondly, some have websites but possess robust IT knowledge and employ measures to block any attempt to scrape data from their websites.

- Adventure Without Limits (AWOL)	https://www.awol.com.cy/ 

- Alphamega	https://www.alphamega.com.cy/ 

- Alter Vape	https://altervape.eu/ 

- Athlokinisi	https://athlokinisi.com.cy/ 

- Bwell Pharmacy	https://bwell.com.cy/ 

- Cablenet	https://cablenet.com.cy/ 

- Consumer Protection Service	https://consumer.gov.cy/gr/ 

- Cyprus Energy Regulation Authority (CERA)	https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf 

- Cyprus Ministry of Education, Sport and Youth	https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

- Cyprus Post	https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf 

- Cyprus Telecommunications Authority (CYTA)	https://www.cyta.com.cy/personal 

- Epic	https://www.epic.com.cy/en/page/start/home 

- E-WHOLESALE	https://www.ewsale.com/tsigaro 

- Electroline	https://electroline.com.cy/ 

- European University Cyprus	https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf 

- Famous Sports	https://www.famousports.com/en 

- FuelDaddy (Agip, EKO, Eni, Esso, Fill n GO, Petrolina, Shell, Staroil, Total Plus)	https://www.fueldaddy.com.cy/en 

- IKEA	https://www.ikea.com.cy/

- Marks & Spencer	https://www.marksandspencer.com/cy/ 

- Mazda	https://www.mazda.com.cy/home 

- Moto Race	https://www.motorace.com.cy/ 

- Nissan	https://www.nissan.com.cy/ 

- Novella Hair Salon	https://novella.com.cy/ 

- NUMBEO	https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR 

- Pizza Hut	https://www.pizzahut.com.cy/ 

- Primetel	https://primetel.com.cy/en 

- Rio Cinemas	http://www.riocinemas.com.cy/ 

- Sewerage Board of Limassol-Amathus (SBLA)	https://www.sbla.com.cy/Sewage-Charges 

- Sewerage Board of Nicosia (SBN)	https://www.sbn.org.cy/el/apoxeteftika-teli 

- Sewerage and Drainage Board of Larnaca (LSDB)	https://www.lsdb.org.cy/en/services/financial-information/sewage-charges/ 

- Stephanis	https://www.stephanis.com.cy/en 

- Stradivarius	https://www.stradivarius.com/cy/ 

- SupermarketCy	https://www.supermarketcy.com.cy/ 

- The CYgar Shop	https://www.thecygarshop.com/ 

- The Royal Cigars 	https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos 

- Water Board of Nicosia (WBN)	https://www.wbn.org.cy/%CE%BA%CE%B1%CF%84%CE%B1%CE%BD%CE%B1%CE%BB%CF%89%CF%84%CE%AE%CF%82/%CE%B4%CE%B9%CE%B1%CF%84%CE%B9%CE%BC%CE%AE%CF%83%CE%B5%CE%B9%CF%82/ 

- Water Board of Larnaca (LWB)	https://www.lwb.org.cy/en/charges-and-fees.html 

- Water Board of Limassol (WBL)	https://www.wbl.com.cy/el/water-rates 

- Wolt (Costa Coffee, Piatsa Gourounaki Nicosia, Pixida Nicosia, Kofini Tavern Limassol, Vlachos Taverna Larnaca, Zakos Beach Restaurant Larnaca, Paphos Tavernaki, Ocean Basket Paphos, McDonald’s)	https://wolt.com/en/cyp 

 
## GitHub Actions

The project utilizes GitHub Actions to automate the scraping process. The repository contains the following YAML files within the ./github/workflows directory:

### run-daily-scrape.yml: 
This file schedules the execution of scrape_tool.py and calculations.py scripts on a daily basis.
### initialise-clear-csv.yml: 
Whenever a pull request is made targeting the initialise or initialize branch, this file runs initial.py to reset the BillionPricesProject_ProductList.csv file.
### initialise_clear_calculations.yml: 
Whenever a pull request is made targeting the initialise_c or initialize_c branch, this file runs initialise_calculations.py to reset the Calculations.csv file.

