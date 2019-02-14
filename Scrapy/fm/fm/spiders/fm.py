#!/usr/bin/env python3
# coding=utf-8

import scrapy
import json

class JokeNeihanSpider(scrapy.Spider):
    name = 'fm_xmly'
    # allowed_domains = ['neihanshequ.com/']
    start_urls = ['http://www.ximalaya.com/dq/news/']

    def parse(self, response):
        print(response.text)
        results = response.xpath('//div[@class="discoverAlbum_wrapper"]/div/@album_id').extract()
        for result in results:
            print(result)
            url = 'http://www.ximalaya.com/tracks/{}.json'.format(result)
            yield scrapy.Request(url,callback=self.parse_detail)
        pass

    def parse_detail(self,response):
        result = json.loads(response.text)
        title = result.get('title')
        url = result.get('play_path')
        author = result.get('nickname')
        pass