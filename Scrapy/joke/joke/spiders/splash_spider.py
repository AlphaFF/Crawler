import scrapy
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware


class SplashSpider(Spider):
    name = 'splash'
    start_urls = ['http://www.baidu.com']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.get_res, endpoint='render.html', args={'wait': 0.5})

    def get_res(self, response):
        print(response.text)
        print('ending...')
