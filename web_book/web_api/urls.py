# -*- coding:utf-8 -*-
from rest_framework import routers
from django.conf.urls import url

from .views import *

router = routers.DefaultRouter(trailing_slash=False)

# router.register(r'test', Test, base_name='test')

urlpatterns = router.urls

urlpatterns.append(url(r'add_task_a/', add_task_a))
urlpatterns.append(url(r'add_task_b/', add_task_b))
urlpatterns.append(url(r'get/ping', get_ping))
urlpatterns.append(url(r'get/resource', get_resource))
urlpatterns.append(url(r'get/monitor', get_monitor))
urlpatterns.append(url(r'get/wireless/monitor', get_wireless_monitor))
urlpatterns.append(url(r'get/pop/ping/pop', get_pop_ping_pop_monitor))
urlpatterns.append(url(r'get/pop/ping/line', get_pop_ping_line_monitor))
