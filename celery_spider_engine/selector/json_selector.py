# encoding=utf-8
import simplejson as json
from jsonpath_rw import parse
from .text_selector import TextSelector


class JsonSelector:

    def __init__(self, text=""):

        self._text = text
        try:
            self._json = json.loads(text)
        except:
            self._json = {}

    def text(self):
        return self._text

    def text_all(self):
        return [self.text()]

    def smart_text(self):
        return "".join(self.text_all())

    def re(self, regex, index=0):
        return TextSelector(self.text()).re(regex, index)

    def wildcard(self, pattern, index):
        return TextSelector(self.text()).wildcard(pattern, index)

    def json_path(self, expr):
        try:
            parser = parse(expr)
            res = parser.find(self._json)
            for r in res:
                return JsonSelector(r.value)
            return ""
        except:
            return JsonSelector("")
