from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
import codecs


class RoburSpider(BaseSpider):
    name = "robur"
    allowed_domains = ["swedbankrobur.se"]
    start_urls = (
        'http://fonder.swedbankrobur.se/robur/site/query.action',
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        self.log( response.url)
        numOfLinks = len(hxs.select('//a'))
        self.log('There are ' + str(numOfLinks) + ' number of links')
