# ImmoRentPred
Immobilienscout24 Scrapy Machine Learning Predictor for Rent in Germany

# Requirenments
Only Python 3.6
scrapy==1.8.0
requests==2019.4.13
googlemaps

# Description
Fast running scraper which get data only from the search site.

# Run
The program can simply be executed with "runner.py". The URL can be inputted as string. All the data behind this URL will be scrapped. The URL should contain the needed filter criteria. Please go to www.immobilienscout24.de to get the search link.

# Saving of Data
The scraped data will be saved into a SQLite Database "real-estate.db".

# Thanks to
Initial development was copied from https://github.com/asmaier/ImmoSpider