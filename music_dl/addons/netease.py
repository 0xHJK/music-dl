#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: netease.py
@time: 2019-05-08
"""

import os
import binascii
import base64
import json
import requests
from Crypto.Cipher import AES
from .. import config
from ..exceptions import RequestError, ResponseError, DataError
from ..song import BasicSong


class NeteaseSong(BasicSong):
    def __init__(self):
        super(NeteaseSong, self).__init__()

    def download_lyrics(self):
        row_data = {
            "csrf_token": "",
            "id": self.id,
            "lv": -1,
            "tv": -1
        }
        data = encrypted_request(row_data)
        s = requests.Session()
        s.headers.update(config.get("fake_headers"))
        if config.get("proxies"):
            s.proxies.update(config.get("proxies"))
        s.headers.update({"referer": "http://music.163.com/"})
        r = s.post("https://music.163.com/weapi/song/lyric", data=data)
        json_data = r.json()

        if "lrc" in json_data and "lyric" in json_data["lrc"]:
            self.lyrics_text = json_data["lrc"]["lyric"]
            super(NeteaseSong, self)._save_lyrics_text()

    def download(self):
        """ Download song from netease music """
        eparams = {
            "method": "POST",
            "url": "http://music.163.com/api/song/enhance/player/url",
            "params": {"ids": [self.id], "br": 320000},
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

        self.song_url = j["data"][0]["url"]
        self.rate = int(j["data"][0]["br"] / 1000)

        super(NeteaseSong, self).download()


def netease_search(keyword) -> list:
    """ 从网易云音乐搜索 """
    number = config.get("number") or 5
    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": keyword, "type": 1, "offset": 0, "limit": number},
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

            song = NeteaseSong()
            song.source = "netease"
            song.id = m["id"]
            song.title = m["name"]
            song.singer = "、".join(singers)
            song.album = m["al"]["name"]
            song.duration = int(m["dt"] / 1000)
            song.size = round(size / 1048576, 2)
            song.cover_url = m["al"]["picUrl"]
            music_list.append(song)
    except Exception as e:
        raise DataError(e)

    return music_list


def encode_netease_data(data) -> str:
    data = json.dumps(data)
    key = binascii.unhexlify("7246674226682325323F5E6544673A51")
    encryptor = AES.new(key, AES.MODE_ECB)
    # 补足data长度，使其是16的倍数
    pad = 16 - len(data) % 16
    fix = chr(pad) * pad
    byte_data = (data + fix).encode("utf-8")
    return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

def encrypted_request(data) -> dict:
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
    secret = create_key(16)
    params = aes(aes(data, NONCE), secret)
    encseckey = rsa(secret, PUBKEY, MODULUS)
    return {"params": params, "encSecKey": encseckey}


def aes(text, key):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(key, 2, b"0102030405060708")
    ciphertext = encryptor.encrypt(text)
    return base64.b64encode(ciphertext)


def rsa(text, pubkey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
    return format(rs, "x").zfill(256)


def create_key(size):
    return binascii.hexlify(os.urandom(size))[:16]

def netease_playlist(url):
    pass


search = netease_search
playlist = netease_playlist
