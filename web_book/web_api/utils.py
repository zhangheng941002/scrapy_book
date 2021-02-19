#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/5 17:45
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : utils.py
# @Software: PyCharm
import datetime
from django.conf import settings


def Bj_date():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=8)


def get_page_limit(page_size, page):
    try:
        page = int(page) if page else 1
        page_size = int(page_size) if page_size else 10
        return (page - 1) * page_size, page_size * page
    except Exception:
        return 1, 10


def page_size_limit(page_size):
    if int(page_size) > settings.PAGE_SIZE_MAX:
        page_size = settings.PAGE_SIZE_MAX
    if int(page_size) < settings.PAGE_SIZE_MIN:
        page_size = settings.PAGE_SIZE_MIN
    return int(page_size)