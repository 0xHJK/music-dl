#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: test_config
@time: 2019-01-30
"""
import pytest
from music_dl import config


def test_init():
    # with pytest.raises(AttributeError):
    #     config.opts
    config.init()
    assert config.opts


def test_get():
    config.init()
    assert config.get("number") == 5
    assert config.get("outdir") == "."
    assert config.get("fasdfjklasd") == ""


def test_set():
    config.init()
    assert config.get("fasdfjklasd") == ""
    config.set("fasdfjklasd", "music-dl")
    assert config.get("fasdfjklasd") == "music-dl"
    proxies = {"http": "http://127.0.0.1:1087", "https": "http://127.0.0.1:1087"}
    config.set("proxies", proxies)
    assert config.get("proxies")["http"] == "http://127.0.0.1:1087"
    assert config.get("proxies")["https"] == "http://127.0.0.1:1087"
