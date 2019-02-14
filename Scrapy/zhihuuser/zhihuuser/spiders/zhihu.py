# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhihuuserItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    user_url = 'https://www.zhihu.com/people/sgai/following'
    following_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
    followed_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'

    def start_requests(self):
        yield scrapy.Request(self.following_url,callback=self.parse_user)
        # yield scrapy.Request(self.followed_url,callback=self.parse)

    def parse_user(self, response):
        # print(response.text)
        results = json.loads(response.text).get('data')
        for result in results:
            url_token = result.get('url_token')
            name = result.get('name')
            following_url = 'https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'.format(url_token)
            yield scrapy.Request(following_url,callback=self.parse_user)

