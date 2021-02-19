#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/7/7 14:11
# @Author : Zh
# @Project : monitor_center
# @File   : tasks.py
# @Software: PyCharm

from __future__ import absolute_import
import datetime

from celery import shared_task
from rediscluster import RedisCluster
import redis
from django.conf import settings
import json
from .models import *
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
def handle_monitor():
    print('-------------------- handle_monitor ---------------', datetime.datetime.now(), '-------------', )

    radius_redis_session = "session"
    radius_redis_user = "user"

    # 1 读取在线session信息
    radius_redis_cluster = RedisCluster(startup_nodes=settings.REDIS_CLUSTER_NODES, decode_responses=True,
                                        password=settings.REDIS_CLUSTER_PASSWORD)
    _flag = {}

    get_cpe_info_task_flag = ConsoleCode.objects.filter(table="get_cpe_info_task",
                                                        parent__table='monitor_center_config',
                                                        status=0).exists()
    get_cpe_ping_task_flag = ConsoleCode.objects.filter(table="get_cpe_ping_task",
                                                        parent__table='monitor_center_config',
                                                        status=0).exists()
    get_cpe_monitor_task_flag = ConsoleCode.objects.filter(table="get_cpe_monitor_task",
                                                           parent__table='monitor_center_config',
                                                           status=0).exists()

    for key in radius_redis_cluster.hkeys(radius_redis_session):
        try:
            session_data = json.loads(radius_redis_cluster.hget(radius_redis_session, key))
            user_name = session_data.get("user_name")

            # if user_name.startswith("4230"):
            #     continue
            if user_name.startswith("424") or user_name.startswith("425"):
                pass
            else:
                print(f'------------- delete username:{user_name}----------------')
                continue
            user_info = json.loads(radius_redis_cluster.hget(radius_redis_user, user_name))
            user_attrs = json.loads(user_info.get("attrs"))
            cpe_ip = None
            for attr in user_attrs:
                attr_name = attr.get("attr_name")
                if attr_name == "Framed-IP-Address":
                    cpe_ip = attr.get("attr_value")
            if not cpe_ip:
                continue
            if cpe_ip.startswith("10.188"):
                continue
            sn = "csn-{}".format(replace_char(user_name, "0", 3))
            if sn[6:7] not in ['1', '2', '3']:
                sn = replace_char(sn, "3", 6)
            if _flag.get(sn, None) and _flag.get(sn).get("ip").startswith("10.202"):
                continue
            sdw = SdwModel.objects.get(sn=sn)
            _data = sdw.auth.get("api")
            _data['ip'] = cpe_ip
            # _data['ip'] = sdw.ip.get("contrl")
            _data['port'] = settings.CPE_REQUEST_PORT
            _data['sn'] = sn
            _data['time_out'] = settings.CPE_REQUEST_TIMEOUT
            print('=====================', _data)

            _flag[sn] = _data

        except:
            print('----------------- handle monitor error ---------------', traceback.format_exc())

    # 调用异步任务
    """
    默认是都开启的，当只有在console_code_info表中status改为不是0时，则不在收集数据
    """

    return True




import requests

for i in range(50000):
    requests.get("http://172.30.11.47:8090/task/handle/")