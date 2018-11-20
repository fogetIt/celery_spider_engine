import traceback
import requests
import simplejson
from typing import Callable
from selenium import webdriver
from pyvirtualdisplay import Display
from .logger import logger_facade
from .errors import HttpMethodUnSupportError
from .selector import HtmlSelector, JsonSelector, TextSelector


class RequestParams(object):

    def __init__(
            self,
            url: str,
            method: str = 'get',
            options: dict = None,
            encoding: str = 'utf-8',
            level: str = '',
            selenium: bool = False,
            ext_data: dict = None
    ):
        self.url = url
        self.method = method.lower()
        self.options = options if options else {}
        self.encoding = encoding
        self.level = level
        self.selenium = selenium
        self.ext_data = ext_data if ext_data else {}
        self.__retry_num = 0

    def is_default_level(self) -> bool:
        return self.is_level('')

    def is_level(self, level: str) -> bool:
        return self.level == level

    def put_ext(self, key: str, value):
        self.ext_data[key] = value

    def get_ext(self, key: str):
        return self.ext_data.get(key, '')


class Handler(object):

    @staticmethod
    def todo(method: str) -> Callable:
        return getattr(Handler, method, None)

    @staticmethod
    def options(response) -> dict:
        """
        requests 模块的 options 与 http 协议中的 options，并不完全一致
        """
        kwargs = response.options or {}
        kwargs.update({
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            },
            'timeout': 60,
        })
        return kwargs

    @staticmethod
    def get(response):
        options = Handler.options(response)
        if response.selenium:
            with Display(backend='xvfb', size=(1440, 900)):
                browser = webdriver.Chrome()
                browser.get(response.url)
                browser.close()  # 关闭当前窗口
                # browser.quit()  # 关闭所有窗口，退出驱动
                response.status_code, response.text = 200, browser.page_source
        else:
            resp = requests.get(response.url, params=response.ext_data.get('params'), **options)
            resp.encoding = response.encoding
            response.status_code, response.text = resp.status_code, resp.text

    @staticmethod
    def post(response):
        options = Handler.options(response)
        resp = requests.post(
            response.url,
            data=response.ext_data.get('data'),
            json=simplejson.dumps(response.ext_data.get('json')),
            **options
        )
        resp.encoding = response.encoding
        response.status_code, response.text = resp.status_code, resp.text


class Response(RequestParams):

    def __init__(self, url: str, log_path: str, name: str, **kwargs):
        self.logger = logger_facade(log_path, name + '.response')
        self.status_code = None
        self.text = None
        super(Response, self).__init__(url, **kwargs)
        self.__retry()

    def __retry(self):
        handle = Handler.todo(self.method)
        if handle:
            try:
                handle(self)
            except Exception as e:
                print(e)
                self.__retry_num += 1
                if self.__retry_num < 3:
                    self.__retry()
                else:
                    self.logger.error(traceback.format_exc())
        else:
            raise HttpMethodUnSupportError(self.method)


class Page(Response):

    def __init__(self, valid_url: str, log_path: str, name: str, *args, **kwargs):
        self.results = []
        self.__html_selector = None
        self.__text_selector = None
        self.__json_selector = None
        super(Page, self).__init__(valid_url, log_path, name, **kwargs)
        self.__args = args

    def html_selector(self, text=None):
        if text:
            return HtmlSelector(text=text)
        else:
            if not self.__html_selector:
                self.__html_selector = HtmlSelector(text=self.text)
            return self.__html_selector

    def text_selector(self, text=None):
        if text:
            return TextSelector(text=text)
        else:
            if not self.__text_selector:
                self.__text_selector = TextSelector(text=self.text)
            return self.__text_selector

    def json_selector(self, text=None):
        if text:
            return JsonSelector(text=text)
        else:
            if not self.__json_selector:
                self.__json_selector = JsonSelector(text=self.text)
            return self.__json_selector

    def put(self, arg: dict):
        if isinstance(arg, dict):
            self.results.append(arg)
        else:
            self.logger.error(arg)
            raise Exception("arg must is dict, example: page.put('key_id':'xxx', ...)")

    def add_task(self, url: str, force: bool=False, **kwargs):
        from .tasks import run_spider
        run_spider.delay(url, force, *self.__args, **kwargs)
