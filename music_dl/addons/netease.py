#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: netease.py
@time: 2019-05-08
"""

import os
import re
import binascii
import base64
import json
import copy
from Crypto.Cipher import AES
from .. import config
from ..api import MusicApi
from ..exceptions import RequestError, ResponseError, DataError
from ..song import BasicSong

__all__ = ["search", "playlist"]


class NeteaseApi(MusicApi):
    """ Netease music api http://music.163.com """

    session = copy.deepcopy(MusicApi.session)
    session.headers.update({"referer": "http://music.163.com/"})

    @classmethod
    def encode_netease_data(cls, data) -> str:
        data = json.dumps(data)
        key = binascii.unhexlify("7246674226682325323F5E6544673A51")
        encryptor = AES.new(key, AES.MODE_ECB)
        # 补足data长度，使其是16的倍数
        pad = 16 - len(data) % 16
        fix = chr(pad) * pad
        byte_data = (data + fix).encode("utf-8")
        return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

    @classmethod
    def encrypted_request(cls, data) -> dict:
        MODULUS = (
            "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7"
            "b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280"
            "104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932"
            "575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b"
            "3ece0462db0a22b8e7"
        )
        PUBKEY = "010001"
        NONCE = b"0CoJUm6Qyw8W8jud"
        data = json.dumps(data).encode("utf-8")
        secret = cls.create_key(16)
        params = cls.aes(cls.aes(data, NONCE), secret)
        encseckey = cls.rsa(secret, PUBKEY, MODULUS)
        return {"params": params, "encSecKey": encseckey}

    @classmethod
    def aes(cls, text, key):
        pad = 16 - len(text) % 16
        text = text + bytearray([pad] * pad)
        encryptor = AES.new(key, 2, b"0102030405060708")
        ciphertext = encryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    @classmethod
    def rsa(cls, text, pubkey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
        return format(rs, "x").zfill(256)

    @classmethod
    def create_key(cls, size):
        return binascii.hexlify(os.urandom(size))[:16]


class NeteaseSong(BasicSong):
    def __init__(self):
        super(NeteaseSong, self).__init__()

    def download_lyrics(self):
        row_data = {"csrf_token": "", "id": self.id, "lv": -1, "tv": -1}
        data = NeteaseApi.encrypted_request(row_data)

        self.lyrics_text = (
            NeteaseApi.request(
                "https://music.163.com/weapi/song/lyric", method="POST", data=data
            )
            .get("lrc", {})
            .get("lyric", "")
        )

        if self.lyrics_text:
            super(NeteaseSong, self)._save_lyrics_text()

    def download(self):
        """ Download song from netease music """
        data = NeteaseApi.encrypted_request(dict(ids=[self.id], br=32000))
        res_data = NeteaseApi.request(
            "http://music.163.com/weapi/song/enhance/player/url",
            method="POST",
            data=data,
        ).get("data", [])

        if len(res_data) > 0:
            self.song_url = res_data[0].get("url", "")
            self.rate = int(res_data[0].get("br", 0) / 1000)

        super(NeteaseSong, self).download()


def netease_search(keyword) -> list:
    """ Search song from netease music """
    number = config.get("number") or 5
    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": keyword, "type": 1, "offset": 0, "limit": number},
    }
    data = {"eparams": NeteaseApi.encode_netease_data(eparams)}

    songs_list = []
    res_data = (
        NeteaseApi.request(
            "http://music.163.com/api/linux/forward", method="POST", data=data
        )
        .get("result", {})
        .get("songs", {})
    )
    try:
        for item in res_data:
            if item.get("privilege", {}).get("fl", {}) == 0:
                # 没有版权
                continue
            # 获得歌手名字
            singers = [s.get("name", "") for s in item.get("ar", [])]
            # 获得音乐的文件大小
            # TODO: 获取到的大小并不准确，考虑逐一获取歌曲详情
            if item.get("privilege", {}).get("fl", {}) >= 320000 and item.get("h", ""):
                size = item.get("h", {}).get("size", 0)
            elif item.get("privilege", {}).get("fl", {}) >= 192000 and item.get(
                "m", ""
            ):
                size = item.get("m", {}).get("size", 0)
            else:
                size = item.get("l", {}).get("size", 0)

            song = NeteaseSong()
            song.source = "netease"
            song.id = item.get("id", "")
            song.title = item.get("name", "")
            song.singer = "、".join(singers)
            song.album = item.get("al", {}).get("name", "")
            song.duration = int(item.get("dt", 0) / 1000)
            song.size = round(size / 1048576, 2)
            song.cover_url = item.get("al", {}).get("picUrl", "")
            songs_list.append(song)
    except Exception as e:
        raise DataError(e)

    return songs_list


def netease_playlist(url) -> list:
    songs_list = []
    playlist_id = re.findall(r".+playlist\\*\?id\\*=(\d+)", url)[0]
    if playlist_id:
        params = dict(
            id=playlist_id, total="true", limit=1000, n=1000, offest=0, csrf_token=""
        )
        data = NeteaseApi.encrypted_request(params)

        res_data = (
            NeteaseApi.request(
                "http://music.163.com/weapi/v3/playlist/detail",
                method="POST",
                data=data,
            )
            .get("playlist", {})
            .get("tracks", [])
        )
        for item in res_data:
            song = NeteaseSong()
            # 获得歌手名字
            singers = [s.get("name", "") for s in item.get("ar", {})]
            # 获得音乐文件大小
            # TODO: 获取到的大小并不准确，考虑逐一获取歌曲详情
            if item.get("l", ""):
                size = item.get("l", {}).get("size", 0)
            elif item.get("m", ""):
                size = item.get("m", {}).get("size", 0)
            else:
                size = item.get("h", {}).get("size", 0)
            song.source = "netease"
            song.id = item.get("id", "")
            song.title = item.get("name", "")
            song.singer = "、".join(singers)
            song.album = item.get("al", {}).get("name", "")
            song.duration = int(item.get("dt", 0) / 1000)
            song.size = round(size / 1048576, 2)
            song.cover_url = item.get("al", {}).get("picUrl", "")
            songs_list.append(song)
    return songs_list


def netease_single(url) -> NeteaseSong:
    song_id = re.findall(r".+song\\*\?id\\*=(\d+)", url)[0]
    data_detail = NeteaseApi.encrypted_request(
        dict(c=json.dumps([{"id": song_id}]), ids=[song_id])
    )
    res_data_detail = NeteaseApi.request(
        "http://music.163.com/weapi/v3/song/detail", method="POST", data=data_detail
    ).get("songs", [])
    if len(res_data_detail) > 0:
        item = res_data_detail[0]
        song = NeteaseSong()
        song.source = "netease"
        song.id = item.get("id", "")
        song.title = item.get("name", "")
        singers = [s.get("name", "") for s in item.get("ar", {})]
        song.singer = "、".join(singers)
        song.album = item.get("al", {}).get("name", "")
        song.duration = int(item.get("dt", 0) / 1000)
        song.cover_url = item.get("al", {}).get("picUrl", "")
        return song
    else:
        raise DataError("Get song detail failed.")


search = netease_search
playlist = netease_playlist
single = netease_single
