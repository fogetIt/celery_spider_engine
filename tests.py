import unittest
from celery import Celery
from celery_spider_engine import start_spider
import spider

app = Celery('tasks', broker='redis://:redis12315@127.0.0.1:6379/0', backend='redis://:redis12315@127.0.0.1:6379/0')
app.config_from_object({
    'SPIDER_LOG_PATH': 'logs',
    'SPIDER_REDIS_HOST': '127.0.0.1',
    'SPIDER_REDIS_PORT': 6379,
    'SPIDER_REDIS_DB': 0,
    'SPIDER_REDIS_PASSWORD': 'redis12315',
})


class Spider(object):
    start_list = [{'url': 'www.baidu.com', 'force': True}]

    @staticmethod
    def process(p):
        if p.is_default_level():
            p.add_task('www.baidu.com', force=True)


class TestProj(unittest.TestCase):

    def test_engine(self):
        # start_spider(app, spider)
        start_spider(app, Spider)


if __name__ == '__main__':
    unittest.main()
