#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: HJK
@file: main.py
@time: 2019-01-08
"""

import sys
import os
import re
import gettext
import click
import logging
import prettytable as pt
from . import config
from .utils import colorize
from .source import MusicSource
from .player import play_music, time_duration_to_seconds

gettext.install("music-dl", "locale")


def menu(songs_list):
    # 创建table
    tb = pt.PrettyTable()
    tb.field_names = ["序号", "歌名", "歌手", "大小", "时长", "专辑", "来源"]
    # 遍历输出搜索列表
    songs_list.sort(key=lambda x: x.size)
    for index, song in enumerate(songs_list):
        song.idx = index
        tb.add_row(song.row)
        # click.echo(song.info)
    tb.align = "l"
    click.echo(tb)
    click.echo("")

    # 用户指定下载序号
    prompt = (
        _("请输入{下载序号}，支持形如 {numbers} 的格式，输入 {N} 跳过下载").format(
            下载序号=colorize(_("下载序号"), "yellow"),
            numbers=colorize("0 3-5 8", "yellow"),
            N=colorize("N", "yellow"),
        )
        + "\n >>"
    )

    choices = click.prompt(prompt)

    while not re.match(r"^((\d+\-\d+)|(\d+)|\s+)+$", choices):
        if choices.lower() == "n":
            return
        choices = click.prompt("%s%s" % (colorize(_("输入有误!"), "red"), prompt))

    click.echo("")
    selected_list = []
    downloaded_files = []
    
    for choice in choices.split():
        start, to, end = choice.partition("-")
        if end:
            selected_list += range(int(start), int(end) + 1)
        else:
            selected_list.append(int(start))

    for idx in selected_list:
        if idx < len(songs_list):
            song = songs_list[idx]
            # 记录下载前的文件不存在状态
            song_file_exists = os.path.exists(song.song_fullname) if hasattr(song, 'song_fullname') else False
            
            # 下载歌曲
            song.download()
            
            # 确认文件被下载成功（通过检查文件是否存在且下载前不存在）
            if hasattr(song, 'song_fullname') and os.path.exists(song.song_fullname) and (song.song_url or not song_file_exists):
                downloaded_files.append(song.song_fullname)
    
    # 如果启用了播放功能，则播放下载的音乐
    if config.get("play") and downloaded_files:
        play_music(downloaded_files)


def run():
    ms = MusicSource()
    if config.get("keyword"):
        songs_list = ms.search(config.get("keyword"), config.get("source").split())
        
        # 处理过滤条件
        filter_str = config.get("filter")
        if filter_str:
            for condition in filter_str.split(','):
                if not condition:
                    continue
                
                # 解析条件
                filtered_songs = []
                
                if condition.startswith("size"):
                    # 解析大小条件
                    if ">" in condition:
                        size_limit = float(condition.split(">")[1])
                        filtered_songs = [song for song in songs_list if 
                                          (song.size and song.size > size_limit) or not song.size]
                    elif "<" in condition:
                        size_limit = float(condition.split("<")[1])
                        filtered_songs = [song for song in songs_list if 
                                          (song.size and song.size < size_limit) or not song.size]
                    elif "=" in condition:
                        size_equal = float(condition.split("=")[1])
                        filtered_songs = [song for song in songs_list if 
                                          (song.size and abs(song.size - size_equal) < 0.01) or not song.size]
                
                elif condition.startswith("length"):
                    # 解析时长条件
                    if ">" in condition:
                        length_limit = int(condition.split(">")[1])
                        filtered_songs = [song for song in songs_list if 
                                        not song._duration or time_duration_to_seconds(song._duration) > length_limit]
                    elif "<" in condition:
                        length_limit = int(condition.split("<")[1])
                        filtered_songs = [song for song in songs_list if 
                                        not song._duration or time_duration_to_seconds(song._duration) < length_limit]
                    elif "=" in condition:
                        length_equal = int(condition.split("=")[1])
                        filtered_songs = [song for song in songs_list if 
                                        not song._duration or time_duration_to_seconds(song._duration) == length_equal]
                
                # 更新歌曲列表
                songs_list = filtered_songs
        
        menu(songs_list)
        config.set("keyword", click.prompt(_("请输入要搜索的歌曲，或Ctrl+C退出") + "\n >>"))
        run()
    elif config.get("playlist"):
        songs_list = ms.playlist(config.get("playlist"))
        menu(songs_list)
    elif config.get("url"):
        song = ms.single(config.get("url"))
        # 记录下载前的文件不存在状态
        song_file_exists = os.path.exists(song.song_fullname) if hasattr(song, 'song_fullname') else False
        
        # 下载歌曲
        song.download()
        
        # 如果启用了播放功能，则播放下载的音乐
        if config.get("play") and hasattr(song, 'song_fullname') and os.path.exists(song.song_fullname) and (song.song_url or not song_file_exists):
            play_music([song.song_fullname])
    else:
        return


@click.command()
@click.version_option()
@click.option("-k", "--keyword", help=_("搜索关键字，歌名和歌手同时输入可以提高匹配（如 空帆船 朴树）"))
@click.option("-u", "--url", default="", help=_("通过指定的歌曲URL下载音乐"))
@click.option("-p", "--playlist", default="", help=_("通过指定的歌单URL下载音乐"))
@click.option(
    "-s",
    "--source",
    # default="qq netease kugou baidu",
    help=_("支持的数据源: ") + "baidu",
)
@click.option("-n", "--number", default=5, help=_("搜索数量限制"))
@click.option("-o", "--outdir", default=".", help=_("指定输出目录"))
@click.option("-x", "--proxy", default="", help=_("指定代理（如http://127.0.0.1:1087）"))
@click.option("-v", "--verbose", default=False, is_flag=True, help=_("详细模式"))
@click.option("--lyrics", default=False, is_flag=True, help=_("同时下载歌词"))
@click.option("--cover", default=False, is_flag=True, help=_("同时下载封面"))
@click.option("--nomerge", default=False, is_flag=True, help=_("不对搜索结果列表排序和去重"))
@click.option("--filter", default="", help=_("过滤条件，如'size>8,length>300'表示大于8MB且时长超过5分钟"))
@click.option("--play", default=False, is_flag=True, help=_("下载完成后播放音乐"))
def main(
    keyword,
    url,
    playlist,
    source,
    number,
    outdir,
    proxy,
    verbose,
    lyrics,
    cover,
    nomerge,
    filter,
    play,
):
    """
        Search and download music from netease, qq, kugou, baidu and xiami.
        Example: music-dl -k "周杰伦"
    """
    if sum([bool(keyword), bool(url), bool(playlist)]) != 1:
        # click.echo(_("ERROR: 必须指定搜索关键字、歌曲的URL或歌单的URL中的一个") + "\n", err=True)
        # ctx = click.get_current_context()
        # click.echo(ctx.get_help())
        # ctx.exit()
        keyword = click.prompt(_("搜索关键字，歌名和歌手同时输入可以提高匹配（如 空帆船 朴树）") + "\n >>")

    # 初始化全局变量
    config.init()
    config.set("keyword", keyword)
    config.set("url", url)
    config.set("playlist", playlist)
    if source:
        config.set("source", source)
    config.set("number", min(number, 50))
    config.set("outdir", outdir)
    config.set("verbose", verbose)
    config.set("lyrics", lyrics)
    config.set("cover", cover)
    config.set("nomerge", nomerge)
    config.set("filter", filter)
    config.set("play", play)
    if proxy:
        proxies = {"http": proxy, "https": proxy}
        config.set("proxies", proxies)

    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)-8s | %(name)s: %(msg)s ",
        datefmt="%H:%M:%S",
    )

    try:
        run()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)


if __name__ == "__main__":
    main()
