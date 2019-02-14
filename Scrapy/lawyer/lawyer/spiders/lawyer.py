#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlphaFF
# @Date:   2018-08-31 09:09:22
# @Email: liushahedi@gmail.com
# @Last Modified by:   AlphaFF
# @Last Modified time: 2018-08-31 09:37:25

import scrapy
from scrapy_splash import SplashRequest


class LawyerSpider(scrapy.Spider):
    name = 'lawyer'
    allow_domains = ['bjsf.gov.cn']
    start_urls = ['http://www.bjsf.gov.cn/publish/portal0/tab145/']

    def start_requests(self):
        splash_args = {
            'wait': 2
        }
        headers = {
            'Host': 'www.bjsf.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,la;q=0.6',
        }
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse_result,
                                endpoint='render.html',
                                splash_headers=headers,
                                args=splash_args)

    def parse_result(self, response):
        print('北京市亚奥律师事务所' in response.text)
        pass
