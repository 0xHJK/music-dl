#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: source.py
@time: 2019-05-13
"""

"""
    Music source proxy object
"""

import re
import threading
import importlib
import traceback
import logging
import click
from . import config
from .utils import colorize
from .exceptions import *


class MusicSource:
    """
        Music source proxy object
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def search(self, keyword, sources_list) -> list:
        sources_map = {
            "baidu": "baidu",
            # "flac": "flac",
            "kugou": "kugou",
            "netease": "netease",
            "163": "netease",
            "qq": "qq",
            "migu": "migu",
            # "xiami": "xiami",
        }
        thread_pool = []
        ret_songs_list = []
        ret_errors = []

        click.echo("")
        click.echo(
            _("Searching {keyword} from ...").format(
                keyword=colorize(config.get("keyword"), "highlight")
            ),
            nl=False,
        )

        for source_key in sources_list:
            if not source_key in sources_map:
                raise ParameterError("Invalid music source.")

            t = threading.Thread(
                target=self.search_thread,
                args=(sources_map.get(source_key), keyword, ret_songs_list, ret_errors),
            )
            thread_pool.append(t)
            t.start()

        for t in thread_pool:
            t.join()

        click.echo("")
        # 输出错误信息
        for err in ret_errors:
            self.logger.debug(_("音乐列表 {error} 获取失败.").format(error=err[0].upper()))
            self.logger.debug(err[1])

        # 对搜索结果排序和去重
        if not config.get("nomerge"):
            ret_songs_list.sort(
                key=lambda song: (song.singer, song.title, song.size), reverse=True
            )
            tmp_list = []
            for i in range(len(ret_songs_list)):
                # 如果名称、歌手都一致的话就去重，保留最大的文件
                if (
                    i > 0
                    and ret_songs_list[i].size <= ret_songs_list[i - 1].size
                    and ret_songs_list[i].title == ret_songs_list[i - 1].title
                    and ret_songs_list[i].singer == ret_songs_list[i - 1].singer
                ):
                    continue
                tmp_list.append(ret_songs_list[i])
            ret_songs_list = tmp_list

        return ret_songs_list

    def search_thread(self, source, keyword, ret_songs_list, ret_errors):
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            ret_songs_list += addon.search(keyword)
        except (RequestError, ResponseError, DataError) as e:
            ret_errors.append((source, e))
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            ret_errors.append((source, err))
        finally:
            # 放在搜索后输出是为了营造出搜索很快的假象
            click.echo(" %s ..." % colorize(source.upper(), source), nl=False)

    def single(self, url):
        sources_map = {
            # "baidu.com": "baidu",
            # "flac": "flac",
            # "kugou.com": "kugou",
            "163.com": "netease",
            # "qq.com": "qq",
            # "xiami.com": "xiami",
        }
        sources = [v for k, v in sources_map.items() if k in url]
        if not sources:
            raise ParameterError("Invalid url.")
        source = sources[0]
        click.echo(_("Downloading song from %s ..." % source.upper()))
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            song = addon.single(url)
            return song
        except (RequestError, ResponseError, DataError) as e:
            self.logger.error(e)
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            self.logger.error(err)

    def playlist(self, url) -> list:
        sources_map = {
            # "baidu.com": "baidu",
            # "flac": "flac",
            # "kugou.com": "kugou",
            "163.com": "netease",
            # "qq.com": "qq",
            # "xiami.com": "xiami",
        }
        sources = [v for k, v in sources_map.items() if k in url]
        if not sources:
            raise ParameterError("Invalid url.")
        source = sources[0]
        click.echo(_("Parsing music playlist from %s ..." % source.upper()))
        ret_songs_list = []
        try:
            addon = importlib.import_module(".addons." + source, __package__)
            ret_songs_list = addon.playlist(url)
        except (RequestError, ResponseError, DataError) as e:
            self.logger.error(e)
        except Exception as e:
            # 最后一起输出错误信息免得影响搜索结果列表排版
            err = traceback.format_exc() if config.get("verbose") else str(e)
            self.logger.error(err)

        return ret_songs_list
