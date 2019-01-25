#!/usr/bin/env python  
#-*- coding:utf-8 -*-  
"""
@author: HJK 
@file: netease.py 
@time: 2019-01-11

网易云音乐下载

"""

import binascii
import json
import datetime
import traceback
from Crypto.Cipher import AES
import glovar
from core.common import *
from core.exceptions import *

def netease_search(keyword) -> list:
    ''' 从网易云音乐搜索 '''
    count = glovar.get_option('count') or 5
    eparams = {
        'method': 'POST',
        'url': 'http://music.163.com/api/cloudsearch/pc',
        'params': {
            's': keyword,
            'type': 1,
            'offset': 0,
            'limit': count
        }
    }
    data = {'eparams': encode_netease_data(eparams)}

    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://music.163.com/',
    })
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    r = s.post('http://music.163.com/api/linux/forward', data=data)

    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 200:
        raise ResponseError(j)

    music_list = []
    try:
        for m in j['result']['songs']:
            if m['privilege']['fl'] == 0:
                # 没有版权
                continue
            # 获得歌手名字
            singers = []
            for singer in m['ar']:
                singers.append(singer['name'])
            # 获得最优音质的文件大小
            if m['privilege']['fl'] >= 320000 and 'h' in m.keys() and m['h']:
                # 有时候即使>=320000，h属性依然为None
                size = m['h']['size']
            elif m['privilege']['fl'] >= 192000 and 'm' in m.keys() and m['m']:
                size = m['m']['size']
            else:
                size = m['l']['size']

            music = {
                'title': m['name'],
                'id': m['id'],
                'duration': str(datetime.timedelta(seconds=int(m['dt']/1000))),
                'singer': '、'.join(singers),
                'album': m['al']['name'],
                'size': round(size / 1048576, 2),
                'source': 'netease'
            }
            music_list.append(music)
    except Exception as e:
        # 如果是详细模式则输出详细错误信息
        err = traceback.format_exc() if glovar.get_option('verbose') else str(e)
        raise DataError(err)

    return music_list


def netease_download(music):
    ''' 从网易云音乐下载 '''
    eparams = {
        'method': 'POST',
        'url': 'http://music.163.com/api/song/enhance/player/url',
        'params': {
            'ids': [music['id']],
            'br': 320000,
        }
    }
    data = {'eparams': encode_netease_data(eparams)}

    s = requests.Session()
    s.headers.update(glovar.FAKE_HEADERS)
    s.headers.update({
        'referer': 'http://music.163.com/',
    })
    if glovar.get_option('proxies'):
        s.proxies.update(glovar.get_option('proxies'))

    r = s.post('http://music.163.com/api/linux/forward', data=data)

    if r.status_code != requests.codes.ok:
        raise RequestError(r.text)
    j = r.json()
    if j['code'] != 200:
        raise ResponseError(j)

    music['url'] = j['data'][0]['url']
    music['rate'] = int(j['data'][0]['br'] / 1000)
    music['size'] = round(j['data'][0]['size'] / 1048576, 2)
    music['name'] = '%s - %s.mp3' % (music['singer'], music['title'])

    music_download(music)


def encode_netease_data(data) -> str:
    data = json.dumps(data)
    key = binascii.unhexlify('7246674226682325323F5E6544673A51')
    encryptor = AES.new(key, AES.MODE_ECB)
    # 补足data长度，使其是16的倍数
    pad = 16 - len(data) % 16
    fix = chr(pad) * pad
    byte_data = (data + fix).encode('utf-8')
    return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

search = netease_search
download = netease_download