# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IfengSpider(CrawlSpider):
    name = 'ifeng'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml']
    
    rules = (
        Rule(LinkExtractor(allow='listpage/.*/rtlist.shtml',
                           restrict_xpaths='//div[@class="m_page"]//a[contains(., "下一页")]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="newsList"]//a'), callback='parse_item'),
    )
    
    def parse_item(self, response):
        print(response.css('title::text').extract_first())
