# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging


class JokePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', '', 'test', charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql, params = item.insert_into_sql()
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(sql)
        return item
