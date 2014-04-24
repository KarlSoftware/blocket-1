from scrapy.spider import BaseSpider
from scrapy.selector import Selector
import codecs
import re

class BlocketSpider(BaseSpider):
    name = "blocket"
    allowed_domains = ["blocket.se"]

    output_file = codecs.open("/home/jonas/data/scrapy/blocket.csv",
                                  encoding='utf-8', mode='w+')
    max_cost = 13000
    min_cost = 4000

    def __init__(self, searchword='downhill', category='6060'):
 
        self.start_urls = [
            "http://www.blocket.se/hela_sverige?q=%s&cg=%s&w=3&st=s&c=&ca=14&l=0&md=th" % ( searchword, category )
            ]

    def get_blocket_items(self, hxs, classname):
            xpath = '//div[@class="' + classname + '"]'
            return hxs.xpath(xpath)

    def print_to_file(self,text):
        """Print a text to a file that is specified for this class"""
        output_file = self.output_file
        output_file.write(text)
        output_file.write(unicode('\n'))

    def get_relative_item(self,item,xpath):
        """Gets the path from a html path selector, returns False if no hit"""
        result = item.xpath(xpath).extract()
        if result.__len__() == 0:
            return False
        return result[0]
        
    
    

    def iterate_blocket_items(self,items):
        for item in items:
            text = ""
            price = self.get_relative_item(item,'div/p/text()')
            if price:
                price = re.sub('\s','',price)
                price = re.sub('\:.*','',price)
                text = price
            else:
                continue
            name = self.get_relative_item(item,'div/a/text()')
            if name:
                text = name + u',' + text
            date = self.get_relative_item(item,'div/div/text()')
            if date:
                text = date + u',' + text
            
            
            # if the item costs more
            if price and int(price) > self.min_cost and int(price) < self.max_cost:
                self.print_to_file(text)

            
    def parse(self, response):


        hxs = Selector(response)
        

        
        items = self.get_blocket_items(hxs, 'item_row item_row_first')
        self.iterate_blocket_items(items)
        items = self.get_blocket_items(hxs, 'item_row')
        self.iterate_blocket_items(items)
        items = self.get_blocket_items(hxs, 'item_row item_row_last')
        self.iterate_blocket_items(items)
        
                

        self.output_file.close()
