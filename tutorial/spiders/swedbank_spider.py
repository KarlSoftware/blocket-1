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
        Rule(SgmlLinkExtractor(allow=r'fonder', deny=('.*nyheter.*','fonder\.')), callback='parse_iframe', follow=False),
        )


    
    def parse_iframe(self, response):
        output_file = codecs.open("/home/jonas/data/scrapy/swedbank.txt",
                                  encoding='utf-8', mode='a')
        output_file.write(response.url + '\n')
        output_file.close()

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = TutorialItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i
