# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', '', 'test', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''
            insert into jobbole(title,url,create_date,img_url,praise_num,fav_num,comment_num,content) values (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.cursor.execute(sql, (
        item['title'], item['url'], item['create_date'], item['img_url'], item['praise_num'], item['fav_num'],
        item['comment_num'], item['content']))
        self.conn.commit()
        return item

# 异步存储mysql
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['HOST'],
            user=settings['USER'],
            passwd=settings['PASSWD'],
            db=settings['DB'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)
        pass

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        sql = '''
                    insert into jobbole(title,url,create_date,img_url,praise_num,fav_num,comment_num,content) values (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        cursor.execute(sql, (
            item['title'], item['url'], item['create_date'], item['img_url'], item['praise_num'], item['fav_num'],
            item['comment_num'], item['content']))
        # self.conn.commit()
        pass
    pass
