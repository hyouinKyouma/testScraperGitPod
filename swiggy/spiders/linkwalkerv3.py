import scrapy
from scrapy_selenium import SeleniumRequest
import random
import pandas as pd
import boto3  
import io
import os
import logging


os.environ['OP_FILE'] = 'test923.csv'
os.environ['IP_FILE'] = 'myntra_parameters.csv'

class Linkwalkerv3Spider(scrapy.Spider):
    name = 'linkwalkerv3'
# -*- coding: utf-8 -*-
# os.environ(opfile)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    # user_agent = "Mozilla/5.0 (X11; Linux i686; rv:79.0) Gecko/20100101 Firefox/79.0"
    # custom_settings = {
    #     'FEED_FORMAT':'csv',
    #     'FEED_URI':'s3://linkwalker-op/%s'%(os.getenv('OP_FILE'))
    # }
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'g2.csv'
    }
    
    # custom_settings = {
    #     pathlib.Path('items.csv'): {
    #     'format': 'csv'
    #     # 'fields': ['price', 'name'],
    # }
    # }
    # UTILITY FUNCTIONS--------------->>>
    # For extracting values based on the xpath
    def xptahExtractor(self,response,x_path):
        try:
            extracted_val = response.xpath(x_path).extract()
            return extracted_val
        except Exception as e:
            return ("---------------->>> XPATH RETURNED AN EMPTY ARRAY\n",e)

        
    # For extracting values based on the css class
    def cssExtractor(self,response, css_class):
        try:
            extracted_val = response.css(css_class).extract()
            return extracted_val
        except Exception as e:
            return ("----------------->>>CSS RETURNED AN EMPTY ARRAY\n",e)

    #function to save html files 
    def save_html(self,html,name):
        file = open(str(name),'w',encoding='utf-8')
        file.write(html)
        file.close()

    # setting the range of page
    def pageRangeSetter(self):
        urls = []
        for i in range(self.page_range_start,self.page_range_end):
            page = i
            page = str(page)
            temp_link = self.super_link.replace('PAGE',page)
            urls.append(temp_link) 
        return urls

    # reading csv file from amazon s3 bucket for patrameters
    def readCsvFromS3(self,access_key,secret_access_key,input_bucket,input_file):
        s3c = boto3.client(
            's3', 
            # region_name = REGION,
            # aws_access_key_id='AKIAIJ4PRNXZHJWOXQFA',
            # aws_secret_access_key='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'
            # 'linkwalker-ip'
            # 'test_para_3.csv'
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )
        obj = s3c.get_object(Bucket=input_bucket,Key =input_file)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8',header=None)
        return df 
    
    def start_requests(self):
        urls = self.urls
        print("--------------------------------->URLS",urls)
        for url in urls:
            yield SeleniumRequest(
                url=url, 
                callback=self.parse_result,
                wait_before_scroll=1,
                infiniteScroll=True
            )

    def __init__(self):
        # self.df = self.readCsvFromS3('AKIAIJ4PRNXZHJWOXQFA',
        #                             'gV/RxdNoXK81jI58KSHZDRTn8sjorVIFb6+U+mvp',
        #                             'linkwalker-ip',
        #                             os.getenv('IP_FILE')
        #                             )
        self.df = pd.read_csv("myntra_parameters2.csv",header=None)
        self.domain = self.df.iat[1,3]
        self.page_range_start =int(self.df.iat[1,1])
        self.page_range_end =int(self.df.iat[1,2])
        self.super_link = self.df.iat[1,0]
        self.loop_range = int(self.df.shape[1])
        self.urls = self.pageRangeSetter()        

    def parse_result(self, response):
        """
        @url http://www.amazon.com/s?field-keywords=selfish+gene
        @returns items 1 16
        @returns requests 0 0
        @scrapes Title Author Year Price

        """
        # for getting sublinks
        # xpath_sublinks=self.df.iat[1,4]
        sub_links = response.xpath(self.df.iat[1,4]).extract()
        # sub_links = self.xptahExtractor(response,xpath_sublinks)
        # print("sublinks--------",sub_links)
        for link in sub_links:
            print('self.domain + link,=========>>',self.domain + link,)
            yield SeleniumRequest(url = self.domain + link, callback=self.extractAttributes, wait_time=20)
                                   
    def extractAttributes(self,response):
        # print("response headers====================================>>",response.request.meta['Firefox'].title)
        print("====================================>>",response)
        MyDictionaryObj = dict()
        for i in range(6,self.loop_range):
            # extracted_val = self.xptahExtractor(response,self.df.iat[1,i])
            extracted_val = response.xpath(self.df.iat[1,i]).extract()
            if extracted_val == '':
                self.logger.warning('No item received for 2nd iteration %s', response.url)
            print("extracted Val---------------->>>",extracted_val)
            header_op_csv= self.df.iat[0,i]
            MyDictionaryObj[header_op_csv] = extracted_val
            print("=============================================>",MyDictionaryObj)    
        yield MyDictionaryObj



       
         
        

