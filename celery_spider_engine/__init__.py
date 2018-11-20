import sys
from celery import Celery
from .single import Single
from .tasks import run_spider
from .utils import object2sequence
from .errors import PythonVersionUnmatchError

PY2 = sys.version_info.major == 2
if PY2:
    raise PythonVersionUnmatchError


def start_spider(app: Celery, spider, pipeline=None):
    app.autodiscover_tasks(packages=['celery_spider_engine'], related_name='tasks')
    # app.conf.update({'include': 'celery_spider_engine.tasks'})
    """
    :param spider:    爬虫执行程序
    :param pipeline:  数据存储管道
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
    spider_redis = (
        str(app.conf['SPIDER_REDIS_HOST']),
        int(app.conf['SPIDER_REDIS_PORT']),
        int(app.conf['SPIDER_REDIS_DB']),
        str(app.conf.get('SPIDER_REDIS_PASSWORD', ''))
    )
    for params in spider.start_list:
        run_spider.delay(
            params.pop('url'),
            params.pop('force', False),
            log_path, *object2sequence(spider), *object2sequence(pipeline), *spider_redis,  # only py3
            **params
        )


__all__ = ('start_spider',)
