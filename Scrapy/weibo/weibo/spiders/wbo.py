# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


class WboSpider(scrapy.Spider):
    name = 'wbo'
    allowed_domains = ['weibo.com']

    def __init__(self, task_id=None, object_urls=None, *args, **kw):
        super(WboSpider, self).__init__(*args, **kw)
        self.start_urls = ['https://m.weibo.cn/p/1005052803301701',
                           'https://m.weibo.cn/u/2189067512']

    def start_requests(self):
        for start_url in self.start_urls:
            container_id = ''
            url_head = 'https://m.weibo.cn/api/container/getIndex?containerid='
            if 'm.weibo.cn/p/' in start_url:
                container_id = start_url.replace('https://m.weibo.cn/p/', '').replace('100505', '107603')
            elif 'https://m.weibo.cn/u/' in start_url:
                container_id = '107603' + start_url.replace('https://m.weibo.cn/u/', '')
            if container_id:
                origin_url = '%s%s' % (url_head, container_id)
                yield Request(origin_url, callback=self.parse)


    def parse(self, response):
        content = json.loads(response.text)
        # print(content)
        weibo_info = content.get('data').get('cards', [])
        for info in weibo_info:
            print('info====',info)
            if info.get('mblog') and info.get('mblog').get('text'):
                title = info['mblog']['text']
                url = "https://m.weibo.cn/status/%s" % info["mblog"]["mid"]
                time_str = info.get('mblog').get('created_at')
                print('=====微博内容=====')
                print(title)
                print(url)
                print(time_str)
        pass
