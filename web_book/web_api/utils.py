#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/5 17:45
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : utils.py
# @Software: PyCharm
import datetime
import hashlib
import os

import requests
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


def getMD5(value):
    md5 = hashlib.md5()
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()


def load_img(url, path):
    name = getMD5(url)
    hz = ".{}".format(url.split(".")[-1])
    file_path = path + name + hz
    if not os.path.exists(file_path):

        resp = requests.get(url).content
        with open(file_path, 'wb') as file:
            file.write(resp)
    else:
        print("文件已经存在了")


if __name__ == '__main__':
    load_img("http://www.iqiwx.com/files/article/image/64/64988/64988s.jpg", "./images/")
