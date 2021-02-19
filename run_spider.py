#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/20 18:20
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : run_spider.py
# @Software: PyCharm

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl bookSpider".split())