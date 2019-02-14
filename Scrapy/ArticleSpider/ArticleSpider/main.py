#!/usr/bin/env python3
# coding=utf-8

from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
print(os.path.abspath(os.path.dirname(__file__)))

execute(['scrapy','crawl','jobbole'])
# execute(['scrapy','crawl','zhihu'])