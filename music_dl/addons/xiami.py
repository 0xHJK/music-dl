#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: xiami.py
@time: 2019-06-13
"""

import re
import copy
import json
import hashlib
from .. import config
from ..api import MusicApi
from ..song import BasicSong
from ..exceptions import DataError

__all__ = ["search"]


class XiamiApi(MusicApi):
    session = copy.deepcopy(MusicApi.session)
    session.headers.update({"referer": "http://www.xiami.com/song/play"})

    @classmethod
    def encrypted_params(cls, keyword):
        number = config.get("number") or 5
        _q = dict(key=keyword, pagingVO=dict(page=1, pageSize=number))
        _q = json.dumps(_q)
        url = "https://www.xiami.com/search?key={}".format(keyword)
        res = cls.session.get(url)
        cookie = res.cookies.get("xm_sg_tk", "").split("_")[0]
        origin_str = "%s_xmMain_/api/search/searchSongs_%s" % (cookie, _q)
        _s = hashlib.md5(origin_str.encode()).hexdigest()
        return dict(_q=_q, _s=_s)


class XiamiSong(BasicSong):
    def __init__(self):
        super(XiamiSong, self).__init__()


def xiami_search(keyword) -> list:
    """ search music from xiami """
    params = XiamiApi.encrypted_params(keyword=keyword)
    print(params)
    res_data = (
        XiamiApi.request(
            "https://www.xiami.com/api/search/searchSongs", method="GET", data=params
        )
        .get("result", {})
        .get("data", {})
        .get("songs", [])
    )
    if not res_data:
        raise DataError("Get xiami data failed.")

    songs_list = []
    for item in res_data:
        song = XiamiSong()
        song.source = "xiami"
        song.id = item.get("songId", "")
        song.title = item.get("songName", "")
        song.singer = item.get("singers", "")
        song.album = item.get("albumName", "")
        song.cover_url = item.get("albumLogo", "")
        song.lyrics_url = item.get("lyricInfo", {}).get("lyricFile", "")

        listen_files = sorted(
            item.get("listenFiles", []),
            key=lambda x: x.get("downloadFileSize", 0),
            reverse=True,
        )
        song.song_url = listen_files[0].get("listenFile", "")
        song.duration = int(listen_files[0].get("length", 0) / 1000)
        song.ext = listen_files[0].get("format", "mp3")
        song.rate = re.findall("https?://s(\d+)", song.song_url)[0]

        songs_list.append(song)

    return songs_list


search = xiami_search
