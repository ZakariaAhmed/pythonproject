# pythonproject

Project Description: Web scraping, Crawling automated with Python - Implentation Stats,

Problem: Company X have many banks as customers, Company x wants to find out, how many of their customers
have implemented loan calculators and or videos on their websites, and they want to monitor once a month, to see how it progresses

We want to build an automated crawler and scraper, that looks for values in different websites.

We will implement 3 databases in Google's Big Query
1. A list of databases to crawl.
2. A list of values to look for on each website we crawl
3. Response table where we insert what we found and where.


Last but not least we will implement graphs etc. on Google DataStudio, so that company x can monitor through Google DataStudio chart we will share with them.

requirements:
Connecting to Google Cloud Platform

Authenticated with service account key


Dependent Libraries: scrapy, google.cloud

to crawl navigate to pythonproject/pythonproject and cmd. scrapy crawl allcrawler 
you need to configure google authentication at connector_facade.py,
and create 3 datatables in big query


How final project look like 

The list of websites we are crawling and updating on each finished job, what time it was crawled,
how many sites on the page we crawled etc.
![List of Websites We going to crawl](https://github.com/ZakariaAhmed/pythonproject/blob/master/UpdatesWebsiteTableOnCrawl.png)

The values we are looking for on each html document
![alt text](https://github.com/ZakariaAhmed/pythonproject/blob/master/ValuesWeAreLookingFor.png)

what we collected so far on our crawl, as you can see the snippetValue that was collected and where it was found.
![alt text](https://github.com/ZakariaAhmed/pythonproject/blob/master/ValuesWeAreLookingFor.png)


