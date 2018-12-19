# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from ..items import PythonprojectItem
from ..connector_facade import *
from datetime import datetime

# # Current month only
current_dt = datetime.now()
current_time = str(current_dt)
month = datetime.now().strftime("%m")
# # Current month UTC timestamp defaults to first in month
today = datetime.today()
current_month_timestamp = str(datetime(today.year, today.month, 1))
# # Test UTC Timestamp
test_timestamp = '2018-09-01 00:00:00'


# find next website to crawl
next_allowed_domain = str(get_next_website(current_month_timestamp)[0].website)
next_start_url = 'https://'+str(get_next_website(current_month_timestamp)[0].start_url)

class AllcrawlerSpider(CrawlSpider):
    name = 'allcrawler'
    allowed_domains = [next_allowed_domain]
    start_urls = [next_start_url]
    rules = (Rule(LinkExtractor(allow=()), callback='parse_items',
                  follow=True),)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AllcrawlerSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        print("SPIDER OPENED")
        spider.logger.info('Spider opened: %s', spider.name)
        update_timestamp(month, "none", next_allowed_domain, current_time, current_time)

    def spider_closed(self, spider):
        responseFromSites = self.crawler.stats.get_value('downloader/response_count')
        spider.logger.info('Spider closed: %s', spider.name)
        update_timestamp(month, str(responseFromSites), next_allowed_domain, current_time, '0')

    def parse_items(self, response):
        item = PythonprojectItem()
        items = []
        # here we can parse our html document
        # we want to access our crawler entity table and loop through each snippet value to check if it exist in the html document
        for entity in bq_table():
            if entity.snippet_type == 'beregner' and entity.snippet_response_selector == 'css':
                if response.css(entity.snippet_value) or response.css('#'+entity.snippet_value):
                    print('found loan calculator '+str(entity.snippet_value))
                    response_data(next_allowed_domain, entity.snippet_name, response.url, current_time)

            elif entity.snippet_type == 'beregner' and entity.snippet_response_selector == 'xpath':
                pass

            elif entity.snippet_type == 'video' and entity.snippet_response_selector == 'xpath text':
                if response.xpath('//*[contains(text(), "' + str(entity.snippet_value) + '")]'):
                    print('found video snippet of'+str(entity.snippet_value)+' at '+response.url)
                    response_data(next_allowed_domain, entity.snippet_name, response.url, current_time)
