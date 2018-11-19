import redis
import importlib
from celery import Celery
from .constants import PY2
from .errors import PythonVersionUnmatchError, ImportModuleError
from .tasks import run_spider

if PY2:
    raise PythonVersionUnmatchError


def start_spider(app: Celery):
    app.autodiscover_tasks(packages=['celery_spider_engine'], related_name='tasks')
    # app.conf.update({'include': 'celery_spider_engine.tasks'})
    """
    params['url']               页面地址
    params['method']='get'      页面请求方式
    params['options']={}        requests options
    params['encoding']='utf-8'  页面编码
    params['level']=''          页面级别
    params['selenium']=False    是否使用谷歌驱动
    params['ext_data']={}       扩展数据
    params['force']=False       是否强制重复爬取
    """
    # 日志文件存储路径
    log_path = str(app.conf.get('SPIDER_LOG_PATH'))
    # redis 判重集合
    spider_redis_host = str(app.conf['SPIDER_REDIS_HOST'])
    spider_redis_port = int(app.conf['SPIDER_REDIS_PORT'])
    spider_redis_db = int(app.conf['SPIDER_REDIS_DB'])
    spider_redis_password = app.conf.get('SPIDER_REDIS_PASSWORD', None)
    # 爬虫执行程序
    spider_mod = app.conf['SPIDER_MOD']
    spider_package = app.conf.get('SPIDER_PACKAGE', None)
    # 数据存储管道
    spider_pipeline_mod = app.conf.get('SPIDER_PIPELINE_MOD')
    spider_pipeline_package = app.conf.get('SPIDER_PIPELINE_PACKAGE')

    try:
        spider = importlib.import_module(spider_mod, spider_package)
    except Exception as e:
        print(e)
        raise ImportModuleError(spider_mod, spider_package)

    for params in spider.start_list:
        run_spider.delay(
            log_path,
            spider_redis_host, spider_redis_port, spider_redis_db, spider_redis_password,
            spider_mod, spider_package,
            spider_pipeline_mod, spider_pipeline_package,
            **params
        )


__all__ = ('start_spider',)
