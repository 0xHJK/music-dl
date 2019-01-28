#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
"""
@author: HJK 
@file: setup.py 
@time: 2019-01-26

打包配置文件

"""
import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'music_dl', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'music-dl = music_dl.__main__:main',
        ],
    },
    install_requires=[
        'requests',
        'click',
        'pycryptodome',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities'
    ],
)