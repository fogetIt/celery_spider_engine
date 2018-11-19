import sys
import redis
import importlib
from .errors import ImportModuleError
from .utils import get_spider_name, get_script_path

PY2 = sys.version_info.major == 2
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
            spider_redis_host: str, spider_redis_port: int, spider_redis_db: int, spider_redis_password: str,
            spider_mod: str, spider_package: str,
            spider_pipeline_mod: str, spider_pipeline_package: str,
    ):
        self.redis_client = redis.StrictRedis(
            host=spider_redis_host,
            port=spider_redis_port,
            db=spider_redis_db,
            password=spider_redis_password
        )
        try:
            self.spider = importlib.import_module(spider_mod, spider_package)
        except Exception as e:
            print(e)
            raise ImportModuleError(spider_mod, spider_package)
        if spider_pipeline_mod and spider_pipeline_package:
            try:
                self.pipeline = importlib.import_module(spider_pipeline_mod, spider_pipeline_package)()
            except Exception as e:
                print(e)
                raise ImportModuleError(spider_pipeline_mod, spider_pipeline_package)
        else:
            from .pipeline import DebugPipeline
            self.pipeline = DebugPipeline(log_path, get_spider_name(self.spider))
