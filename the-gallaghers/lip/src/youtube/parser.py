"""
YouTube链接解析模块
支持：频道主页、播放列表、单个视频
"""
import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Optional


class YouTubeURLParser:
    """YouTube URL解析器"""
    
    # 各种YouTube URL模式
    PATTERNS = {
        'channel': [
            r'youtube\.com/@([\w.-]+)',  # @username
            r'youtube\.com/c/([\w.-]+)',  # /c/customname
            r'youtube\.com/channel/([\w-]+)',  # /channel/UCxxx
        ],
        'playlist': [
            r'youtube\.com/playlist\?list=([\w-]+)',  # 播放列表
        ],
        'video': [
            r'youtube\.com/watch\?v=([\w-]+)',  # 普通视频
            r'youtu\.be/([\w-]+)',  # 短链接
            r'youtube\.com/shorts/([\w-]+)',  # Shorts
        ]
    }
    
    @classmethod
    def parse(cls, url: str) -> Dict[str, str]:
        """
        解析YouTube URL
        
        Returns:
            {
                'type': 'channel' | 'playlist' | 'video' | 'unknown',
                'id': str,  # channel_id, playlist_id 或 video_id
                'url': str  # 标准化后的URL
            }
        """
        url = url.strip()
        
        # 检查频道链接
        for pattern in cls.PATTERNS['channel']:
            match = re.search(pattern, url)
            if match:
                identifier = match.group(1)
                # 区分不同类型的频道ID
                if url.startswith('youtube.com/channel/'):
                    return {
                        'type': 'channel',
                        'id': identifier,
                        'id_type': 'channel_id',
                        'url': f'https://www.youtube.com/channel/{identifier}'
                    }
                else:
                    return {
                        'type': 'channel',
                        'id': identifier,
                        'id_type': 'handle',
                        'url': f'https://www.youtube.com/@{identifier}'
                    }
        
        # 检查播放列表链接
        for pattern in cls.PATTERNS['playlist']:
            match = re.search(pattern, url)
            if match:
                playlist_id = match.group(1)
                return {
                    'type': 'playlist',
                    'id': playlist_id,
                    'url': f'https://www.youtube.com/playlist?list={playlist_id}'
                }
        
        # 检查视频链接
        for pattern in cls.PATTERNS['video']:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return {
                    'type': 'video',
                    'id': video_id,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
                }
        
        return {
            'type': 'unknown',
            'id': None,
            'url': url
        }
    
    @classmethod
    def extract_video_id(cls, url: str) -> Optional[str]:
        """从URL中提取视频ID"""
        parsed = cls.parse(url)
        return parsed['id'] if parsed['type'] == 'video' else None
    
    @classmethod
    def is_valid_youtube_url(cls, url: str) -> bool:
        """检查是否是有效的YouTube URL"""
        parsed = cls.parse(url)
        return parsed['type'] != 'unknown'