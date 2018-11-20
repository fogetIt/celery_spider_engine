import sys
import redis
from .pipeline import DebugPipeline
from .utils import sequence2object, get_script_path
sys.path.append(get_script_path())


class Single(object):

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Single, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            log_path: str,
            spider_name: str, spider_module: str,
            pipeline_name: str, pipeline_module: str,
            spider_redis_host: str, spider_redis_port: int, spider_redis_db: int, spider_redis_password: str,
    ):
        self.spider = sequence2object(spider_name, spider_module)
        self.name = self.spider.__name__
        self.log_path = log_path
        self.pipeline = sequence2object(pipeline_name, pipeline_module) or DebugPipeline(log_path, self.name)
        self.redis_client = redis.StrictRedis(
            host=spider_redis_host,
            port=spider_redis_port,
            db=spider_redis_db,
            password=spider_redis_password
        )
