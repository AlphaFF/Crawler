import scrapy
import json
import re
from datetime import datetime
from ..items import JokeItem
from urllib.parse import urljoin
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import logging


class JokeNeihanSpider(scrapy.Spider):
    name = 'joke_qiushi'
    start_urls = ['https://www.qiushibaike.com/']

    def __init__(self):
        self.crawled_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('crawled_urls', ','.join(self.crawled_urls))
        logging.warning(self.crawler.stats)

    def parse(self, response):
        self.crawled_urls.append(response.url)
        self.crawler.stats.inc_value('crawled_url')
        item = JokeItem()
        results = response.xpath('//div[@id="content-left"]/div')
        for result in results:
            content = ''.join(result.xpath('.//div[@class="content"]/span/text()').extract())
            create_time = datetime.now()
            fav_num = result.xpath('.//span[@class="stats-vote"]/i[@class="number"]/text()').extract_first()
            item['content'] = content.strip()
            item['publish_time'] = create_time
            item['fav_num'] = fav_num
            item['tags'] = ''
            item['data_from'] = '糗事'
            yield item

        next = response.xpath('//span[@class="next"]/text()').extract_first()

        if next and next.strip() == '下一页':
            next_url = response.xpath('//ul[@class="pagination"]//a/@href').extract()[-1]
            next_url = urljoin(response.url, next_url)
            yield scrapy.Request(next_url, callback=self.parse)
