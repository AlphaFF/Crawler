# -*- coding: utf-8 -*-
import scrapy
from ArticleSpider.damatuWeb import DamatuApi
import io
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']

    start_urls = ['https://zhihu.com/']

    rules = (
        Rule(link_extractor=LinkExtractor(allow=(r'question/\d+?')),callback='get_questions',follow=True),
        Rule(link_extractor=LinkExtractor(allow=(r'question/\d+?/answer/\d+?')),callback='get_answers',follow=True)
    )

    def start_requests(self):
        url = 'https://www.zhihu.com/signin'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'www.zhihu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        return [scrapy.Request(url, headers=headers, callback=self.get_xsrf)]

    def get_xsrf(self, response):
        _xsrf = response.xpath('//input[@name="_xsrf"]/@value').extract()[0]
        captcha_url = 'https://www.zhihu.com/captcha.gif?type=login&lang=en'
        headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'www.zhihu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        return [scrapy.Request(captcha_url, headers=headers,callback=self.get_code,meta={'_xsrf':_xsrf})]

    def get_code(self,response):
        _xsrf = response.meta.get('_xsrf')
        dmt = DamatuApi("yscredit", "Yscredit08")
        vcode = dmt.decode(io.BytesIO(response.body), 54).strip().lower()
        print(vcode)
        login_url = 'https://www.zhihu.com/login/email'
        data = {
            '_xsrf':_xsrf,
            'email':'liushahedi@163.com',
            'password':'31415926fw',
            'captcha_type': 'en',
            'captcha': vcode
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'www.zhihu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        yield scrapy.FormRequest(login_url,formdata=data,headers=headers,callback=self.after_login)
            
    def after_login(self,response):
        print(response.text)
        url = 'https://www.zhihu.com/'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': ' gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'www.zhihu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        yield scrapy.Request(url,headers=headers,callback=self.get_index)


    def get_index(self,response):
        print('in this methods...')
        print(response.text)
        pass

    def get_answers(self,response):
        print(response.text)

    def get_questions(self,response):
        print(response.text)
