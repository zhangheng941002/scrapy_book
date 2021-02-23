#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/1 10:25
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : urls.py
# @Software: PyCharm

from rest_framework import routers
from django.conf.urls import url

from .views import *

router = routers.DefaultRouter(trailing_slash=False)


router.register(r'book', BookAllInfoViewSet, base_name='book')
# router.register(r'test', Test, base_name='test')

urlpatterns = router.urls

urlpatterns.append(url(r'book_type/', book_type))  # 分类
urlpatterns.append(url(r'book_type_info/', book_info))  # 分类下书的信息
urlpatterns.append(url(r'book_chapter/', book_chapter))  # 章节列表
urlpatterns.append(url(r'chapter_content/', chapter_content))  # 章节内容

urlpatterns.append(url(r'search/', search))  # 根据作者名或者书名模糊搜索



