# -*- coding: utf-8 -*-
# @Date:   2018-04-13 18:31:34
# @Last Modified time: 2018-04-13 18:31:45
import os
import socket
import hashlib
from urllib3.util import parse_url, Url


def get_spider_name(spider_obj) -> str:
    return spider_obj.__name__


def get_script_path() -> str:
    return os.getcwd()


def make_hash(string: str) -> str:
    """
    哈希得到固定长度的字符串（减少内存占用）
    """
    u8bytes = string.encode("utf-8")
    return hashlib.sha1(u8bytes).hexdigest()


def get_machine_ip() -> str:  # TODO
    """
    生成本机名
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def correct_url(url: str, refer_url: str='') -> str:
    """
    校正url：
        # => None
        javascript:xxx => None
        /abc.htm => http://xxx/abc.htm
    :param url:
    :param refer_url:
    :return:
    """
    refer_scheme, _, refer_host, refer_port, _, _, _ = parse_url(refer_url)
    refer_scheme = refer_scheme if refer_scheme and refer_scheme.lower() in ['http', 'https'] else None
    scheme, auth, host, port, path, query, fragment = parse_url(url)
    if not host:
        if not path or not refer_host:
            return ''
        else:
            host = refer_host
            port = refer_port
    scheme = scheme or refer_scheme or 'http'
    return Url(scheme=scheme, auth=auth, host=host, port=port, path=path, query=query, fragment=fragment).url
