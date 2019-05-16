#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: exceptions.py
@time: 2019-01-09

自定义异常

"""


class RequestError(RuntimeError):
    """ 请求时的状态码错误 """

    def __init__(self, *args, **kwargs):
        pass


class ResponseError(RuntimeError):
    """ 得到的response状态错误 """

    def __init__(self, *args, **kwargs):
        pass


class DataError(RuntimeError):
    """ 得到的data中没有预期的内容 """

    def __init__(self, *args, **kwargs):
        pass


class ParameterError(RuntimeError):
    """ 输入的参数错误 """

    def __init__(self, *args, **kwargs):
        pass
