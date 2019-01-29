#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: xiami.py
@time: 2019-01-21

从虾米搜索和下载音乐

"""

import threading
import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..music import Music

__all__ = ["xiami_search", "xiami_download"]


def xiami_search(keyword) -> list:
    """ 搜索音乐 """
    count = config.get("count") or 5
    params = {
        "key": keyword,
        "v": "2.0",
        "app_key": "1",
        "r": "search/songs",
        "page": 1,
        "limit": count,
    }
    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    # 获取cookie
    s.head("http://m.xiami.com")
    s.headers.update({"referer": "http://m.xiami.com/"})

    music_list = []
    r = s.get("http://api.xiami.com/web", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    thread_pool = []

    for m in j["data"]["songs"]:
        # 如果无版权则不显示
        if not m["listen_file"]:
            continue
        music = Music()
        music.source = "xiami"
        music.id = m["song_id"]
        music.title = m["song_name"]
        music.singer = m["artist_name"]
        music.album = m["album_name"]
        # 默认使用320K
        music.url = m["listen_file"].replace("m128.xiami.net", "m320.xiami.net")
        music.rate = 320

        t = threading.Thread(target=xiami_music_info, args=(music, music_list, s))
        thread_pool.append(t)
        t.start()

    for t in thread_pool:
        t.join()

    return music_list


def xiami_download(music):
    """ 从虾米音乐下载音乐 """
    music.download()


def xiami_music_info(music, music_list, s):
    """
        需要补充请求获得音乐信息，用于多线程
    :param music: 音乐对象
    :param music_list: 音乐对象列表
    :param s: requests session
    :return: 返回结果直接追加到music_list中
    """
    mr = s.get("http://www.xiami.com/song/playlist/id/%s/type/0/cat/json" % music.id)
    if mr.status_code != requests.codes.ok:
        raise RequestError(mr.text)
    mj = mr.json()
    if not mj["data"]["trackList"]:
        # raise DataError('no data.trackList')
        return

    mj_music = mj["data"]["trackList"][0]
    music.duration = mj_music["length"]

    if not music.avaiable:
        # 如果没有320K则使用128K
        music.url = music.url.replace("m320.xiami.net", "m128.xiami.net")
        music.rate = 128

    music_list.append(music)


search = xiami_search
download = xiami_download
