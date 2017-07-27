import six
from scrapy.linkextractors.lxmlhtml import LxmlParserLinkExtractor
from six.moves.urllib.parse import urljoin

import lxml.etree as etree
from w3lib.html import strip_html5_whitespace
from w3lib.url import canonicalize_url

from scrapy.link import Link
from scrapy.utils.misc import arg_to_iter, rel_has_nofollow
from scrapy.utils.python import unique as unique_list, to_native_str
from scrapy.utils.response import get_base_url
from scrapy.linkextractors import FilteringLinkExtractor


class RegexLinkExtractor():
    def __init__(self, restrict_re='', base_url=None):
        self.restrict_re = restrict_re
        self.base_url = base_url
    
    def extract_links(self, response):
        if not self.base_url:
            self.base_url = get_base_url(response)
        items = response.xpath('.').re(self.restrict_re)
        print(items)
        all_links = [Link(response.urljoin(self.base_url.format(str(item))), text=str(item)) for item in items]
        return unique_list(all_links)
