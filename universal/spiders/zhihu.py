# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from universal.extractors import RegexLinkExtractor
from universal.items import SongItem


class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = [
        'https://www.zhihu.com/api/v4/members/Germey/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20']
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
        }
    }
    
    def __init__(self, *args, **kwargs):
        self.rules = [
            Rule(RegexLinkExtractor(restrict_re='"url_token": "(.*?)"',
                                    base_url='/api/v4/members/{0}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'),
                 callback='parse_item'),
            Rule(RegexLinkExtractor(restrict_re='"next": "(.*?)"', base_url='{0}'),
                 follow=True),
        ]
        super(ZhihuSpider, self).__init__(*args, **kwargs)
    
    def parse_item(self, response):
        print(response.text)
    
    def _requests_to_follow(self, response):
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)
