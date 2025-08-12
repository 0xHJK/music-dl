#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@file: player.py
@description: 音乐播放器功能
"""

import os
import sys
import time
import gettext
import click

# 导入用于播放音乐的库
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

gettext.install("music-dl", "locale")

# 导入工具函数
from .utils import colorize


def time_duration_to_seconds(duration):
    """将时间字符串(如'05:30')转换为秒数"""
    if not duration:
        return 0
    
    parts = duration.split(":")
    if len(parts) == 3:  # H:M:S
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:  # M:S
        return int(parts[0]) * 60 + int(parts[1])
    else:  # S
        return int(parts[0])


def play_music(song_files):
    """播放下载的音乐文件"""
    if not PYGAME_AVAILABLE:
        click.echo(_("警告: 未安装pygame库，无法播放音乐。请安装pygame后重试: pip install pygame"))
        return
    
    # 过滤有效文件
    valid_song_files = [f for f in song_files if f and os.path.exists(f)]
    if not valid_song_files:
        click.echo(_("没有有效的音乐文件可播放"))
        return
        
    # 初始化
    pygame.init()
    pygame.mixer.init()
    playing = True
    current_song_index = 0
    current_pos = 0
    
    # 显示帮助
    click.echo(_("\n播放控制: 空格键-暂停/继续  左右方向键-切换歌曲  ,键-后退5秒  .键-前进5秒  q键-退出播放  d键-删除这首歌\n"))

    # 播放第一首
    click.echo(_("\n正在播放: ") + colorize(os.path.basename(valid_song_files[current_song_index]), "highlight"))
    pygame.mixer.music.load(valid_song_files[current_song_index])
    pygame.mixer.music.play()
    
    # 检测键盘输入环境
    try:
        import msvcrt
        is_windows = True
    except ImportError:
        is_windows = False
        try:
            import termios, tty
        except ImportError:
            click.echo(_("警告: 不支持的操作系统，无法捕获键盘输入，将自动播放全部歌曲"))
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            return
    
    # 设置播放位置
    def set_position(seconds):
        nonlocal current_pos
        try:
            sound = pygame.mixer.Sound(valid_song_files[current_song_index])
            song_length = sound.get_length()
        except:
            song_length = 300
        
        pygame.mixer.music.stop()
        new_pos = max(0, min(song_length, seconds))
        current_pos = new_pos
        pygame.mixer.music.load(valid_song_files[current_song_index])
        pygame.mixer.music.play(start=new_pos)
    
    # 删除当前歌曲
    def delete_current_song():
        nonlocal current_song_index, valid_song_files
        
        current_song_file = valid_song_files[current_song_index]
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.mixer.init()
        time.sleep(0.2)
        
        try:
            os.remove(current_song_file)
            click.echo(_("\n已删除: ") + colorize(os.path.basename(current_song_file), "red"))
            valid_song_files.pop(current_song_index)
            
            if not valid_song_files:
                click.echo(_("\n播放列表为空，退出播放"))
                return True
            
            if current_song_index >= len(valid_song_files):
                current_song_index = max(0, len(valid_song_files) - 1)
            
            current_pos = 0
            click.echo(_("\n正在播放: ") + colorize(os.path.basename(valid_song_files[current_song_index]), "highlight"))
            pygame.mixer.music.load(valid_song_files[current_song_index])
            pygame.mixer.music.play()
        except Exception as e:
            click.echo(_("\n删除文件失败: ") + str(e))
        return False
    
    # 获取键盘输入
    def get_key():
        if is_windows:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    return 'space'
                elif key == b'q':
                    return 'q'
                elif key == b',':
                    return 'comma'
                elif key == b'.':
                    return 'dot'
                elif key == b'd':
                    return 'delete'
                elif key == b'\xe0':
                    key = msvcrt.getch()
                    if key == b'K':
                        return 'left'
                    elif key == b'M':
                        return 'right'
            return None
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
            if ch == ' ':
                return 'space'
            elif ch == 'q':
                return 'q'
            elif ch == ',':
                return 'comma'
            elif ch == '.':
                return 'dot'
            elif ch == 'd':
                return 'delete'
            elif ch == '\x1b':
                ch = sys.stdin.read(2)
                if ch == '[D':
                    return 'left'
                elif ch == '[C':
                    return 'right'
            return None
    
    # 主循环
    while True:
        time.sleep(0.1)
        
        if playing and pygame.mixer.music.get_busy():
            current_pos += 0.1
        
        # 播放下一首
        if not pygame.mixer.music.get_busy() and playing:
            current_song_index += 1
            if current_song_index >= len(valid_song_files):
                click.echo(_("\n播放列表已播放完毕"))
                break
            
            current_pos = 0
            click.echo(_("\n正在播放: ") + colorize(os.path.basename(valid_song_files[current_song_index]), "highlight"))
            pygame.mixer.music.load(valid_song_files[current_song_index])
            pygame.mixer.music.play()
        
        # 处理按键
        key = get_key()
        if key == 'space':
            if playing:
                pygame.mixer.music.pause()
                playing = False
            else:
                pygame.mixer.music.unpause()
                playing = True
        
        elif key == 'left':
            current_song_index = max(0, current_song_index - 1)
            current_pos = 0
            click.echo(_("\n正在播放: ") + colorize(os.path.basename(valid_song_files[current_song_index]), "highlight"))
            pygame.mixer.music.load(valid_song_files[current_song_index])
            pygame.mixer.music.play()
            playing = True
        
        elif key == 'right':
            current_song_index = min(len(valid_song_files) - 1, current_song_index + 1)
            current_pos = 0
            click.echo(_("\n正在播放: ") + colorize(os.path.basename(valid_song_files[current_song_index]), "highlight"))
            pygame.mixer.music.load(valid_song_files[current_song_index])
            pygame.mixer.music.play()
            playing = True
        
        elif key == 'comma':
            set_position(current_pos - 5)
            playing = True
        
        elif key == 'dot':
            set_position(current_pos + 5)
            playing = True
        
        elif key == 'delete':
            should_exit = delete_current_song()
            if should_exit:
                break
            playing = True
        
        elif key == 'q':
            pygame.mixer.music.stop()
            break
    
    pygame.mixer.quit()
    pygame.quit()
    click.echo(_("\n播放结束")) 