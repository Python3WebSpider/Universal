import json
import re
import time


# 如果需要扩展，可自行添加

def list2str(list):
    """
    列表拼合成字符串
    :param result: 列表
    :return: 字符串
    """
    return ''.join(list)


def unescape(string):
    """
    转义还原
    :param string: 被转义字符
    :return: 原字符
    """
    return re.sub('\\\\', '\\', string)


def date_transform(datetime, format_from, format_to):
    """
    时间格式转换
    :param datetime: 当前时间
    :param format_from: 当前时间格式
    :param format_to: 转后时间格式
    :return: 转后时间
    """
    if not datetime:
        return datetime
    timestamp = time.mktime(time.strptime(datetime, format_from))
    return time.strftime(format_to, time.localtime(timestamp))

def set_value(obj, value):
    """
    设置固定数值
    :param value: 数值
    :return: 数值
    """
    return value

def get_attr(obj, attr):
    """
    获取属性
    :param obj: 对象
    :param attr: 属性
    :return: 属性值
    """
    return getattr(obj, attr)

def get_time(obj, format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间
    :param obj: 对象
    :param format: 格式
    :return: 格式化后时间
    """
    return time.strftime(format, time.localtime(time.time()))
