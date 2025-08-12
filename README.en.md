# Music-dl: Listen to what you want

<p align="center">
  <a href="https://github.com/0xHJK/music-dl">
    <img src="https://github.com/0xHJK/music-dl/raw/master/static/logo.png" height="400" alt="music-dl">
  </a>
</p>
<hr>
<p align="center">
  <a href="https://travis-ci.org/0xHJK/music-dl">
    <img src="https://travis-ci.org/0xHJK/music-dl.svg?branch=master">
  </a>
  <a><img src="https://img.shields.io/pypi/pyversions/pymusic-dl.svg"></a>
  <a href="https://codecov.io/gh/0xHJK/music-dl">
    <img src="https://codecov.io/gh/0xHJK/music-dl/branch/master/graph/badge.svg"/>
  </a>
  <a href="https://github.com/0xHJK/music-dl/releases">
    <img src="https://img.shields.io/github/release/0xHJK/music-dl.svg">
  </a>
  <a><img src="https://img.shields.io/github/license/0xHJK/music-dl.svg"></a>
</p>

**[Music-dl](https://github.com/0xHJK/music-dl)** is a command line tool which helps you search and download music from multiple sources.

Support for QQ music, Netease music, Xiami music, Kugou music and Baidu music. See [supported sources](#supported-sources).

**Python3 Only. Python 3.5+ Recommended.**

English | [中文文档](https://github.com/0xHJK/music-dl/blob/master/README.md)

> Note: Some music sources may not be available in some countries and regions. If that happens, you could use Chinese proxies. See <https://github.com/0xHJK/Proxies> for public proxies.

- Support for lossless music
- Search for high-quality music with priority ( flac -> 320K -> 128K )
- Support for HTTP and SOCKS proxy
- Support for multithreading searching
- Support for merging and sorting results
- Support keyword highlighting
- Support for filtering search results by file size and song duration (using `--filter` parameter)
- Support for auto-play after downloading (using `--play` parameter)
- Player supports common controls: space to pause/resume, left/right to switch songs, ,/. to move 5 seconds backward/forward, q to quit
- While playing, press d to delete songs you don't like (removes from disk and playlist)

## Installation

Install using pip (Recommended)

```bash
$ pip3 install pymusic-dl
```

Manual

```bash
$ git clone https://github.com/0xHJK/music-dl.git
$ cd music-dl
$ python3 setup.py install
```

Use directly

```bash
$ git clone https://github.com/0xHJK/music-dl.git
$ cd music-dl
$ pip3 install -r requirements.txt
$ ./music-dl

# OR python3 music-dl
```

## Usage

```
$ music-dl --help
Usage: music-dl [OPTIONS]

  Search and download music from netease, qq, kugou, baidu and xiami.
  Example: music-dl -k "Bruno Mars"

Options:
  --version            Show the version and exit.
  -k, --keyword TEXT   Query keyword
  -s, --source TEXT    Support for qq netease kugou baidu xiami flac
  -c, --count INTEGER  Searching count limit (default: 5)
  -o, --outdir TEXT    Output dir (default: current dir)
  -x, --proxy TEXT     Set proxy (like http://127.0.0.1:1087)
  -m, --merge          Sort and merge
  -v, --verbose        Verbose mode
  --lyrics              Download lyrics
  --cover               Download cover image
  --nomerge             Don't sort and merge search results
  --filter TEXT         Filter search results by file size and song duration
  --play                Enable auto-play after downloading
  --help               Show this message and exit.
```

- Default search sources are `qq netease kugou baidu`, with a limit of 5 results each, and the save directory is the current directory.
- When specifying numbers, you can use formats like `1-5 7 10`.
- By default, search results are sorted and deduplicated. Sorting is based on artist and song name, and when both are the same, the largest file is kept.
- Lossless music tracks are limited in number. If lossless is not available, 320K or 128K will be displayed.
- HTTP and SOCKS proxies are supported, in formats like `-x http://127.0.0.1:1087` or `-x socks5://127.0.0.1:1086`.

- Attributes supported by filter include:
  - `size`: File size in MB
  - `length`: Song duration in seconds

- Operators supported by filter include:
  - `>`: Greater than
  - `<`: Less than
  - `=`: Equal to

  ```bash
  music-dl -k --filter "size>8" # Only show songs larger than 8MB
  music-dl -k --filter "size<3" # Only show songs smaller than 3MB
  music-dl -k --filter "length>300" # Only show songs longer than 5 minutes
  music-dl -k --filter "length>180,length<300" # Only show songs between 3-5 minutes
  music-dl -k --filter "size>3,size<8,length>240" # Only show songs between 3-8MB and longer than 4 minutes
  ```

Example:

![](https://github.com/0xHJK/music-dl/raw/master/static/preview-en.png)

## Supported sources

| Music sources             | Abbreviation | Websites                  |
| ------------------------- | ------------ | ------------------------- |
| QQ Music                  | qq           | <https://y.qq.com/>       |
| Kugou Music               | kugou        | <http://www.kugou.com/>   |
| Netease Music             | netease      | <https://music.163.com/>  |
| Baidu Music               | baidu        | <http://music.baidu.com/> |
| Xiami Music               | xiami        | <https://www.xiami.com/>  |
| Lossless Music From Baidu | flac         | <http://music.baidu.com/> |

Welcome to submit plugins to support more music sources! Refer to the files in `extractors`.

![](https://github.com/0xHJK/music-dl/raw/master/static/fork.png)

## Credits

- <https://github.com/requests/requests>
- <https://github.com/soimort/you-get>
- <https://github.com/maicong/music>
- <https://github.com/YongHaoWu/NeteaseCloudMusicFlac>

## LICENSE

[MIT License](https://github.com/0xHJK/music-dl/blob/master/LICENSE)
