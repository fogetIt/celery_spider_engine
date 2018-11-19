from setuptools import setup, find_packages

setup(
    name="celery_spider_engine",
    version="0.0.1",
    author="forgetIt",
    author_email="2271404280@qq.com",

    url="https://github.com/fogetIt/celery_spider_engine",
    description="spider in celery",
    long_description="run spider in celery",
    keywords=("spider", "celery", "engine"),
    license="MIT Licence",

    packages=find_packages(),
    include_package_data=False,
    platforms="any",
    install_requires=[
        'celery==4.2.1',
        'gevent==1.3.7',
        'requests===2.19.1',
        'redis==2.10.6',
        'selenium==3.141.0',
        'pyvirtualdisplay==0.2.1',
        'lxml==4.2.5',
        'parsel==1.5.0',
        'simplejson==3.16.0',
        'jsonpath-rw==1.4.0'
    ],
)
