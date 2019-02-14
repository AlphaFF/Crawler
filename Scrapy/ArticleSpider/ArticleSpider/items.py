# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from datetime import datetime
import re


def convert_date(date):
    try:
        create_date = datetime.strptime(date, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date


def get_first_one(value):
    try:
        return value[0]
    except Exception as e:
        print(e)


def get_num(value):
    re_match = re.match(r'.*?(\d+).*', value)
    if re_match:
        num = int(re_match.group(1))
    else:
        num = 0
    return num


class ArticlespiderLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # img_url_out = TakeFirst()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    # img_path = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field(input_processor=MapCompose(get_num))
    comment_num = scrapy.Field(input_processor=MapCompose(get_num))
    fav_num = scrapy.Field(input_processor=MapCompose(get_num))
    tag = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(convert_date))
