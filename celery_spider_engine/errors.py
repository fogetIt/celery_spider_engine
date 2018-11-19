# -*- coding: utf-8 -*-
# @Date:   2018-04-17 15:35:16
# @Last Modified time: 2018-04-17 15:35:18


class HttpMethodUnSupportError(Exception):

    def __init__(self, method: str):
        err = 'http method {} is not support.'.format(method)
        super(HttpMethodUnSupportError, self).__init__(err)


class ImportModuleError(Exception):

    def __init__(self, name: str, package: str):
        err = "can't import {} from {}.".format(name, package)
        super(ImportModuleError, self).__init__(err)


class PythonVersionUnmatchError(EnvironmentError):

    def __init__(self):
        err = 'celery_spider_engine only support python3.'
        super(PythonVersionUnmatchError, self).__init__(err)