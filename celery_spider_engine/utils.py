# -*- coding: utf-8 -*-
# @Date:   2018-04-13 18:31:34
# @Last Modified time: 2018-04-13 18:31:45
import os
import types
import typing
import socket
import hashlib
import importlib
from urllib3.util import parse_url, Url
from .errors import ImportModuleError


def get_script_path() -> str:
    return os.getcwd()


def object2sequence(obj=None) -> typing.Tuple[str, str]:
    if not obj:
        return '', ''
    if not isinstance(obj, types.ModuleType):
        obj_module = obj.__module__
        obj_name = obj.__name__
    else:
        obj_module = obj.__name__
        obj_name = ''
    return obj_name, obj_module


def sequence2object(obj_name: str, obj_module: str):
    if not obj_module:
        return None
    try:
        obj = importlib.import_module(obj_module)
        if obj_name:
            obj = getattr(obj, obj_name)
    except Exception as e:
        print(e)
        raise ImportModuleError(obj_name, obj_module)
    return obj


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
