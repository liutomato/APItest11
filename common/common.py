#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import time
import urllib
import yaml
import urllib3
from lxml import etree
import random
import traceback
from urllib import parse
import jsonpath
import requests
import hx_mysql
import uuid
import os
import jsondiff

urllib3.disable_warnings()


def read_yaml(yaml_path):
    """
    调用函数读取yaml文件
    :return: 返回读取的数据
    """
    with open(yaml_path, "r", encoding="utf-8") as data:
        return yaml.safe_load(data)


# Webhook获取时间戳和签名
def get_timestamp_and_sign():
    timestamp = str(round(time.time() * 1000))
    secret = 'asdfgh'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


# 获取当前格式化后时间
def get_format_time(timestamp=None, style='%Y-%m-%d %H:%M', shift=0):
    if timestamp is None:
        timestamp = int(time.time())
    current_time = time.strftime(style, time.localtime(timestamp + int(shift)))
    return current_time


def get_phone_number(pni=None):
    if pni is None:
        return '1' + ''.join(random.sample('0123456789', 10))
    else:
        return '1' + str(pni) + ''.join(random.sample('0123456789', (10 - len(str(pni)))))


def html_parser(obj, dom):
    """从获取到的html从返回list类型的页面文本
        :param obj: requests请求后返回的Response对象 且response headers=>content-type:text/html
        :param dom: obj的html xpath的值（可以不唯一，即返回多个值）例:dom = '//span[@class="column-orderNumber"]/text()'
        :rtype: list
    """
    tree = etree.HTML(obj.text)
    content = tree.xpath(dom)
    return content


def is_kw_exist(kw, content):
    if isinstance(kw, str):
        is_exist = (kw in content.lower())
        return is_exist
    if isinstance(kw, list) or isinstance(kw, set):
        for i in kw:
            if i in content.lower():
                return True
        return False
    else:
        return 'kw格式不正确'


def get_trace(step):
    method_name = traceback.extract_stack()[-(step+1)][-2]
    return method_name

# 获取函数名中指定位置关键词
def get_single_word(string, index, sep='_'):
    word_list = string.split(sep)
    return word_list[index]


# 运行gocron上定时任务
def exec_gocron_task(task_id):
    url = 'http://112.126.89.234:5920/api/user/login'
    payload = {'username': 'gocron', 'password': 'gocron'}
    session = requests.session()
    res = session.post(url, data=payload)
    token = jsonpath.jsonpath(json.loads(res.text), '$..token')[0]
    base_url = 'http://112.126.89.234:5920/api/task/run/'
    task_url = parse.urljoin(base_url, str(task_id))
    task_header = {'Auth-Token': token}
    task_res = session.get(task_url, headers=task_header)
    print(task_res.text)

# 向测试环境kafka写入数据
def send_kafka_message(topic, message):
    url = 'https://t-api-serverkkkk'
    payload = json.dumps({'topic': topic, 'message': message, 'retry': 1})
    res = requests.post(url, data=payload)
    return res

# 获取指定数量的uid
def get_member_uids(num):
    db = hx_mysql.MysqlUtils()
    sql = f'select uid from pre_ucenter_members where 1=1 ORDER BY uid desc limit {num};'
    db.connect_database('kkkk')
    data = db.get_db_data(sql)
    uid_list = [uid[0] for uid in data]
    db.close_db()
    return uid_list

# 获取随机uuid
def get_uuid():
    data = ''.join(str(uuid.uuid4()).split('-'))
    return data

# 获取指定路径下所有文件名
def get_filename(path):
    file_list = os.listdir(path)
    return file_list

# 比对两个json数据
def compare_json(json1, json2):
    result = jsondiff.diff(json1,json2)
    return result
