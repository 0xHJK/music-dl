#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: netease.py
@time: 2019-01-11

网易云音乐下载

"""

import binascii
import json
import requests
from Crypto.Cipher import AES
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["netease_search", "netease_download"]


def netease_search(keyword) -> list:
    """ 从网易云音乐搜索 """
    count = config.get("count") or 5
    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": keyword, "type": 1, "offset": 0, "limit": count},
    }
    data = {"eparams": encode_netease_data(eparams)}

    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update({"referer": "http://music.163.com/"})

    r = s.post("http://music.163.com/api/linux/forward", data=data)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j["code"] != 200:
        raise ResponseError(r.text)

    music_list = []
    try:
        for m in j["result"]["songs"]:
            if m["privilege"]["fl"] == 0:
                # 没有版权
                continue
            # 获得歌手名字
            singers = [s["name"] for s in m["ar"]]
            # 获得最优音质的文件大小
            if m["privilege"]["fl"] >= 320000 and "h" in m and m["h"]:
                # 有时候即使>=320000，h属性依然为None
                size = m["h"]["size"]
            elif m["privilege"]["fl"] >= 192000 and "m" in m and m["m"]:
                size = m["m"]["size"]
            else:
                size = m["l"]["size"]

            music = Music()
            music.source = "netease"
            music.id = m["id"]
            music.title = m["name"]
            music.singer = "、".join(singers)
            music.album = m["al"]["name"]
            music.duration = int(m["dt"] / 1000)
            music.size = round(size / 1048576, 2)
            music_list.append(music)
    except Exception as e:
        raise DataError(e)

    return music_list


def netease_download(music):
    """ 从网易云音乐下载 """
    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/song/enhance/player/url",
        "params": {"ids": [music.id], "br": 320000},
    }
    data = {"eparams": encode_netease_data(eparams)}

    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update({"referer": "http://music.163.com/"})

    r = s.post("http://music.163.com/api/linux/forward", data=data)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j["code"] != 200:
        raise ResponseError(r.text)

    music.url = j["data"][0]["url"]
    music.rate = int(j["data"][0]["br"] / 1000)

    music.download()


def encode_netease_data(data) -> str:
    data = json.dumps(data)
    key = binascii.unhexlify("7246674226682325323F5E6544673A51")
    encryptor = AES.new(key, AES.MODE_ECB)
    # 补足data长度，使其是16的倍数
    pad = 16 - len(data) % 16
    fix = chr(pad) * pad
    byte_data = (data + fix).encode("utf-8")
    return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()


search = netease_search
download = netease_download
