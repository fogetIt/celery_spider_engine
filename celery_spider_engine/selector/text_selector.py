# -*- coding: utf-8 -*-
# @Date:   2018-01-18 10:06:19
# @Last Modified time: 2018-01-30 10:19:03
from .utils import extract_regex


class TextSelector:

    def __init__(self, text=""):
        self._res = []
        self._text = text

    def text(self):
        return self._text

    def text_all(self):
        return [self.text()]

    def smart_text(self):
        return "".join(self.text_all())

    def re(self, regex, index=0):
        list_result = extract_regex(regex, self._text)
        return TextSelector(self._eq_(list_result, index))

    def wildcard(self, pattern, index):
        text = self._text
        if isinstance(text, str):
            text = text.decode("utf-8")
        if isinstance(pattern, str):
            pattern = pattern.decode("utf-8")
        limit = 0
        pars = pattern.split("*")
        res = []
        flag = False
        last = len(pars) - 1
        for pos, p in enumerate(pars):
            group_index = text.find(p)
            if group_index == -1:
                res = []
                break
            if flag:
                sub = text[0: group_index]
                if last == pos and (not p):
                    res.append(text)
                else:
                    res.append(sub)

            text = text[group_index + len(p):]
            flag = True
            if limit > 5:
                break
            limit += 1
        return TextSelector(self._eq_(res, index))

    def _eq_(self, res=(), index=0):
        if index >= 0 and len(res) > index:
            return res[index]
        return ""
