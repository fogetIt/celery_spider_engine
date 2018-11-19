import unittest
from celery import Celery
from celery_spider_engine import start_spider

app = Celery('tasks', broker='redis://:redis12315@127.0.0.1:6379/0', backend='redis://:redis12315@127.0.0.1:6379/0')
app.config_from_object({
    'SPIDER_LOG_PATH': 'logs',
    'SPIDER_REDIS_HOST': '127.0.0.1',
    'SPIDER_REDIS_PORT': 6379,
    'SPIDER_REDIS_DB': 0,
    'SPIDER_REDIS_PASSWORD': 'redis12315',
    'SPIDER_MOD': 'spider',
    'SPIDER_PACKAGE': '.'
})


class TestProj(unittest.TestCase):

    def test_engine(self):
        start_spider(app)


if __name__ == '__main__':
    unittest.main()
