#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/7/7 14:11
# @Author : Zh
# @Project : monitor_center
# @File   : tasks.py
# @Software: PyCharm

from __future__ import absolute_import
import datetime
from django_redis import get_redis_connection
from celery import shared_task
from django.conf import settings
import json
from web_api.models import BookChapterModel
from web_api.serializers import BookChapterSerializer

import traceback


# @app.task(base=QueueOnce, once={'graceful': True, 'timeout': 60})
@shared_task
def report(x, y):
    print('-------------------- report ---------------', datetime.datetime.now(), '-------------', x + y)

    # task_a.delay(10, 11)
    return True


def replace_char(string, char, index):
    string = list(string)
    string[index] = char
    return ''.join(string)


@shared_task(ignore_result=True)
def add_chapter_list(book_id):
    print('-------------------- add_chapter_list ---------------', datetime.datetime.now(),
          '------------- book_id-------------', book_id)

    redis = get_redis_connection("redis")
    chapter = BookChapterModel.objects.filter(book_id=book_id).order_by("num")
    redis.hset("book_chapter_list", book_id,
                  json.dumps({"list": BookChapterSerializer(chapter, many=True).data, "counts": chapter.count()},
                             ensure_ascii=False))

    return True
