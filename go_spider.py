from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from swiggy.spiders.yeshwanthpur import YeshwanthpurSpider

 
process = CrawlerProcess(get_project_settings())
process.crawl(YeshwanthpurSpider)
process.start()




