# coding: utf-8
from celery import shared_task
from .page import Page
from .logger import logger_facade
from .utils import correct_url, make_hash
from .single import Single


@shared_task
def run_spider(url: str, force: bool=False, *args, **kwargs):
    """
    tasks function arguments must can switch to json
    """
    single = Single(*args)
    name = single.name
    log_path = single.log_path
    unique_set = name + '.unique_set'
    logger = logger_facade(log_path, name + '.task')
    valid_url = correct_url(url)
    if valid_url:
        hashed_valid_url = make_hash(url)
        if not force and single.redis_client.sismember(unique_set, hashed_valid_url):
            logger.error('duplicate url:{}.'.format(url))
            return 'duplicate url:{}.'.format(url)
        single.redis_client.sadd(unique_set, hashed_valid_url)
        page = Page(valid_url, log_path, name, *args, **kwargs)
        for result in page.results:
            single.pipeline.save(result)
        single.spider.process(page)
        return 'success'
    else:
        logger.error('invalid url:{}.'.format(url))
        return 'invalid url:{}.'.format(url)
