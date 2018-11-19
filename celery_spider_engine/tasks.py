# coding: utf-8
import os, sys
from celery import shared_task
from .page import Page
from .logger import logger_facade
from .utils import correct_url, get_spider_name, make_hash
from .constants import Single


@shared_task
def run_spider(
        log_path: str,
        spider_redis_host: str, spider_redis_port: int, spider_redis_db: int, spider_redis_password: str,
        spider_mod: str, spider_package: str,
        spider_pipeline_mod: str, spider_pipeline_package: str,
        url: str,
        force: bool=False,
        **kwargs
):
    """
    tasks function arguments must can switch to json
    """
    args = (
        log_path,
        spider_redis_host, spider_redis_port, spider_redis_db, spider_redis_password,
        spider_mod, spider_package,
        spider_pipeline_mod, spider_pipeline_package
    )
    single = Single(*args)
    spider_name = get_spider_name(single.spider)
    unique_set = spider_name + '.unique_set'
    logger = logger_facade(log_path, spider_name + '.task')
    valid_url = correct_url(url)
    if valid_url:
        hashed_valid_url = make_hash(url)
        if not force and single.redis_client.sismember(unique_set, hashed_valid_url):
            logger.error('duplicate url:{}.'.format(url))
            return 'duplicate url:{}.'.format(url)
        single.redis_client.sadd(unique_set, hashed_valid_url)
        page = Page(spider_name, valid_url, *args, **kwargs)
        for result in page.results:
            single.pipeline.save(result)
        single.spider.process(page)
        return 'success'
    else:
        logger.error('invalid url:{}.'.format(url))
        return 'invalid url:{}.'.format(url)
