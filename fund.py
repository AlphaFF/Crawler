#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: wangfeng1
# @Date:   2019-03-27 19:59:29
# @Email: liushahedi@gmail.com
# @Last Modified by:   wangfeng1
# @Last Modified time: 2019-04-09 11:10:56

import json
import requests
import pymysql
from datetime import datetime, timedelta
import pandas as pd
import time
import re
from lxml import etree

# conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='test', charset='utf8')
# cursor = conn.cursor()

# sql = 'select price from funds;'
# df = pd.read_sql(sql, conn)
# # print(df.values.mean(), df.values.std(), df.values.var())
# print(df.describe())


ts = []
prices = []
current_price = ''


def get_fund_dataframe(code, name, page=1):
    # print(code, name)
    headers = {
        'Host': 'fund.eastmoney.com',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Upgrade-Insecure-Requests': '1',
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6'
    }
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={}&page={}&per=20&sdate=&edate=&rt=0.7823397557719116'.format(code, page)
    print(url)
    res = requests.get(url, headers=headers).text
    # print(res)
    content = re.findall(r'<table.*table>', res)[0]
    # print(content)
    html = etree.HTML(content)
    dwjz = html.xpath('//tr')
    for _ in dwjz[1:]:
        t = _.xpath('./td[1]/text()')[0]
        d = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        p = _.xpath('./td[2]/text()')[0]
        if t == d:
            global current_price
            current_price = p
            print(current_price)
        # print(t, p)
        # print(type(t), type(p))
        ts.append(t)
        prices.append(float(p))
        if datetime.strptime(t, '%Y-%m-%d') < datetime.strptime('20150101', '%Y%m%d'):
            break
    pages = re.findall(r',pages:(\d+),', res)[0]
    # print(pages)
    if page < int(pages):
        page += 1
        time.sleep(1)
        get_fund_dataframe(code, name, page)

# f = []
#     print('====page {}===='.format(page))
# if res.get('ErrCode'):
#     print('数据请求失败.')
#     return
#     for i in res.get('Data').get('LSJZList'):
#         # print(i.get('FSRQ'), i.get('DWJZ'))
#         if i.get('DWJZ'):
#             funds.append(i.get('DWJZ'))
# print('100032', pd.Series(funds).describe())
# d = datetime.strptime(i.get('FSRQ'), '%Y-%m-%d').date()
# day, weekday, price = d, d.weekday() + 1, i.get('DWJZ')
#         print(day, weekday, price)
#         sql = 'insert into funds (day, weekday, price) values (%s, %s, %s);'
#         cursor.execute(sql, (day, weekday, price))
# conn.commit()
# cursor.close()
# conn.close()


funds = {
    # '100032': '富国中证红利指数增强',
    # '100038': '富国沪深300指数增强',
    # '161017': '富国中证500指数增强',
    # '110003': '易方达上证50指数A',
    # '000478': '建信中证500指数增强A',
    # '000311': '景顺长城沪深300增强',
    # '163406': '兴全合润分级混合',
    # '163407': '兴全沪深300指数增强',
    # '000961': '天弘沪深300指数A',
    '002086': 'abcd'
    # '001550': '天弘中证医药100A'
}

for k, v in funds.items():
    get_fund_dataframe(k, v)


dataFrame = pd.DataFrame({
    # 'day': pd.Series(ts),
    'price': pd.Series(prices)
})
print(current_price, dataFrame.mean().values[0], dataFrame.max().values[0], dataFrame.min().values[0], dataFrame.std().values[0])

# get_fund_dataframe('100032', 'afdsa', 52)

"""
20190402
富国中证红利指数增强 1.1920 1.3276303921568628 2.424 0.935 0.29837930174750377
天弘沪深300指数A 1.1852 1.0525030392156862 1.5301 0.8209 0.12370963986553705
兴全沪深300指数增强 1.9472 1.5205557843137254 1.9908 1.0891 0.21904557019320992
富国沪深300指数增强 1.7850 1.5555764705882353 2.014 1.189 0.19413448247759615
景顺长城沪深300增强 2.0910 1.8829382352941175 2.453 1.408 0.20690107317575523
兴全合润分级混合 1.4387 1.5441560784313728 3.1416 0.9938 0.627206249399575
易方达上证50指数A 1.6210 1.1823439215686276 1.621 0.8371 0.19126291512207697
天弘中证500指数A 0.9705 1.024550588235294 1.9336 0.686 0.19076661634912556
富国中证500指数增强 1.9660 2.0112500000000004 3.134 1.419 0.2661402178447766
建信中证500指数增强A 2.1900 2.122987254901961 3.0983 1.4827 0.2850331563350441
"""
