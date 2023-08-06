# -*- coding: utf-8 -*-
# @File   : setup.py
# @license: Copyright(C) 2019 FNEP-Tech
# @Author : hansion
# @Date   : 2019-02-16
# @Desc   : 

from setuptools import setup

setup(
    name='cullinan',
    version='0.2.0',
    packages=['cullinan'],
    description='cullinan',
    author='fnep',
    author_email='hansion@fnep-tech.com',
    url='https://www.fnep-tech.com/',
    install_requires=['tornado', 'python-dotenv', 'sqlalchemy', 'pymysql'],
)
