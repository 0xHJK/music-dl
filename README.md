# music-dl
search and download music 从网易云音乐、虾米音乐、QQ音乐、酷狗音乐、酷我音乐等搜索和下载歌曲

![](./docs/preview.png)

## 使用方式
```bash
python main.py [关键字]
```

## 支持音乐源列表
已支持
- [x] QQ音乐
- [x] 酷狗音乐
- [x] 网易云音乐

待支持
- [ ] 虾米音乐
- [ ] 酷我音乐
- [ ] 百度音乐

欢迎提交插件支持更多音乐源！插件写法参考`core/extractors`中的文件

![](./docs/fork.png)

## TODO
- 支持更多音乐源
- 增加更多定制化参数
    - 指定某个音乐源
    - 自定义数量和翻页
    - 选择音质
- 更友好的交互
    - 搜索进度提示
    - 下载完继续搜索
    - 键盘控制交互

## 致谢
本项目受以下项目启发，参考了其中一部分思路，向这些开发者表示感谢。
- <https://github.com/soimort/you-get>
- <https://github.com/maicong/music>

## LICENSE

WTFPL
