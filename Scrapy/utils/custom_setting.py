import scrapy

class TestSpider(scrapy.Spider):
    name = "Test"
    ...
    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }