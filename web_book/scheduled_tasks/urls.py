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

urlpatterns.append(url(r'handle/', handle_book_all_info))



