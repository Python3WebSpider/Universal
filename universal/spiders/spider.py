#
# import logging
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# from scrapy.spiders import Spider, CrawlSpider, \
#     XMLFeedSpider, CSVFeedSpider, SitemapSpider
# from scrapy import signals
# from scrapy.http import HtmlResponse
# from scrapy import Request
# from scrapy_splash import SplashRequest
# from scrapy_splash.response import SplashTextResponse
# from common.public import *
# from DLQYSpider2.cleaner import cleaner_decorator
# from statistics.sender import data_sender
# from statistics.receiver import data_receiver
# logging.basicConfig()
#
#
# # 原始数据模板
# template = {
#         'url': '',
#         'text': '',
#         'encoding': '',
#         'xpath': {}
# }
#
#
# def source_data_package(response, xpath):
#     '''组装原始数据
#     :param response:响应体
#     :param xpath:分析解析规则
#     :return:字典
#     '''
#     template['url'] = response.url
#     template['text'] = response.text
#     template['encoding'] = response.encoding
#     template['xpath'] = xpath
#     return template
#
#
# class Task(object):
#     '''用于任务映射'''
#     def __init__(self):
#         self.spider_name = ''           # scrapy爬虫名字
#         self.spider_crawl_name = ''     # 区分名字，用于区分cookies
#         self.spider_count = 1           # 同一任务同时采集的爬虫个数
#         self.key_search = False         # 是否搜索引擎或论坛
#         self.java_script = False        # 是否JavaScript渲染response
#         self.ajax = False               # 是否ajax网页
#         self.type = ''                  # 任务类型
#         self.id = ''                    # 任务ID
#         self.delay = 0                  # 采集延迟
#         self.depth_limit = 0            # 采集深度
#         self.retry = 0                  # 重试次数
#         self.url = ''                   # url信源（未使用）
#         self.headers = {}               # 请求头
#         # self.params = {}
#         self.note = ''                  # 是否记录到数据库
#         self.proxy = False              # 是否使用代理
#         self.page = {}                  # 翻页规则
#         self.xpath = {}                 # 采集规则
#
#
# class SingleSpider(Spider):
#     '''最简单的一级爬虫'''
#     name = 'single_spider'
#     sender = {'current_url': '', 'url': '', 'floor': 0, 'type': ''}
#
#     def __init__(self, init, pipe, *args, **kw):
#         task = Task()
#         [setattr(task, k, v) for k, v in init.items()]
#         self.name = task.spider_crawl_name
#         self.task = task
#         self.pipe = pipe
#         self.source_task = init
#         self.allowed_domains = task.page.get('allowed_domains')
#         self.start_urls = task.page.get('start_urls')
#         self.pages = task.page.get('pages')
#         self.download_delay = task.delay
#         self.floor = 0
#         self.db_floor = 0
#         self.note = getattr(self.task, 'note', '')
#         super().__init__(self.name, *args, **kw)
#
#     def start_requests(self):
#         '''初始化请求选择
#         :return: Request/SplashRequest对象
#         '''
#         tmp = []
#         for url in self.start_urls:
#             if self.note:
#                 last_page = data_receiver(url)
#                 if last_page:
#                     # 数据库中存储的当前url信息
#                     url = last_page['url']
#                     self.db_floor = last_page['floor']
#                     tmp.append(url)
#         if tmp:
#             self.start_urls.clear()
#             self.start_urls.extend(tmp)
#         yield from [SplashRequest(url, dont_filter=True, meta={'spider_name': self.name}) if
#                     self.task.java_script else Request(url, dont_filter=True, meta={'spider_name': self.name})
#                     for url in self.start_urls]
#
#     def parse(self, response):
#         '''
#         :param response:响应体
#         :return: Request/SplashRequest对象
#         '''
#         self.pipe.send(source_data_package(response, self.source_task['xpath']))
#         item = {}
#         if self.task.key_search:
#             # xpath结果匹配，搜索引擎和论坛适用
#             max_num = self.task.xpath['max_num']
#             for i in range(1, max_num + 1):
#                 for k, v in self.task.xpath.items():
#                     if 'max_num' == k:
#                         continue
#                     item[k] = get_data_by_xpath(response, [j.format(i) for j in v['xpath']])
#                 # item的value都为空时舍弃
#                 if not [i for i in item.values() if i]:
#                     continue
#                 item['url'] = self.task.url
#                 item['current_url'] = response.url
#                 if self.note:
#                     # 每个item都要统计到server
#                     item['db_floor'] = self.db_floor
#                     self.note_to_server(self.task.url, response.url, item)
#                 yield item
#                 item.clear()
#         else:
#             for k, v in self.task.xpath.items():
#                 item[k] = get_data_by_xpath(response, v['xpath'])
#             item['url'] = response.url
#             yield item
#
#         url = get_data_by_xpath(response, self.pages.get('next'))
#         if url:
#             url = urljoin(response.url, self.clean_normal(url))
#             yield SplashRequest(url, dont_filter=True, meta={'spider_name': self.name}) if \
#                 self.task.java_script else Request(url, dont_filter=True, meta={'spider_name': self.name})
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         '''绑定爬虫的关闭信号
#         :param crawler:
#         :param args:
#         :param kwargs:
#         :return: None
#         '''
#         spider = super(SingleSpider, cls).from_crawler(crawler, *args, **kwargs)
#         crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
#         return spider
#
#     def note_to_server(self, subject_url, current_url, item):
#         '''提取数据项
#         :param subject_url:帖子url
#         :param current_url:当前url
#         :param item:数据项
#         :return: None
#         '''
#         if not item:
#             return
#         self.sender['url'] = subject_url
#         self.sender['current_url'] = current_url
#         self.sender['floor'] = item['floor']
#         self.sender['type'] = getattr(self.task, 'note', 'N/A')
#         data_sender(self.sender)
#
#     def spider_closed(self, spider):
#         '''关闭爬虫时触发，然后发送一个标识位到管道来表明爬虫已经结束
#         :param spider: 爬虫对象
#         :return: None
#         '''
#         self.pipe.send('shutdown')
#
#     @staticmethod
#     @cleaner_decorator({'列表检查': {}})
#     def clean_normal(data):
#         # 普通清洗
#         return data
#
#     @staticmethod
#     @cleaner_decorator({'列表检查': {}}, {'string转int': {}})
#     def clean_floor(data):
#         return data
#
#     @staticmethod
#     @cleaner_decorator({'列表检查': {}}, {'string转json': {}})
#     def clean_author_info(data):
#         # 再次清洗用户信息和评论的信息
#         return data
#
#     @staticmethod
#     @cleaner_decorator({'列表检查': {}}, {'去除两端空白': {}}, {'时间适配': {'format': '%Y-%m-%d %H:%M'}})
#     def clean_date(data):
#         # 清洗日期
#         return data
#
#     @staticmethod
#     @cleaner_decorator({'列表检查': {}}, {'去除两端空白': {}})
#     def clean_content(data):
#         # 清洗content
#         return data
#
#
# class NormalSpider(SingleSpider):
#     '''普通的二级爬虫'''
#     name = 'normal_spider'
#
#     def parse(self, response):
#         article = get_data_by_xpath(response, self.pages.get('body'))
#         article = map(lambda x: urljoin(response.url, x), article)
#         yield from [Request(one, callback=self.parse_one) for one in article]
#         url = get_data_by_xpath(response, self.pages.get('next'))
#         if url:
#             url = urljoin(response.url, self.clean_normal(url))
#             yield SplashRequest(url, dont_filter=True, meta={'spider_name': self.name}) if \
#                 self.task.java_script else Request(url, dont_filter=True, meta={'spider_name': self.name})
#
#     def parse_one(self, response):
#         '''
#         :param response:响应体
#         :return: item数据项
#         '''
#         self.pipe.send(source_data_package(response, self.source_task['xpath']))
#         item = {}
#         for k, v in self.task.xpath.items():
#             item[k] = get_data_by_xpath(response, v['xpath'])
#         item['url'] = response.url
#         yield item
#
#
# class WeiXinSpider(SingleSpider):
#     '''微信爬虫'''
#     name = "weixin_spider"
#
#     def parse(self, response):
#         article = get_data_by_xpath(response, self.pages[0].get('body'))
#         article = map(lambda x: urljoin(response.url, x), article)
#         yield from [Request(one, callback=self.parse_one, meta={'spider_name': self.name}) for one in article]
#         nxt = get_data_by_xpath(response, self.pages[0].get('next'))
#         if nxt:
#             nxt = urljoin(response.url, nxt[0])
#             yield SplashRequest(nxt, dont_filter=True, meta={'spider_name': self.name}) if self.task.java_script else \
#                 Request(nxt, dont_filter=True, meta={'spider_name': self.name, 'referer': response.url})
#
#     def parse_one(self, response):
#         self.pipe.send(source_data_package(response, self.source_task['xpath']))
#         item = {}
#         for k, v in self.task.xpath.items():
#             item[k] = get_data_by_xpath(response, v['xpath'])
#         item['url'] = response.url
#         yield item
#
#
# class NormalCrawlSpider(CrawlSpider):
#     '''
#     全站抓取爬虫，这个爬虫用于全站抓取的需求
#     '''
#     name = 'normal_crawl_spider'
#     next_pages = set()
#
#     def __init__(self, init, pipe, *args, **kw):
#         task = Task()
#         [setattr(task, k, v) for k, v in init.items()]
#         self.name = init.get('spider_crawl_name', task.spider_name)
#         self.task = task
#         self.pipe = pipe
#         self.source_task = init
#         self.allowed_domains = task.page.get('allowed_domains')
#         self.start_urls = task.page.get('start_urls')
#         # rules尝试了迭代配置来生成Rule对象，但是只要一迭代就不能调用callback，故采用代码eval
#         self.rules = eval(task.page.get('rules'))
#         self.download_delay = task.delay
#         super().__init__(self.name, *args, **kw)
#
#     def _requests_to_follow(self, response):
#         '''不添加翻页url到redis去重队列
#         :param response:
#         :return:
#         '''
#         if not isinstance(response, (HtmlResponse, SplashTextResponse)):
#             return
#         seen = set()
#         length = len(self._rules)
#         for n, rule in enumerate(self._rules):
#             links = [lnk for lnk in rule.link_extractor.extract_links(response)
#                      if lnk not in seen]
#             if links and rule.process_links:
#                 links = rule.process_links(links)
#             for link in links:
#                 seen.add(link)
#                 if length == n + 1:
#                     # 最后一个rule是页节点url，需要去重
#                     r = Request(url=link.url, callback=self._response_downloaded) if not self.task.java_script else \
#                         SplashRequest(url=link.url, callback=self._response_downloaded)
#                     r.meta.update(rule=n, link_text=link.text)
#                     yield rule.process_request(r)
#                 else:
#                     # 不添加翻页到redis去重队列
#                     r = Request(url=link.url, callback=self._response_downloaded, dont_filter=True) if not self.task.java_script else \
#                         SplashRequest(url=link.url, callback=self._response_downloaded, dont_filter=True)
#                     if link.url not in NormalCrawlSpider.next_pages:
#                         NormalCrawlSpider.next_pages.add(link.url)
#                         r.meta.update(rule=n, link_text=link.text)
#                         yield rule.process_request(r)
#
#     def start_requests(self):
#         yield from [SplashRequest(url, dont_filter=True, meta={'spider_name': self.name}) if
#                     self.task.java_script else Request(url, dont_filter=True, meta={'spider_name': self.name})
#                     for url in self.start_urls]
#
#     def parse_item(self, response):
#         '''处理具体请求
#         :param response:响应体
#         :return:字典数据
#         '''
#         self.pipe.send(source_data_package(response, self.source_task['xpath']))
#         item = {}
#         for k, v in self.task.xpath.items():
#             item[k] = get_data_by_xpath(response, v['xpath'])
#         item['url'] = response.url
#         yield item
#
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(NormalCrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
#         crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
#         return spider
#
#     def spider_closed(self, spider):
#         self.pipe.send('shutdown')
#
#
# class NormalXMLFeedSpider(XMLFeedSpider):
#     # 预留XML spider
#     pass
#
#
# class NormalCSVFeedSpider(CSVFeedSpider):
#     # 预留CSV spider
#     pass
#
#
# class NormalSitemapSpider(SitemapSpider):
#     # 预留Sitemap spider
#     pass
#
#
#
