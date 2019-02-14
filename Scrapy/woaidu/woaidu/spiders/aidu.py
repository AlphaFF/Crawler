# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import WoaiduItem

class AiduSpider(scrapy.Spider):
    name = 'aidu'
    allowed_domains = ['woaidu.org']
    start_urls = ['http://www.woaidu.org/sitemap_1.html']

    def parse(self, response):
        next_link = response.xpath('//div[@class="k2"]/div/a[text()="下一页"]/@href').extract_first()
        print(next_link)
        if next_link:
            url = urljoin(response.url,next_link)
            yield scrapy.Request(url,callback=self.parse)

        for detail_link in response.xpath('//div[@class="zuo1"]/div/a/@href').extract():
            url = urljoin(response.url,detail_link)
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self,response):
        item = WoaiduItem()
        item['name'] = response.xpath('//div[@class="zizida"]/text()').extract_first()
        item['url'] = response.url
        item['author'] = response.xpath('//div[@class="xiaoxiao"]/text()').extract_first()[5:].strip()
        item['desc'] = response.xpath('//div[@class="lili"]/text()').extract_first().strip()

        yield item
