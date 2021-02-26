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

# ----------------------------------------- mysql 配置 -----------------------------------------

MYSQL_HOST = os.environ.get('MYSQL_HOST') if os.environ.get('MYSQL_HOST') != None else "book_mysql"
MYSQL_USER = os.environ.get('MYSQL_USER') if os.environ.get('MYSQL_USER') != None else "root"
MYSQL_PWD = os.environ.get('MYSQL_PWD') if os.environ.get('MYSQL_PWD') != None else "123456"
MYSQL_DB = os.environ.get('MYSQL_DB') if os.environ.get('MYSQL_DB') != None else "iqiwx"
MYSQL_PORT = os.environ.get('MYSQL_PORT') if os.environ.get('MYSQL_PORT') != None else "3306"

# ----------------------------------------- mysql 配置 -----------------------------------------


iqiwx = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': MYSQL_DB,
    'USER': MYSQL_USER,
    'HOST': MYSQL_HOST,
    'PORT': MYSQL_PORT,
    'PASSWORD': MYSQL_PWD,
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

# ----------------------------------------- redis 配置 -----------------------------------------

REDIS_HOST = os.environ.get('MYSQL_HOST') if os.environ.get('REDIS_HOST') != None else "book_redis"
REDIS_PWD = os.environ.get('MYSQL_PWD') if os.environ.get('REDIS_PWD') != None else "123456"
REDIS_DB = os.environ.get('MYSQL_DB') if os.environ.get('REDIS_DB') != None else "0"
REDIS_PORT = os.environ.get('MYSQL_PORT') if os.environ.get('REDIS_PORT') != None else "6379"

# ----------------------------------------- redis 配置 -----------------------------------------


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
        "LOCATION": "redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}".format(REDIS_HOST=REDIS_HOST, REDIS_PORT=REDIS_PORT,
                                                                          REDIS_DB=REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",  # 压缩，默认是关闭的
            "PASSWORD": REDIS_PWD,  # redis 密码
            "CONNECTION_POOL_KWARGS": {"decode_responses": True, "max_connections": 100},
        }
    }
}

# log日志格式
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
IS_LOAD_IMAGE = False

# celery 配置
CELERY_BROKER_URL = 'redis://:{REDIS_PWD}@{REDIS_HOST}:{REDIS_PORT}/8'.format(REDIS_HOST=REDIS_HOST,
                                                                              REDIS_PORT=REDIS_PORT,
                                                                              REDIS_PWD=REDIS_PWD)
CELERY_RESULT_BACKEND = 'redis://:{REDIS_PWD}@{REDIS_HOST}:{REDIS_PORT}/9'.format(REDIS_HOST=REDIS_HOST,
                                                                                  REDIS_PORT=REDIS_PORT,
                                                                                  REDIS_PWD=REDIS_PWD)
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
CELERY_TIMEZONE = 'Asia/Shanghai'
