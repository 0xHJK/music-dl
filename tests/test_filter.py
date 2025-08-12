#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import pytest

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from music_dl import config
from music_dl.song import BasicSong


class TestFilter:
    def setup_method(self):
        # 初始化配置
        config.init()
        
        # 创建测试用的歌曲列表
        self.song1 = BasicSong()
        self.song1.size = 2.5  # 2.5MB
        self.song1._duration = "0:02:30"  # 2分30秒 = 150秒
        
        self.song2 = BasicSong()
        self.song2.size = 8.1  # 8.1MB
        self.song2._duration = "0:04:15"  # 4分15秒 = 255秒
        
        self.song3 = BasicSong()
        self.song3.size = 15.3  # 15.3MB
        self.song3._duration = "0:08:45"  # 8分45秒 = 525秒
        
        self.test_songs = [self.song1, self.song2, self.song3]
    
    def apply_filter(self, songs, filter_str):
        """应用过滤条件，模拟 __main__.py 中的过滤逻辑"""
        filtered_songs = songs
        
        if not filter_str:
            return filtered_songs
        
        # 解析过滤条件
        filter_conditions = filter_str.split(',')
        
        for condition in filter_conditions:
            if not condition:
                continue
                
            result_songs = []
            
            # 大小过滤
            if condition.startswith("size"):
                if ">" in condition:
                    # 大于指定大小
                    size_limit = float(condition.split(">")[1])
                    for song in filtered_songs:
                        if song.size and song.size > size_limit:
                            result_songs.append(song)
                        elif not song.size:  # 如果没有大小信息，保留
                            result_songs.append(song)
                elif "<" in condition:
                    # 小于指定大小
                    size_limit = float(condition.split("<")[1])
                    for song in filtered_songs:
                        if song.size and song.size < size_limit:
                            result_songs.append(song)
                        elif not song.size:  # 如果没有大小信息，保留
                            result_songs.append(song)
                elif "=" in condition:
                    # 等于指定大小
                    size_equal = float(condition.split("=")[1])
                    for song in filtered_songs:
                        if song.size and abs(song.size - size_equal) < 0.01:  # 允许0.01MB的误差
                            result_songs.append(song)
                        elif not song.size:  # 如果没有大小信息，保留
                            result_songs.append(song)
            
            # 长度过滤
            elif condition.startswith("length"):
                if ">" in condition:
                    # 大于指定长度
                    length_limit = int(condition.split(">")[1])
                    for song in filtered_songs:
                        if song._duration:  # 确保有时长信息
                            duration_parts = song._duration.split(":")
                            # 转换为秒
                            if len(duration_parts) == 3:  # H:M:S
                                duration_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + int(duration_parts[2])
                            elif len(duration_parts) == 2:  # M:S
                                duration_seconds = int(duration_parts[0]) * 60 + int(duration_parts[1])
                            else:  # S
                                duration_seconds = int(duration_parts[0])
                            
                            if duration_seconds > length_limit:
                                result_songs.append(song)
                        else:
                            result_songs.append(song)  # 如果没有时长信息，保留
                elif "<" in condition:
                    # 小于指定长度
                    length_limit = int(condition.split("<")[1])
                    for song in filtered_songs:
                        if song._duration:  # 确保有时长信息
                            duration_parts = song._duration.split(":")
                            # 转换为秒
                            if len(duration_parts) == 3:  # H:M:S
                                duration_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + int(duration_parts[2])
                            elif len(duration_parts) == 2:  # M:S
                                duration_seconds = int(duration_parts[0]) * 60 + int(duration_parts[1])
                            else:  # S
                                duration_seconds = int(duration_parts[0])
                            
                            if duration_seconds < length_limit:
                                result_songs.append(song)
                        else:
                            result_songs.append(song)  # 如果没有时长信息，保留
                elif "=" in condition:
                    # 等于指定长度
                    length_equal = int(condition.split("=")[1])
                    for song in filtered_songs:
                        if song._duration:  # 确保有时长信息
                            duration_parts = song._duration.split(":")
                            # 转换为秒
                            if len(duration_parts) == 3:  # H:M:S
                                duration_seconds = int(duration_parts[0]) * 3600 + int(duration_parts[1]) * 60 + int(duration_parts[2])
                            elif len(duration_parts) == 2:  # M:S
                                duration_seconds = int(duration_parts[0]) * 60 + int(duration_parts[1])
                            else:  # S
                                duration_seconds = int(duration_parts[0])
                            
                            if duration_seconds == length_equal:
                                result_songs.append(song)
                        else:
                            result_songs.append(song)  # 如果没有时长信息，保留
            
            # 更新歌曲列表，用于下一个条件过滤
            filtered_songs = result_songs
            
        return filtered_songs
    
    def test_size_filter_greater_than(self):
        """测试大小过滤 - 大于指定值"""
        filtered = self.apply_filter(self.test_songs, "size>10")
        assert len(filtered) == 1
        assert filtered[0] == self.song3
    
    def test_size_filter_less_than(self):
        """测试大小过滤 - 小于指定值"""
        filtered = self.apply_filter(self.test_songs, "size<5")
        assert len(filtered) == 1
        assert filtered[0] == self.song1
    
    def test_size_filter_equal(self):
        """测试大小过滤 - 等于指定值"""
        filtered = self.apply_filter(self.test_songs, "size=8.1")
        assert len(filtered) == 1
        assert filtered[0] == self.song2
    
    def test_length_filter_greater_than(self):
        """测试长度过滤 - 大于指定值"""
        filtered = self.apply_filter(self.test_songs, "length>300")
        assert len(filtered) == 1
        assert filtered[0] == self.song3
    
    def test_length_filter_less_than(self):
        """测试长度过滤 - 小于指定值"""
        filtered = self.apply_filter(self.test_songs, "length<200")
        assert len(filtered) == 1
        assert filtered[0] == self.song1
    
    def test_combined_filters(self):
        """测试组合过滤条件"""
        filtered = self.apply_filter(self.test_songs, "size>5,length<300")
        assert len(filtered) == 1
        assert filtered[0] == self.song2
    
    def test_combined_filters_complex(self):
        """测试复杂组合过滤条件"""
        filtered = self.apply_filter(self.test_songs, "size>2,size<10,length>200")
        assert len(filtered) == 1
        assert filtered[0] == self.song2
    
    def test_range_filter(self):
        """测试范围过滤（通过组合大于小于条件）"""
        filtered = self.apply_filter(self.test_songs, "size>5,size<10")
        assert len(filtered) == 1
        assert filtered[0] == self.song2 