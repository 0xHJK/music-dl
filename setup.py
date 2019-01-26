#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
"""
@author: HJK 
@file: setup.py 
@time: 2019-01-26



"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymusic-dl",
    version="2.0.0",
    author="HJK",
    author_email="HJKdev@gmail.com",
    description="Search and download music from netease, qq, kugou, baidu and xiami.",
    long_description=long_description,
    url="https://github.com/0xHJK/music-dl",
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
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Utilities"
    ],
)