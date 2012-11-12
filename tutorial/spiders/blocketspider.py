from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import codecs
import re

class BlocketSpider(BaseSpider):
    name = "blocket"
    allowed_domains = ["blocket.se"]
    start_urls = [
        "http://www.blocket.se/hela_sverige?q=downhill&cg=6060&w=3&st=s&c=&ca=14&l=0&md=th"
    ]
    output_file = codecs.open("/home/jonas/Kod/scrapy/tutorial/test.html",
                                  encoding='utf-8', mode='w+')
    max_cost = 13000
    min_cost = 4000

    def get_blocket_items(self, hxs, classname):
            xpath = '//div[@class="' + classname + '"]'
            return hxs.select(xpath)

    def print_to_file(self,text):
        output_file = self.output_file
        output_file.write(text)
        output_file.write(unicode('</br>\n'))

    def iterate_blocket_items(self,items):
        for item in items:
            price = item.select('div/p/text()').extract()[0]
            # cleaning the tags and whitespace away
            price = re.sub(':.*','', price)
            price = re.sub('\s','', price)
            # concat the strings with price and text
            text = item.select('div/a/text()').extract()[0] + u' ' + price
            # if the item costs more
            if price and int(price) > self.min_cost and int(price) < self.max_cost:
                self.print_to_file(text)

            
    def parse(self, response):


        hxs = HtmlXPathSelector(response)
        

        
        items = self.get_blocket_items(hxs, 'item_row item_row_first')
        self.iterate_blocket_items(items)
        items = self.get_blocket_items(hxs, 'item_row')
        self.iterate_blocket_items(items)
        items = self.get_blocket_items(hxs, 'item_row item_row_last')
        self.iterate_blocket_items(items)
        
                

        self.output_file.close()
    

        
