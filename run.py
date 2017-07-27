import sys
from universal.spiders.universal import UniversalSpider
from universal.utils import get_config
from scrapy.crawler import CrawlerProcess


def run():
    name = sys.argv[1]
    custom_settings = get_config(name)
    process = CrawlerProcess(custom_settings.get('settings'))
    process.crawl(UniversalSpider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()
