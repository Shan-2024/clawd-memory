"""
YouTube视频/字幕提取模块
使用 yt-dlp
"""
import subprocess
import json
import re
from typing import List, Dict, Optional
from datetime import datetime


class YouTubeExtractor:
    """YouTube内容提取器"""
    
    def __init__(self, proxy: str = None):
        self.proxy = proxy
    
    def _run_ytdlp(self, args: List[str]) -> subprocess.CompletedProcess:
        """运行 yt-dlp 命令"""
        import os
        
        cmd = ['yt-dlp'] + args
        if self.proxy:
            cmd.extend(['--proxy', self.proxy])
        
        # 添加cookies支持
        cookies_file = os.path.expanduser('~/.openclaw/workspace/the-gallaghers/lip/cookies/youtube_cookies.txt')
        if os.path.exists(cookies_file):
            cmd.extend(['--cookies', cookies_file])
        
        # Python 3.6兼容性：使用stdout和stderr参数
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=120
        )
        return result
    
    def get_channel_videos(self, channel_url: str, limit: int = 50) -> List[Dict]:
        """
        获取频道的视频列表
        
        Args:
            channel_url: 频道URL
            limit: 最多获取多少条
            
        Returns:
            视频信息列表，按发布时间倒序
        """
        args = [
            '--flat-playlist',
            '--dump-single-json',
            '--playlist-end', str(limit),
            channel_url
        ]
        
        result = self._run_ytdlp(args)
        
        if result.returncode != 0:
            raise Exception(f"获取视频列表失败: {result.stderr}")
        
        try:
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
                    'view_count': entry.get('view_count'),
                    'thumbnail': entry.get('thumbnail')
                }
                videos.append(video)
            
            return videos
            
        except json.JSONDecodeError as e:
            raise Exception(f"解析视频列表失败: {e}")
    
    def get_video_info(self, video_url: str) -> Dict:
        """
        获取单个视频的详细信息
        """
        args = [
            '--dump-single-json',
            '--no-download',
            video_url
        ]
        
        result = self._run_ytdlp(args)
        
        if result.returncode != 0:
            raise Exception(f"获取视频信息失败: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
            return {
                'id': data.get('id'),
                'title': data.get('title'),
                'description': data.get('description'),
                'duration': data.get('duration'),
                'upload_date': data.get('upload_date'),
                'uploader': data.get('uploader'),
                'view_count': data.get('view_count'),
                'thumbnail': data.get('thumbnail'),
                'tags': data.get('tags', []),
                'categories': data.get('categories', [])
            }
        except json.JSONDecodeError as e:
            raise Exception(f"解析视频信息失败: {e}")
    
    def extract_transcript(self, video_url: str, languages: List[str] = None) -> Optional[str]:
        """
        提取视频字幕
        
        Args:
            video_url: 视频URL
            languages: 优先语言列表，如 ['zh', 'zh-CN', 'en', 'en-US']
            
        Returns:
            字幕文本，如果没有字幕返回 None
        """
        if languages is None:
            languages = ['zh', 'zh-CN', 'en', 'en-US', 'zh-Hans', 'zh-TW']
        
        # 尝试自动下载最佳字幕
        args = [
            '--skip-download',
            '--write-auto-subs' if self._has_auto_subs(video_url) else '--write-subs',
            '--sub-langs', ','.join(languages),
            '--convert-subs', 'srt',
            '--print', 'filename',
            '-o', '-',  # 输出到stdout
            video_url
        ]
        
        # 先尝试获取字幕列表
        list_args = [
            '--list-subs',
            '--skip-download',
            video_url
        ]
        
        result = self._run_ytdlp(list_args)
        
        # 检查是否有字幕
        if 'no subtitles' in result.stdout.lower() and 'no automatic captions' in result.stdout.lower():
            return None
        
        # 尝试提取字幕
        extract_args = [
            '--skip-download',
            '--write-subs',
            '--write-auto-subs',
            '--sub-langs', ','.join(languages),
            '--convert-subs', 'srt',
            '--print', 'after_move:filepath',
            '-o', '/tmp/%(id)s.%(ext)s',
            video_url
        ]
        
        result = self._run_ytdlp(extract_args)
        
        if result.returncode != 0:
            # 可能没有字幕
            if 'no subtitles' in result.stderr.lower():
                return None
            raise Exception(f"提取字幕失败: {result.stderr}")
        
        # 解析字幕文件路径
        srt_path = result.stdout.strip().replace('.webm', '.srt').replace('.mp4', '.srt')
        
        # 如果上面的方法没找到，尝试找文件
        if not srt_path or not srt_path.endswith('.srt'):
            video_id = self._extract_video_id(video_url)
            import os
            for lang in languages:
                possible_paths = [
                    f'/tmp/{video_id}.{lang}.srt',
                    f'/tmp/{video_id}.srt',
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        srt_path = path
                        break
                if srt_path and os.path.exists(srt_path):
                    break
        
        if srt_path and srt_path.endswith('.srt') and os.path.exists(srt_path):
            with open(srt_path, 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # 清理字幕文件
            os.remove(srt_path)
            
            # 解析SRT，提取纯文本
            return self._parse_srt(srt_content)
        
        return None
    
    def _has_auto_subs(self, video_url: str) -> bool:
        """检查视频是否有自动字幕"""
        args = ['--list-subs', '--skip-download', video_url]
        result = self._run_ytdlp(args)
        return 'automatic captions' in result.stdout.lower()
    
    def _extract_video_id(self, url: str) -> str:
        """从URL提取视频ID"""
        patterns = [
            r'v=([\w-]+)',
            r'youtu\.be/([\w-]+)',
            r'shorts/([\w-]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ''
    
    def _parse_srt(self, srt_content: str) -> str:
        """
        解析SRT字幕文件，提取纯文本
        """
        lines = srt_content.strip().split('\n')
        text_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过序号行
            if line.isdigit():
                i += 1
                # 跳过时间行
                if i < len(lines) and '-->' in lines[i]:
                    i += 1
                continue
            
            # 跳过时间行
            if '-->' in line:
                i += 1
                continue
            
            # 跳过空行
            if not line:
                i += 1
                continue
            
            # 收集文本
            text_lines.append(line)
            i += 1
        
        # 合并文本并清理
        text = ' '.join(text_lines)
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 规范化空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text


# 便捷函数
def extract_video_transcript(video_url: str, proxy: str = None) -> Optional[str]:
    """提取视频字幕的便捷函数"""
    extractor = YouTubeExtractor(proxy=proxy)
    return extractor.extract_transcript(video_url)


def get_channel_recent_videos(channel_url: str, limit: int = 10, proxy: str = None) -> List[Dict]:
    """获取频道最近视频的便捷函数"""
    extractor = YouTubeExtractor(proxy=proxy)
    return extractor.get_channel_videos(channel_url, limit=limit)