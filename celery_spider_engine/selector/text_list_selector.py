# encoding=utf-8
from .text_selector import TextSelector


class TextListSelector:

    def __init__(self, res=()):
        self._res = res

    def text(self):
        return self._eq_(self._res, 0).text()

    def text_all(self):
        return [r.text() for r in self._res]

    def smart_text(self):
        return "".join(self.text_all())

    def re(self, regex, index=0):
        tmp = []
        for r in self._res:
            tmp.append(r.re(regex, index))
        return TextListSelector(tmp)

    def wildcard(self, pattern, index):
        tmp = []
        for r in self._res:
            tmp.append(r.wildcard(pattern, index))
        return TextListSelector(tmp)

    def _eq_(self, res=(), index=0):
        if index >= 0 or len(res) > index:
            return res[index]
        return TextSelector()
