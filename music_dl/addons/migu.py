#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: migu
@time: 2019-08-25
"""

import copy
from .. import config
from ..api import MusicApi
from ..song import BasicSong


class MiguApi(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update(
        {"referer": "http://music.migu.cn/", "User-Agent": config.get("ios_useragent")}
    )


class MiguSong(BasicSong):
    def __init__(self):
        super(MiguSong, self).__init__()
        self.content_id = ""

def migu_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = {
        "ua": "Android_migu",
        "version": "5.0.1",
        "text": keyword,
        "pageNo": 1,
        "pageSize": number,
        "searchSwitch": '{"song":1,"album":0,"singer":0,"tagSong":0,"mvSong":0,"songlist":0,"bestShow":1}',
    }

    songs_list = []
    MiguApi.session.headers.update(
        {"referer": "http://music.migu.cn/", "User-Agent": config.get("ios_useragent")}
    )
    res_data = (
        MiguApi.request(
            "http://pd.musicapp.migu.cn/MIGUM2.0/v1.0/content/search_all.do",
            method="GET",
            data=params,
        )
        .get("songResultData", {})
        .get("result", [])
    )

    for item in res_data:
        # 获得歌手名字
        singers = [s.get("name", "") for s in item.get("singers", [])]
        song = MiguSong()
        song.source = "MIGU"
        song.id = item.get("id", "")
        song.title = item.get("name", "")
        song.singer = "、".join(singers)
        song.album = item.get("albums", [])[0].get("name", "")
        song.cover_url = item.get("imgItems", [])[0].get("img", "")
        song.lyrics_url = item.get("lyricUrl", item.get("trcUrl", ""))
        # song.duration = item.get("interval", 0)
        # 特有字段
        song.content_id = item.get("contentId", "")
        # 品质从高到低排序
        rate_list = sorted(
            item.get("rateFormats", []), key=lambda x: int(x["size"]), reverse=True
        )
        for rate in rate_list:
            url = "http://app.pd.nf.migu.cn/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag={formatType}&netType=00&userId=15548614588710179085069&ua=Android_migu&version=5.1&copyrightId=0&contentId={contentId}&resourceType={resourceType}&channel=0".format(
                formatType=rate.get("formatType", "SQ"),
                contentId=song.content_id,
                resourceType=rate.get("resourceType", "E"),
            )
            song.song_url = url
            if song.available:
                song.size = round(int(rate.get("size", 0)) / 1048576, 2)
                ext = "flac" if rate.get("formatType", "") == "SQ" else "mp3"
                song.ext = rate.get("fileType", ext)
                break

        songs_list.append(song)

    return songs_list


search = migu_search
