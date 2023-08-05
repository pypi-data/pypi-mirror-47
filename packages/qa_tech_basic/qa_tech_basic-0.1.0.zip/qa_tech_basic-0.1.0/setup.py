# -*- coding: utf-8 -*-
# author:      hj
# create_time: 2019/5/14 16:12
# update_time: 2019/5/14 16:12
from distutils.core import setup

setup(
    name='qa_tech_basic',  # 对外我们模块的名字
    version='0.1.0',  # 版本号
    description='齐安科技基础包',  # 描述
    author='hj',  # 作者
    author_email='56172032@qq.com',
    # install_requires=['sqlite3', 'Crypto.Cipher.AES'],
    py_modules=['qa_tech_basic.configuration', 'qa_tech_basic.regex_utils', 'qa_tech_basic.time_utils']
)