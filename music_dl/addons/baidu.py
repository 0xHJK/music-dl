#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: baidu.py
@time: 2019-05-08
"""

import copy
from .. import config
from ..api import MusicApi
from ..song import BasicSong


class BaiduSong(BasicSong):
    def __init__(self):
        super(BaiduSong, self).__init__()


class BaiduApi(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update({"referer": "http://music.baidu.com/"})


def baidu_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = dict(
        query=keyword,
        method="baidu.ting.search.common",
        format="json",
        page_no=1,
        page_size=number,
    )

    songs_list = []
    res_data = BaiduApi.request(
        "http://musicapi.qianqian.com/v1/restserver/ting", method="GET", data=params
    ).get("song_list", [])

    for item in res_data:
        song = BaiduSong()
        song.source = "baidu"
        song.id = item.get("song_id", "")
        song.title = item.get("title", "").replace("<em>", "").replace("</em>", "")
        song.singer = item.get("author").replace("<em>", "").replace("</em>", "")
        song.album = item.get("album_title").replace("<em>", "").replace("</em>", "")
        song.lyrics_url = "http://musicapi.qianqian.com/v1/restserver/ting" + item.get(
            "lrclink", ""
        )

        m_params = dict(method="baidu.ting.song.play", bit=320, songid=song.id)
        res_song_data = BaiduApi.request(
            "http://tingapi.ting.baidu.com/v1/restserver/ting",
            method="GET",
            data=m_params,
        )

        bitrate = res_song_data.get("bitrate", {})
        if not bitrate:
            continue
        song.song_url = bitrate.get("file_link", "")
        if not song.available:  # 如果URL拿不到内容
            continue
        song.duration = bitrate.get("file_duration", 0)
        song.rate = bitrate.get("file_bitrate", 128)
        song.ext = bitrate.get("file_extension", "mp3")
        song.cover_url = res_song_data.get("songinfo", {}).get("pic_radio", "")
        songs_list.append(song)

    return songs_list


def baidu_playlist(url):
    """ Download playlist from baidu music. """
    pass


search = baidu_search
playlist = baidu_playlist
