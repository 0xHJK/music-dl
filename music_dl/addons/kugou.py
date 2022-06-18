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
from urllib.parse import urlparse, parse_qs
import math

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
        url = f"http://krcs.kugou.com/search?ver=1&client=mobi&duration=&hash={self.hash}&album_audio_id="
        req = KugouApi.request(url, method="GET")
        id = req.get('candidates')[0].get('id')
        accesskey = req.get('candidates')[0].get('accesskey')
        song = req.get('candidates')[0].get('song')
        url_lrc = f"http://lyrics.kugou.com/download?ver=1&client=pc&id={id}&accesskey={accesskey}&fmt=lrc&charset=utf8"
        res_lrc = KugouApi.request(
            url_lrc, method="GET"
        )
        import base64
        self.lyrics_text = base64.b64decode(res_lrc.get('content')).decode("utf-8")
        if self.lyrics_text:
            super(KugouSong, self)._save_lyrics_text()

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
    """搜索音乐"""
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

def repeat_get_resource(query) -> list:
    return KugouApi.request("https://m3ws.kugou.com/zlist/list", method="GET", data=query).get('list', {}).get('info', [])

def kugou_playlist(url) -> list:
    songs_list = []
    res = KugouApi.requestInstance(
        url,
        method="GET",
    )
    url = urlparse(res.url)
    query = parse_qs(url.query)
    query["page"] = 1
    query["pagesize"] = 100 # 最大100
    res_list = (
        KugouApi.request("https://m3ws.kugou.com/zlist/list", method="GET", data=query).get('list', {})
    )
    res_data = res_list.get('info', [])
    res_count = res_list.get('count', 0)
    repeat_count = math.floor(res_count / (query["page"] * query["pagesize"]))

    while repeat_count > 0:
        repeat_count -= 1
        query["page"] += 1
        for item in repeat_get_resource(query):
            res_data.append(item)

    for item in res_data:
        song = KugouSong()
        song.source = "kugou"
        song.id = item.get("fileid", "")
        singer_title = item.get("name", "").split(' - ')
        song.title = singer_title[1]
        song.singer = singer_title[0]
        song.duration = int(item.get("timelen", 0) / 1000) 
        song.album = item.get("album_id", "")
        song.size = round(item.get("size", 0) / 1048576, 2)
        song.hash = item.get("hash", "")
        songs_list.append(song)

    return songs_list


search = kugou_search
playlist = kugou_playlist
