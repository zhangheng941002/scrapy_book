#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2021/2/1 10:34
# @Author : Zh
# @Email : zhangheng9394@163.com
# @Project : scrapy_book
# @File   : prod.py
# @Software: PyCharm

from .settings import *

ALLOWED_HOSTS = ["*", ]

DATABASE_ROUTERS = [
    'web_book.database_router.DatabaseAppsRouter'
]
DATABASE_APPS_MAPPING = {
    'iqiwx': 'iqiwx'
}

INSTALLED_APPS += [
    # install app
    "rest_framework",
    "django_filters",

    # my app
    "web_api",
    "scheduled_tasks"
]

iqiwx = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'iqiwx',
    'USER': 'root',
    'HOST': '172.30.11.47',
    'PORT': '3306',
    'PASSWORD': 'mariadb',
    'CHARSET': 'UTF8'
}

DATABASES["iqiwx"] = iqiwx

# http://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'web_book.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20
}

MIDDLEWARE_CLASSES = (
    "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "CACHE_MIDDLEWARE_SECONDS=10",  # 以秒为单位,缓存事件
    "django.middleware.cache.FetchFromCacheMiddleware",
)

# 配置两个缓存，默认的及redis
CACHES = {
    # django-redis默认进入的cache缓存
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    },
    # 配置的redis缓存
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://:123456@172.30.11.47:6379/0",
        "LOCATION": "redis://172.30.11.47:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "123456",
            "CONNECTION_POOL_KWARGS": {"decode_responses": True, "max_connections": 100},
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# 每页多大/最少限制
PAGE_SIZE_MAX = 200
PAGE_SIZE_MIN = 1

# images 存储路径
IMAGE_PATH = "./images/"
# 是否开启下载书封面背景，True/False(下载/不下载)
IS_LOAD_IMAGE = True