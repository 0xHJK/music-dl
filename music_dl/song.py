#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: HJK
@file: basic.py
@time: 2019-05-07
"""

"""
    Basic song object
"""

import os
import re
import datetime
import logging
import click
import requests
from . import config
from .utils import colorize


class BasicSong:
    """
        Define the basic properties and methods of a song.
        Such as title, name, singer etc.
    """

    def __init__(self):
        self.idx = 0
        self.id = 0
        self.title = ""
        self.singer = ""
        self.ext = "mp3"
        self.album = ""
        self.size = ""
        self.rate = ""
        self._duration = ""
        self.source = ""
        self._song_url = ""
        # self.song_file = ""
        self.cover_url = ""
        # self.cover_file = ""
        self.lyrics_url = ""
        self.lyrics_text = ""
        # self.lyrics_file = ""
        self._fullname = ""
        self.logger = logging.getLogger(__name__)

    def __repr__(self):
        """ Abstract of the song """
        source = colorize("%s" % self.source.upper(), self.source)
        return "%s #%s %s-%s-%s \n %s \n" % (
            source,
            self.id,
            self.title,
            self.singer,
            self.album,
            self.song_url,
        )

    def __str__(self):
        """ Song details """
        source = colorize("%s" % self.source.upper(), self.source)
        return _(
            " -> Source: {source} #{id}\n"
            " -> Title: {title}\n"
            " -> Singer: {singer}\n"
            " -> Album: {album}\n"
            " -> Duration: {duration}\n"
            " -> Size: {size}MB\n"
            " -> Bit Rate: {rate}\n"
            " -> Song URL: {song_url}\n"
            " -> Lyrics URL: {lyrics_url}\n"
            " -> Cover URL: {cover_url}\n"
        ).format(
            source=source,
            id=self.id,
            title=self.title,
            singer=self.singer,
            album=self.album,
            duration=self.duration,
            size=self.size,
            rate=self.rate,
            song_url=self.song_url,
            lyrics_url=self.lyrics_url,
            cover_url=self.cover_url,
        )

    @property
    def available(self) -> bool:
        """ Not available when url is none or size equal 0 """
        return bool(self.song_url and self.size)

    @property
    def name(self) -> str:
        """ Song file name """
        return "%s - %s.%s" % (self.singer, self.title, self.ext)

    @property
    def duration(self):
        """ 持续时间 H:M:S """
        return self._duration

    @duration.setter
    def duration(self, seconds):
        self._duration = str(datetime.timedelta(seconds=int(seconds)))

    @property
    def song_url(self) -> str:
        return self._song_url

    @song_url.setter
    def song_url(self, url):
        """ Set song url and update size. """
        try:
            r = requests.get(
                url,
                stream=True,
                headers=config.get("wget_headers"),
                proxies=config.get("proxies"),
            )
            self._song_url = url
            size = int(r.headers.get("Content-Length", 0))
            # 转换成MB并保留两位小数
            self.size = round(size / 1048576, 2)
            # 设置完整的文件名（不含后缀）
            if not self._fullname:
                self._set_fullname()
        except Exception as e:
            self.logger.info(_("Request failed: {url}").format(url=url))
            self.logger.info(e)

    @property
    def row(self) -> list:
        """ Song details in list form """

        def highlight(s, k):
            return s.replace(k, colorize(k, "xiami")).replace(
                k.title(), colorize(k.title(), "xiami")
            )

        ht_singer = self.singer if len(self.singer) < 30 else self.singer[:30] + "..."
        ht_title = self.title if len(self.title) < 30 else self.title[:30] + "..."
        ht_album = self.album if len(self.album) < 20 else self.album[:20] + "..."

        if config.get("keyword"):
            keywords = re.split(";|,|\s|\*", config.get("keyword"))
            for k in keywords:
                if not k:
                    continue
                ht_singer = highlight(ht_singer, k)
                ht_title = highlight(ht_title, k)
                ht_album = highlight(ht_album, k)

        size = "%sMB" % self.size
        ht_size = size if int(self.size) < 8 else colorize(size, "flac")

        return [
            colorize(self.idx, "baidu"),
            ht_title,
            ht_singer,
            ht_size,
            self.duration,
            ht_album,
            self.source.upper(),
        ]

    def _set_fullname(self):
        """ Full name without suffix, to resolve file name conflicts"""
        outdir = config.get("outdir")
        outfile = os.path.abspath(os.path.join(outdir, self.name))
        if os.path.exists(outfile):
            name, ext = self.name.rsplit(".", 1)
            names = [
                x for x in os.listdir(outdir) if x.startswith(name) and x.endswith(ext)
            ]
            names = [x.rsplit(".", 1)[0] for x in names]
            suffixes = [x.replace(name, "") for x in names]
            # filter suffixes that match ' (x)' pattern
            suffixes = [
                x[2:-1] for x in suffixes if x.startswith(" (") and x.endswith(")")
            ]
            indexes = [int(x) for x in suffixes if set(x) <= set("0123456789")]
            idx = 1
            if indexes:
                idx += sorted(indexes)[-1]
            self._fullname = os.path.abspath(
                os.path.join(outdir, "%s (%d)" % (name, idx))
            )
        else:
            self._fullname = outfile.rpartition(".")[0]

    @property
    def song_fullname(self):
        return self._fullname + "." + self.ext

    @property
    def lyrics_fullname(self):
        return self._fullname + ".lrc"

    @property
    def cover_fullname(self):
        return self._fullname + ".jpg"

    def _download_file(self, url, outfile, stream=False):
        """
            Helper function for download
        :param url:
        :param outfile:
        :param stream: need process bar or not
        :return:
        """
        if not url:
            self.logger.error("URL is empty.")
            return
        try:
            r = requests.get(
                url,
                stream=stream,
                headers=config.get("wget_headers"),
                proxies=config.get("proxies"),
            )
            if stream:
                total_size = int(r.headers["content-length"])
                with click.progressbar(
                    length=total_size, label=_(" :: Downloading ...")
                ) as bar:
                    with open(outfile, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))
            else:
                with open(outfile, "wb") as f:
                    f.write(r.content)
            click.echo(
                _(" :: Saved to: {outfile}").format(
                    outfile=colorize(outfile, "highlight")
                )
            )
        except Exception as e:
            click.echo("")
            self.logger.error(_("Download failed: ") + "\n")
            self.logger.error(_("URL: {url}").format(url=url) + "\n")
            self.logger.error(
                _("File location: {outfile}").format(outfile=outfile) + "\n"
            )
            if config.get("verbose"):
                self.logger.error(e)

    def _save_lyrics_text(self):
        with open(self.lyrics_fullname, "w") as f:
            f.write(self.lyrics_text)
            click.echo(
                _(" :: Saved to: {outfile}").format(
                    outfile=colorize(self.lyrics_fullname, "highlight")
                )
            )

    def download_song(self):
        if self.song_url:
            self._download_file(self.song_url, self.song_fullname, stream=True)

    def download_lyrics(self):
        if self.lyrics_url:
            self._download_file(self.lyrics_url, self.lyrics_fullname, stream=False)

    def download_cover(self):
        if self.cover_url:
            self._download_file(self.cover_url, self.cover_fullname, stream=False)

    def download(self):
        """ Main download function """
        click.echo("===============================================================")
        if config.get("verbose"):
            click.echo(str(self))
        else:
            click.echo(" | ".join(self.row))

        self.download_song()
        if config.get("lyrics"):
            self.download_lyrics()
        if config.get("cover"):
            self.download_cover()

        click.echo("===============================================================\n")
