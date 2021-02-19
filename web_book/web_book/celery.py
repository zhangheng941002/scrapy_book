#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/1 10:25
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : celery.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_book.settings')

app = Celery('book')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': settings.CELERY_RESULT_BACKEND,
        'default_timeout': 300
    }
}


platforms.C_FORCE_ROOT = True


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))