import simplejson
from .logger import logger_facade


class DebugPipeline(object):

    def __init__(self, log_path: str, name: str):
        self.logger = logger_facade(log_path, name + '.pipeline')

    def save(self, result):
        key_id = result.get("key_id", None)
        if key_id:
            self.logger.info(simplejson.dumps(result, ensure_ascii=False))
        else:
            self.logger.error(result)
            raise Exception("key_id is needed when p.put({'key_id':'xxx', ...})")
