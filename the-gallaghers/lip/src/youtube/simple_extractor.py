#!/usr/bin/env python3
"""
简化的YouTube内容获取模块
使用 youtube-transcript-api 和 yt-dlp（带cookies备选）
"""
import os
import json
import re
import subprocess
from typing import List, Dict, Optional
from datetime import datetime

# 尝试导入youtube_transcript_api
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    YT_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YT_TRANSCRIPT_AVAILABLE = False
    print("⚠️ youtube_transcript_api not available")


class SimpleYouTubeExtractor:
    """简化版YouTube提取器"""
    
    def __init__(self):
        self.cookies_file = os.path.expanduser(
            '~/.openclaw/workspace/the-gallaghers/lip/cookies/youtube_cookies.txt'
        )
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """从URL提取视频ID"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'  # 直接是ID
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_transcript(self, video_id: str, languages: List[str] = None) -> Optional[str]:
        """
        获取视频字幕
        
        优先使用youtube_transcript_api，失败则返回None
        """
        if not YT_TRANSCRIPT_AVAILABLE:
            return None
        
        if languages is None:
            languages = ['en', 'zh', 'zh-CN', 'zh-TW', 'ja', 'ko']
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return ' '.join([item['text'] for item in transcript_list])
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            print(f"  获取字幕失败: {e}")
            return None
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """
        获取视频信息
        
        使用yt-dlp，带cookies支持
        """
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--skip-download',
            '--no-warnings'
        ]
        
        # 添加cookies如果存在
        if os.path.exists(self.cookies_file):
            cmd.extend(['--cookies', self.cookies_file])
        
        cmd.append(url)
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # 如果有错误但返回了输出，尝试解析
                if not result.stdout:
                    return None
            
            data = json.loads(result.stdout.strip().split('\n')[0])
            
            return {
                'id': data.get('id'),
                'title': data.get('title'),
                'uploader': data.get('uploader'),
                'duration': data.get('duration'),
                'upload_date': data.get('upload_date'),
                'view_count': data.get('view_count'),
                'thumbnail': data.get('thumbnail'),
                'description': data.get('description', '')[:500]  # 限制长度
            }
            
        except Exception as e:
            print(f"  获取视频信息失败: {e}")
            return None
    
    def get_channel_videos(self, channel_url: str, limit: int = 10) -> List[Dict]:
        """
        获取频道视频列表
        
        使用yt-dlp获取视频列表
        """
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--dump-single-json',
            '--playlist-end', str(limit),
            '--no-warnings'
        ]
        
        # 添加cookies如果存在
        if os.path.exists(self.cookies_file):
            cmd.extend(['--cookies', self.cookies_file])
        
        # 处理频道URL
        if '/@' in channel_url and '/videos' not in channel_url:
            channel_url = channel_url.rstrip('/') + '/videos'
        
        cmd.append(channel_url)
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"  获取频道视频失败: {result.stderr[:200]}")
                return []
            
            data = json.loads(result.stdout)
            entries = data.get('entries', [])
            
            videos = []
            for entry in entries:
                video = {
                    'id': entry.get('id'),
                    'title': entry.get('title', 'Unknown'),
                    'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                    'duration': entry.get('duration'),
                    'upload_date': entry.get('upload_date'),
                }
                if video['id']:
                    videos.append(video)
            
            return videos
            
        except Exception as e:
            print(f"  解析频道视频失败: {e}")
            return []


# 便捷函数
def get_video_transcript(video_id_or_url: str) -> Optional[str]:
    """获取视频字幕的便捷函数"""
    extractor = SimpleYouTubeExtractor()
    video_id = extractor.extract_video_id(video_id_or_url)
    if not video_id:
        return None
    return extractor.get_transcript(video_id)


def analyze_youtube_video(video_id_or_url: str) -> Optional[Dict]:
    """
    分析YouTube视频的便捷函数
    
    Returns:
        包含视频信息和字幕的字典
    """
    extractor = SimpleYouTubeExtractor()
    video_id = extractor.extract_video_id(video_id_or_url)
    
    if not video_id:
        return None
    
    print(f"📹 分析视频: {video_id}")
    
    # 获取信息
    info = extractor.get_video_info(video_id)
    if not info:
        return None
    
    print(f"  标题: {info['title'][:50]}...")
    
    # 获取字幕
    transcript = extractor.get_transcript(video_id)
    if transcript:
        print(f"  字幕: {len(transcript)} 字符")
    else:
        print(f"  ⚠️ 无字幕")
    
    return {
        'info': info,
        'transcript': transcript,
        'has_transcript': transcript is not None
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_extractor.py <video_id_or_url>")
        sys.exit(1)
    
    video_input = sys.argv[1]
    result = analyze_youtube_video(video_input)
    
    if result:
        print("\n✅ 成功:")
        print(json.dumps(result['info'], indent=2, ensure_ascii=False))
        if result['transcript']:
            print(f"\n字幕预览: {result['transcript'][:200]}...")
    else:
        print("\n❌ 失败")