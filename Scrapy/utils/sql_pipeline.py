# !/usr/bin/env python3
# coding:utf-8

import scrapy
import pymysql
from twisted.enterprise import adbapi
import logging


class SomeItem(scrapy.Item):
    name = scrapy.Field()

    def insert_into_sql(self):
        sql = 'insert into test (name) values (%s)'
        params = (self['name'])
        return sql, params


# 插入mysql数据库
class MysqlPipeline():
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', db='test', user='root', password='', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        self.count = 0

        def process_item(self, item, spider):
            sql, params = item.insert_into_sql()
            try:
                self.cursor.execute(sql, params)
                self.count += 1
                if self.count % 500 == 0:
                    self.conn.commit()
                    self.count = 0
                    logging.info("成功提交500条")
            except pymysql.Error as e:
                print(e)
                print(sql)

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

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        pass

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        sql = '''
                    insert into jobbole(title,url,create_date,img_url,praise_num,fav_num,comment_num,content) values (%s,%s,%s,%s,%s,%s,%s,%s)
                '''
        cursor.execute(sql, (
            item['title'], item['url'], item['create_date'], item['img_url'], item['praise_num'], item['fav_num'],
            item['comment_num'], item['content']))
        # 不需要提交的,自己会提交
        # self.conn.commit()
        pass

    pass


import MySQLdb
import MySQLdb.cursors
import logging
from twisted.enterprise import adbapi

# 过时了
class CnblogsPipelineobj(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            dbapiName='MySQLdb',
            host='127.0.0.1',
            db='cnblogs',
            user='root',
            passwd='密码',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=False
        )

    # pipeline dafault function
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        logging.debug(query)
        return item

    # insert the data to databases
    def _conditional_insert(self, tx, item):
        parms = (item['Title'], item['TitleUrl'])
        sql = "insert into blogs values('%s','%s') " % parms
        # logging.debug(sql)
        tx.execute(sql)


from sqlalchemy import Column, Integer, String, Date, DateTime, Text,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from settings import MYSQL_CONN
from datetime import datetime

MYSQL_CONN = {
    'host':'127.0.0.1',
    'user':'user_name',
    'password':'user_pwd',
    'db':'test_db',
    'table':'test_tb',
    'mysql_uri':'mysql://{user}:{pwd}@{host}:3306/{db}?charset=utf8'
}
# declare a Mapping,this is the class describe map to table column

Base = declarative_base()


class Cnbeta(Base):
    __tablename__ = 'cnbeta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=False, default=0)
    catid = Column(Integer, nullable=False, default=0)
    score_story = Column(String(512), nullable=False, default='')
    hometext = Column(String(1024), nullable=False, default='')
    counter = Column(Integer, nullable=False, default=0)
    inputtime = Column(DateTime, nullable=False, default=datetime.now())
    topic = Column(Integer, nullable=False, default=0)
    source = Column(String(128), nullable=False, default='')
    mview = Column(Integer, nullable=False, default=0)
    comments = Column(Integer, nullable=False, default=0)
    crawled_datetime = Column(DateTime, nullable=False, default=datetime.now())
    rate_sum = Column(Integer, nullable=False, default=0)
    title = Column(String(512), nullable=False, default='')
    url_show = Column(String(512), nullable=False, default='')
    thumb = Column(String(256), nullable=False, default='')


def create_session():
    # declare the connecting to the server
    engine = create_engine(MYSQL_CONN['mysql_uri']
                           .format(user=MYSQL_CONN['user'], pwd=MYSQL_CONN['password'], host=MYSQL_CONN['host'],
                                   db=MYSQL_CONN['db'])
                           , echo=False)
    # connect session to active the action
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def map_orm_item(scrapy_item, sql_item):
    for k, v in scrapy_item.iteritems():
        sql_item.__setattr__(k, v)
    return sql_item


def convert_date(date_str):
    pass


import models


class CnbetaMysqlPipeline(object):
    def __init__(self):
        self.session = models.create_session()

    def process_item(self, item, spider):
        sql_cnbeta = models.cnbeta()
        sql_cnbeta = models.map_orm_item(scrapy_item=item, sql_item=sql_cnbeta)
        self.session.add(sql_cnbeta)
        self.session.commit()
        self.session.close()
        return item