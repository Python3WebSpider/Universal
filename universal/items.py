# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class SongItem(Item):
    name = Field()
    url = Field()
    style = Field()
    lyric = Field()


class ZhihuUserItem(Item):
    name = Field()
    url = Field()


class NewsItem(Item):
    url = Field()
    website = Field()
    crawl_time = Field()
    publish_time = Field()
    source = Field()
    source_url = Field()
    title = Field()
    content = Field()
    hot = Field()
    hits = Field()
    replies = Field()
    author = Field()
