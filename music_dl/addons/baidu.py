#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: baidu.py
@time: 2019-05-08
"""

import requests
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..song import BasicSong


class BaiduSong(BasicSong):
    def __init__(self):
        super(BaiduSong, self).__init__()


def baidu_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = {
        "query": keyword,
        "method": "baidu.ting.search.common",
        "format": "json",
        "page_no": 1,
        "page_size": number,
    }
    s = requests.Session()
    s.headers.update(config.get("fake_headers"))
    if config.get("proxies"):
        s.proxies.update(config.get("proxies"))
    s.headers.update({"referer": "http://music.baidu.com/"})

    songs_list = []
    r = s.get("http://musicapi.qianqian.com/v1/restserver/ting", params=params)
    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()

    for m in j["song_list"]:
        song = BaiduSong()
        song.source = "baidu"
        song.id = m["song_id"]
        song.title = m["title"].replace("<em>", "").replace("</em>", "")
        song.singer = m["author"].replace("<em>", "").replace("</em>", "")
        song.album = m["album_title"].replace("<em>", "").replace("</em>", "")
        song.lyrics_url = (
            "http://musicapi.qianqian.com/v1/restserver/ting" + m["lrclink"]
        )

        # s.headers.update({"referer": "http://music.baidu.com/song/" + song.id})
        # m_params = {"songIds": song.id}
        # mr = s.get("http://music.baidu.com/data/music/links", params=m_params)
        m_params = dict(method="baidu.ting.song.play", bit=320, songid=song.id)
        mr = s.get("http://tingapi.ting.baidu.com/v1/restserver/ting", params=m_params)
        if mr.status_code != requests.codes.ok:
            raise RequestError(mr.text)
        mj = mr.json()
        bitrate = mj.get("bitrate", {})
        if not bitrate:
            continue
        song.song_url = bitrate.get("file_link", "")
        if not song.available:  # 如果URL拿不到内容
            continue
        song.duration = bitrate.get("file_duration", 0)
        song.rate = bitrate.get("file_bitrate", 128)
        song.ext = bitrate.get("file_extension", "mp3")
        song.cover_url = mj.get("songinfo", {}).get("pic_radio", "")
        songs_list.append(song)

    return songs_list


def baidu_playlist(url):
    """ Download playlist from baidu music. """
    pass


search = baidu_search
playlist = baidu_playlist
