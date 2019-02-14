# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JokeItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    publish_time = scrapy.Field()
    fav_num = scrapy.Field()
    data_from = scrapy.Field()
    tags = scrapy.Field()

    def insert_into_sql(self):
        sql = 'insert into joke (content,fav_num,tags,data_from,publish_time) values (%s,%s,%s,%s,%s)'
        params = (self['content'],self['fav_num'],self['tags'],self['data_from'],self['publish_time'])
        return sql,params
