#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2020/7/7 14:11
# @Author : Zh
# @Project : monitor_center
# @File   : tasks.py
# @Software: PyCharm

from __future__ import absolute_import
import datetime
from celery_once import QueueOnce
from monitor_center.celery import app
from async_tasks.tasks import *
from celery import shared_task
from rediscluster import RedisCluster
import redis
from django.conf import settings
import json
from .models import SdwModel, ConsoleCode, PopListModel, LiveLineModel
import traceback


# @app.task(base=QueueOnce, once={'graceful': True, 'timeout': 60})
@shared_task
def report(x, y):
    print('-------------------- report ---------------', datetime.datetime.now(), '-------------', x + y)

    task_a.delay(10, 11)
    return True


def replace_char(string, char, index):
    string = list(string)
    string[index] = char
    return ''.join(string)


def get_cpe_info_task_apply_async(get_cpe_info_task_data):
    _resp = get_cpe_info_task.apply_async(
        kwargs={"auths": get_cpe_info_task_data},
        queue="get_cpe_info_task")
    # get_cpe_info_task_data.clear()


def get_cpe_ping_task_apply_async(get_cpe_ping_task_data):
    _resp = get_cpe_ping_task.apply_async(
        kwargs={"auths": get_cpe_ping_task_data},
        queue="get_cpe_ping_task")
    # get_cpe_ping_task_data.clear()


def get_cpe_monitor_task_apply_async(get_cpe_monitor_tas_data):
    _resp = get_cpe_monitor_task.apply_async(
        kwargs={"auths": get_cpe_monitor_tas_data},
        queue="get_cpe_monitor_task")
    # get_cpe_monitor_tas_data.clear()


def get_wireless_status_monitor_task_apply_async(get_cpe_monitor_tas_data):
    _resp = get_device_wireless_status_monitor_task.apply_async(
        kwargs={"auths": get_cpe_monitor_tas_data},
        queue="get_device_wireless_status_monitor_task")


def get_pop_ping_pop_monitor_task_apply_async(get_pop_data):
    _res9p = get_pop_ping_pop_monitor_task.apply_async(
        kwargs={"tasks": get_pop_data},
        queue="get_pop_ping_pop_monitor_task")


def get_pop_ping_line_monitor_task_apply_async(get_pop_data):
    _resp = get_pop_ping_line_monitor_task.apply_async(
        kwargs={"tasks": get_pop_data},
        queue="get_pop_ping_line_monitor_task")


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
    for _k, _v in _flag.items():
        if get_cpe_info_task_flag:
            get_cpe_info_task_apply_async(_v)
        if get_cpe_ping_task_flag:
            get_cpe_ping_task_apply_async(_v)
        if get_cpe_monitor_task_flag:
            get_cpe_monitor_task_apply_async(_v)
    return True


@shared_task(ignore_result=True)
def handle_pop_monitor():
    print('===============================get pop ping monitor================')
    pop_list = PopListModel.objects.filter(type=0, status=2).order_by('id').values('id', 'ip', 'area', 'auth', 'extend')
    pop_list_native = pop_list.filter(extend__contains={"foreign": 0})
    pop_list_foreign = pop_list.filter(extend__contains={"foreign": 1})
    pop_pop_infos = []
    for i, pop_src in enumerate(list(pop_list_native)):
        for pop_dest in list(pop_list_native)[i + 1:]:
            passward = pop_src.get('auth').get('api').get('password')
            username = pop_src.get('auth').get('api').get('username')
            auth = {'port': settings.CPE_REQUEST_PORT, 'time_out': settings.CPE_REQUEST_TIMEOUT,
                    'password': passward, 'username': username, 'ip': pop_src.get('ip')}
            pop_info = {'auth': auth, 'pop_src': pop_src.get('ip'),
                        'pop_dst': pop_dest.get('ip'),
                        'area': '{}-{}'.format(pop_src.get('area'), pop_dest.get('area'))}
            pop_pop_infos.append(pop_info)
        for pop_dest in list(pop_list_foreign):
            passward = pop_src.get('auth').get('api').get('password')
            username = pop_src.get('auth').get('api').get('username')
            auth = {'port': settings.CPE_REQUEST_PORT, 'time_out': settings.CPE_REQUEST_TIMEOUT,
                    'password': passward, 'username': username, 'ip': pop_src.get('ip')}
            pop_info = {'auth': auth, 'pop_src': pop_src.get('ip'),
                        'pop_dst': pop_dest.get('ip'),
                        'area': '{}-{}'.format(pop_src.get('area'), pop_dest.get('area'))}
            pop_pop_infos.append(pop_info)
    print(pop_pop_infos)

    # pop_list = PopListModel.objects.filter(type=0, status=2).order_by('id').values('id', 'ip', 'area', 'auth', 'extend')
    pop_list_native = pop_list.filter(extend__contains={"foreign": 0})
    # pop_list_foreign = pop_list.filter(extend__contains={"foreign": 1})

    live_lines = LiveLineModel.objects.filter().values('intranet_ip', 'line')
    pop_line_info = []
    for i, pop_src in enumerate(list(pop_list_native)):
        for pop_dest in list(live_lines):
            passward = pop_src.get('auth').get('api').get('password')
            username = pop_src.get('auth').get('api').get('username')
            auth = {'port': settings.CPE_REQUEST_PORT, 'time_out': settings.CPE_REQUEST_TIMEOUT,
                    'password': passward, 'username': username, 'ip': pop_src.get('ip')}
            pop_info = {'auth': auth, 'pop_src': pop_src.get('ip'),
                        'pop_dst': pop_dest.get('intranet_ip'),
                        'area': '{}-{}'.format(pop_src.get('area'), pop_dest.get('line'))}
            pop_line_info.append(pop_info)
    print(pop_line_info)

    get_pop_ping_pop_flag = ConsoleCode.objects.filter(table="get_pop_ping_pop_task",
                                                       parent__table='monitor_center_config',
                                                       status=0).exists()

    get_pop_ping_line_flag = ConsoleCode.objects.filter(table="get_pop_ping_line_task",
                                                        parent__table='monitor_center_config',
                                                        status=0).exists()

    if get_pop_ping_pop_flag:
        for task in pop_pop_infos:
            get_pop_ping_pop_monitor_task_apply_async(task)

    if get_pop_ping_line_flag:
        for task in pop_line_info:
            get_pop_ping_line_monitor_task_apply_async(task)
    return True


@shared_task(ignore_result=True)
def four_g_monitor():
    # 4G网卡监控
    print('-------------------- 4G interface monitor ---------------', datetime.datetime.now(), '-------------', )

    get_four_g_task = ConsoleCode.objects.filter(table="get_four_g_task",
                                                 parent__table='monitor_center_config',
                                                 status=0).exists()

    # 调用异步任务
    """
    默认是都开启的，当只有在console_code_info表中status改为不是0时，则不在收集数据
    """
    if not get_four_g_task:
        print('------------- 获取4G网卡监控任务关闭，不在操作 --------------')
        return True
    radius_redis_session = "session"
    radius_redis_user = "user"

    # 1 读取在线session信息
    radius_redis_cluster = RedisCluster(startup_nodes=settings.REDIS_CLUSTER_NODES, decode_responses=True,
                                        password=settings.REDIS_CLUSTER_PASSWORD)
    _flag = {}
    four_flag = {}

    for key in radius_redis_cluster.hkeys(radius_redis_session):
        try:
            session_data = json.loads(radius_redis_cluster.hget(radius_redis_session, key))
            user_name = session_data.get("user_name")

            user_info = json.loads(radius_redis_cluster.hget(radius_redis_user, user_name))
            user_attrs = json.loads(user_info.get("attrs"))
            cpe_ip = None
            for attr in user_attrs:
                attr_name = attr.get("attr_name")
                if attr_name == "Framed-IP-Address":
                    cpe_ip = attr.get("attr_value")
            if not cpe_ip:
                continue

            sn = "csn-{}".format(replace_char(user_name, "0", 3))
            if sn[6:7] not in ['1', '2', '3']:
                sn = replace_char(sn, "3", 6)
            if _flag.get(sn, None) and _flag.get(sn).get("ip").startswith("10.202"):
                continue
            sdw = SdwModel.objects.get(sn=sn)
            _data = sdw.auth.get("api")
            control_ip = sdw.ip.get("contrl")

            _data['port'] = settings.CPE_REQUEST_PORT
            _data['sn'] = sn
            _data['time_out'] = settings.CPE_REQUEST_TIMEOUT
            print('=====================', _data)
            if user_name.startswith("4230"):
                if not _flag.get(sn, None):
                    _data['ip'] = control_ip
                    four_flag[sn] = _data
            else:
                _data['ip'] = cpe_ip
                _flag[sn] = _data

        except:
            print('----------------- handle monitor error ---------------', traceback.format_exc())

    for k, v in four_flag.items():
        if not _flag.get(k, None):
            _flag[k] = v

    for _k, _v in _flag.items():
        get_wireless_status_monitor_task_apply_async(_v)

    return True
