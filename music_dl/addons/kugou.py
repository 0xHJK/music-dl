#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: kugou.py
@time: 2019-05-08
"""

import copy
from .. import config
from ..api import MusicApi
from ..song import BasicSong


class KugouApi(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update(
        {"referer": "http://m.kugou.com", "User-Agent": config.get("ios_headers")}
    )


class KugouSong(BasicSong):
    def __init__(self):
        super(KugouSong, self).__init__()
        self.hash = ""

    def download_lyrics(self):
        pass

    def download(self):
        params = dict(cmd="playInfo", hash=self.hash)
        res_data = KugouApi.request(
            "http://m.kugou.com/app/i/getSongInfo.php", method="GET", data=params
        )
        if not res_data.get("url", ""):
            self.logger.error(self.name + " @KUGOU is not available.")
            return
        self.song_url = res_data.get("url", "")
        self.rate = res_data.get("bitRate", 128)
        self.ext = res_data.get("extName", "mp3")
        self.cover_url = res_data.get("album_img", "").replace("{size}", "150")

        super(KugouSong, self).download()


def kugou_search(keyword) -> list:
    """ 搜索音乐 """
    number = config.get("number") or 5
    params = dict(
        keyword=keyword, platform="WebFilter", format="json", page=1, pagesize=number
    )

    songs_list = []
    res_data = (
        KugouApi.request(
            "http://songsearch.kugou.com/song_search_v2", method="GET", data=params
        )
        .get("data", {})
        .get("lists", [])
    )

    for item in res_data:
        song = KugouSong()
        song.source = "kugou"
        song.id = item.get("Scid", "")
        song.title = item.get("SongName", "")
        song.singer = item.get("SingerName", "")
        song.duration = item.get("Duration", 0)
        song.album = item.get("AlbumName", "")
        song.size = round(item.get("FileSize", 0) / 1048576, 2)
        song.hash = item.get("FileHash", "")
        # 如果有更高品质的音乐选择高品质（尽管好像没什么卵用）
        keys_list = ["SQFileHash", "HQFileHash"]
        for key in keys_list:
            hash = item.get(key, "")
            if hash and hash != "00000000000000000000000000000000":
                song.hash = hash
                break
        songs_list.append(song)

    return songs_list


def kugou_playlist(url):
    pass


search = kugou_search
playlist = kugou_playlist
