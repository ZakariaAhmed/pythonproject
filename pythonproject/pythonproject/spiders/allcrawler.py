# -*- coding: utf-8 -*-
import scrapy


class AllcrawlerSpider(scrapy.Spider):
    name = 'allcrawler'
    allowed_domains = ['allcrawler.com']
    start_urls = ['http://allcrawler.com/']

    def parse(self, response):
        pass
