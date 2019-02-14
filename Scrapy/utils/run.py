#!/usr/bin/env python3
# coding=utf-8

# 同一个进程运行多个spider, 每次self.crawl的时候就会新开一个进程
from spiders.xcqq import XcqqSpider
from spiders.zghb import ZghbSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

configure_logging()
runner = CrawlerRunner()
runner.crawl(XcqqSpider)
runner.crawl(ZghbSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

if __name__ == "__main__":
    reactor.run()