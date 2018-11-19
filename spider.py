start_list = [{'url': 'www.baidu.com'}]


def process(p):
    if p.is_default_level():
        print(p.text)
