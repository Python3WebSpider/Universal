# -*- coding: utf-8 -*-
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from universal.items import *
from universal.utils import get_config


class UniversalSpider(CrawlSpider):
    name = 'universal'
    
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = eval(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        self.custom_settings = config.get('settings')
        super(UniversalSpider, self).__init__(*args, **kwargs)
    
    def parse_item(self, response):
        # 获取item配置
        item = self.config.get('item')
        if item:
            data = eval(item.get('class') + '()')
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                data[key] = response
                for process in value:
                    # 动态调用函数和属性
                    if process.get('method'):
                        data[key] = getattr(data[key], process.get('method'))(*process.get('args', []))
                    elif process.get('attr'):
                        data[key] = getattr(data[key], process.get('attr'))
            yield data
