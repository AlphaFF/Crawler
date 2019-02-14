# -*- coding: utf-8 -*-
import scrapy
import json
import re
from datetime import datetime
from ..items import JokeItem

class JokeNeihanSpider(scrapy.Spider):
    name = 'joke_neihan'
    # allowed_domains = ['neihanshequ.com/']
    start_urls = ['https://neihanshequ.com/']

    def parse(self, response):
        results = response.xpath('//ul[@id="detail-list"]/li')
        for result in results:
            content = result.xpath('.//div[@class="content-wrapper"]//p/text()').extract_first()
            create_time = result.xpath('.//span[contains(@class,"time")]/text()').extract_first().strip()
            fav_num = result.xpath('.//span[@class="digg"]/text()').extract_first()

        max_time = re.findall(r'max_time: \'(.*?)\',',response.text)[0]
        load_more = response.xpath('//div[@id="loadMore"]').extract_first()
        if load_more:
            url = 'https://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}'.format(max_time)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        results = json.loads(response.text)
        result = results.get('data')
        datas = result.get('data')
        item = JokeItem()
        for data in datas:
            content = data.get('group').get('content')
            publish_time = data.get('group').get('create_time')
            publish_time = datetime.fromtimestamp(float(publish_time))
            digg_count = data.get('group').get('digg_count')

            item['content'] = content
            item['fav_num'] = digg_count
            item['data_from'] = '内涵'
            item['publish_time'] = publish_time
            item['tags'] = ''

            yield item


        has_more = result.get('has_more')
        max_time = result.get('max_time')

        if has_more:
            url = 'https://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time={}'.format(max_time)
            yield scrapy.Request(url, callback=self.parse_detail)



