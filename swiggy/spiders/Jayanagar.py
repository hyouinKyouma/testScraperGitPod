import scrapy
class JayanagarSpider(scrapy.Spider):
    name = 'jayanagar'
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    #allowed_domains = ['www.zomato.com']
    start_urls = ["https://www.swiggy.com/bangalore/jayanagar-restaurants"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'jayanagar.csv'
    }
    def __init__(self):
        self.domain = "https://www.swiggy.com/bangalore/jayanagar-restaurants"
        self.domain2 = "https://www.swiggy.com"
        self.page_no = 2
        
    def save_restaurent_page(self,response):
        print("________-****-****_8",response.url)
        rest_name = response.xpath('//h1[@class="_3aqeL"]/text()').extract_first()
        rating = response.xpath('//span[@class="_20F32"]//span/text()').extract_first()
        del_status = response.xpath('//span[contains(@class, "_27qo_")]/text()').get()
        # cost_for_two = response.xpath('//div[@class="_20F32"]/text()').extract_first()
        details_row = list(response.xpath('//div[@class="pr21h"]'))
        print("****************---------len : ",len(details_row))
        address = ''.join(details_row[0].xpath('.//div[@class="_396MD"]/text()').getall())
        cuisine = details_row[1].xpath('.//div[@class="_396MD"]/text()').extract_first()
        phone = details_row[2].xpath('.//div[@class="_396MD"]/text()').extract_first()
        fssai = response.xpath('//li[@class="_167GT"]/text()').extract_first()
        #print('\n\n\nrest: ', rest_name,'\nrating ',rating ,'\ndel_status:',del_status,'\ncost_for_two ',cost_for_two,'\naddress ',address,'\ncuisine ',cuisine,'\nfssai ',fssai,'\nphone: ',phone,'\n\n\n')
        yield{
            "restaurant_name":rest_name,
            "location":"jayanagar",
            "status":del_status,
            "rating":rating,
            # "cost_for_two":cost_for_two,
            "address":address,
            "cusine":cuisine,
            "fssai":fssai
        }
    def parse(self, response):
        pagination = response.xpath('//a[@class="_1FZ7A"]').extract()
        if(pagination):
            main_pages_of_restaurents = response.xpath('//a[@class="_1j_Yo"]/@href').extract()
            for main_page_of_restaurent in main_pages_of_restaurents:
                yield scrapy.http.Request(url = self.domain2+main_page_of_restaurent,callback = self.save_restaurent_page)
            #print(main_pages_of_restaurents)
            link = ''
            if("?page=" in response.url):
                link = response.url.split("=")[0]+"="+str(self.page_no)
            else:
                link = response.url+"?page=1"
            self.page_no = self.page_no+1
            yield scrapy.http.Request(url = response.urljoin(link),callback = self.parse)
                  
    
        
        