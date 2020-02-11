import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from immospider.spiders.immoscout import ImmoscoutSpider


process = CrawlerProcess(settings=get_project_settings())
URL = "https://www.immobilienscout24.de/Suche/de/nordrhein-westfalen/dortmund/wohnung-kaufen?price=-150000.0&enteredFrom=one_step_search"

process.crawl(ImmoscoutSpider,url=URL)
process.start()