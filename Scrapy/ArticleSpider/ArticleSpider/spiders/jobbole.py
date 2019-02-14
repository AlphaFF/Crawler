# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from ..items import ArticlespiderItem, ArticlespiderLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    handle_httpstatus_list = [404]

    def __init__(self):
        self.failed_urls = []
        super(JobboleSpider,self).__init__()
        dispatcher.connect(self.handle_spider_closed,signals.spider_closed)

    def handle_spider_closed(self,spider,reason):
        print('hahaha')

    def parse(self, response):
        print(response.headers)
        if response.status == 404:
            self.failed_urls.append(response.url)
            self.crawler.stats.inc_value('faild_urls')
        results = response.xpath('//div[@id="archive"]/div[contains(@class,"post floated-thumb")]')
        for result in results:
            url = result.xpath('.//a/@href').extract_first()
            try:
                img_url = result.xpath('.//a/img/@src').extract_first()
                img_url_real = parse.urljoin(response.url, img_url)
            except Exception as e:
                print(e)
                img_url = ''
                img_url_real = ''
            yield scrapy.Request(url, callback=self.get_detail, meta={'img_url': img_url_real})
        # yield scrapy.Request('http://blog.jobbole.com/61/',callback=self.get_detail)
        # pages = response.xpath('//a[@class="page-numbers"][last()]/text()').extract()[0]
        # if pages:
        #     print(pages)
        #     for page in range(2,int(pages)+1):
        #         url = 'http://blog.jobbole.com/all-posts/page/{}/'.format(str(page))
        #         yield scrapy.Request(url, callback=self.parse)


    def get_detail(self, response):
        # loader如果已经加载到了值，就不会再加载值了
        img_url = response.meta.get('img_url')
        # praise_num = response.xpath('//div[@class="post-adds"]//h10/text()')
        loader = ArticlespiderLoader(item=ArticlespiderItem(), response=response)
        loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        loader.add_value('img_url', img_url)
        loader.add_value('url', response.url)
        loader.add_xpath('content', '//div[@class="entry"]')
        # loader.add_xpath('praise_num', '//div[@class="post-adds"]//h10/text()')

        loader.add_css("praise_num", ".vote-post-up h10::text")
        loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        loader.add_xpath('fav_num', '//div[@class="post-adds"]/span[2]/text()')
        loader.add_xpath('comment_num', '//div[@class="post-adds"]/a/span/text()')
        loader.add_value('praise_num', '0')
        loader.add_value('fav_num', '0')
        loader.add_value('comment_num', '0')
        loader.add_xpath('tag','//p[@class="entry-meta-hide-on-mobile"]/a/text()')

        article_item = loader.load_item()
        yield article_item
