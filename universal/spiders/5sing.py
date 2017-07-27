# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from universal.items import SongItem


class SongSpider(CrawlSpider):
    name = '5sing'
    allowed_domains = ['5sing.kugou.com']
    start_urls = ['http://5sing.kugou.com/yc/list?t=1']
    
    def __init__(self, *args, **kwargs):
        self.rules = (
            Rule(LinkExtractor(allow='\/yc\/\d+\.html'), callback='parse_item'),
            Rule(LinkExtractor(restrict_xpaths='//li[@class="sec"]/a[contains(., "下一页")]')),
        )
        super(SongSpider, self).__init__(*args, **kwargs)

    
    def parse_item(self, response):
        song = SongItem()
        song['name'] = response.xpath('//div[@class="view_tit"]/h1/text()').extract_first()
        song['url'] = response.url
        yield song

    def _requests_to_follow(self, response):
        print('Response', response, type(response))
    
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            print(links)
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)
