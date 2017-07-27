import json
import re
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

