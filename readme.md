```bash
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

##### 创建代理接口
```python
def create_proxies() -> dict:
    # options.update(create_proxies())
    return {}
```


##### 运行
```bash
celery -A tests worker -l info -c 1
python tests.py
```