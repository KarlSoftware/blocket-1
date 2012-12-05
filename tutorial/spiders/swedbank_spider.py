from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from tutorial.items import TutorialItem
import codecs

class SwedbankSpiderSpider(CrawlSpider):
    name = 'swedbank_spider'
    allowed_domains = ['swedbankrobur.se']
    start_urls = ['http://fonder.swedbankrobur.se/robur/site/query.action']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'\.htm'), callback='parse_iframe', follow=True),
    )

    def parse_iframe(self, response):
        self.log('awyeah!')

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = TutorialItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
