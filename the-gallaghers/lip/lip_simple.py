#!/usr/bin/env python3
"""
Lip 简化版定时任务
直接监控YouTube频道，无需下载视频
"""
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage

# 尝试使用skill的方式获取YouTube内容
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YT_API_AVAILABLE = True
except ImportError:
    YT_API_AVAILABLE = False


class SimpleLipAnalyzer:
    """简化版Lip分析器"""
    
    def __init__(self):
        self.config = config_manager
        self.analyzer = AIAnalyzer()
        self.storage = LocalStorage()
        self.daily_limit = 5
    
    def run(self) -> Dict:
        """执行每日分析"""
        print(f"\n{'='*60}")
        print(f"🤖 Lip 每日分析 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        channels = self.config.get_all_channels()
        if not channels:
            print("⚠️ 没有监控的博主")
            return {'success': True, 'analyzed': 0}
        
        results = []
        total_analyzed = 0
        
        for channel in channels:
            if channel['status'] != 'active':
                continue
            
            print(f"\n📺 {channel['name']}")
            print("-" * 40)
            
            try:
                result = self._process_channel(channel)
                results.append(result)
                total_analyzed += result.get('analyzed', 0)
            except Exception as e:
                print(f"  ❌ 错误: {e}")
                results.append({'channel': channel['name'], 'error': str(e)})
        
        # 发送报告
        self._send_report(results, total_analyzed)
        
        print(f"\n✅ 完成，共分析 {total_analyzed} 条视频")
        return {'success': True, 'analyzed': total_analyzed, 'channels': len(channels)}
    
    def _process_channel(self, channel: Dict) -> Dict:
        """处理单个频道"""
        channel_name = channel['name']
        channel_url = channel['url']
        analyzed_ids = channel.get('analyzed_video_ids', [])
        
        # 获取视频列表（使用yt-dlp获取列表，这个不需要cookies）
        videos = self._get_video_list(channel_url)
        if not videos:
            print(f"  ⚠️ 无法获取视频列表")
            return {'channel': channel_name, 'analyzed': 0}
        
        # 筛选未分析的视频
        new_videos = [v for v in videos if v['id'] not in analyzed_ids]
        if not new_videos:
            print(f"  ✅ 所有视频已分析")
            return {'channel': channel_name, 'analyzed': 0}
        
        to_analyze = new_videos[:self.daily_limit]
        print(f"  发现 {len(new_videos)} 条新视频，分析 {len(to_analyze)} 条")
        
        analyzed_count = 0
        for video in to_analyze:
            success = self._analyze_video(channel_name, video)
            if success:
                analyzed_count += 1
        
        return {'channel': channel_name, 'analyzed': analyzed_count}
    
    def _get_video_list(self, channel_url: str) -> List[Dict]:
        """获取视频列表"""
        import subprocess
        
        # 简化URL处理
        if '/@' in channel_url and '/videos' not in channel_url:
            channel_url = channel_url.rstrip('/') + '/videos'
        
        cmd = [
            'yt-dlp',
            '--flat-playlist',
            '--dump-single-json',
            '--playlist-end', '20',
            '--no-warnings',
            channel_url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return []
            
            data = json.loads(result.stdout)
            return [
                {
                    'id': e.get('id'),
                    'title': e.get('title', 'Unknown'),
                    'url': f"https://www.youtube.com/watch?v={e.get('id')}"
                }
                for e in data.get('entries', [])
                if e.get('id')
            ]
        except:
            return []
    
    def _analyze_video(self, channel_name: str, video: Dict) -> bool:
        """分析单个视频"""
        video_id = video['id']
        print(f"\n  📹 {video['title'][:50]}...")
        
        try:
            # 1. 获取字幕（使用youtube_transcript_api）
            transcript = self._get_transcript(video_id)
            
            if not transcript:
                print(f"    ⚠️ 无字幕，跳过")
                self.config.add_analyzed_video(channel_name, video_id)
                return False
            
            print(f"    字幕: {len(transcript)} 字符")
            
            # 2. AI分析
            print(f"    AI分析中...")
            analysis = self.analyzer.analyze_video(transcript)
            
            # 3. 构建视频信息
            video_info = {
                'id': video_id,
                'title': video['title'],
                'uploader': channel_name,
                'duration': 0,
                'upload_date': datetime.now().strftime('%Y%m%d')
            }
            
            # 4. 保存笔记
            self.storage.save_note(channel_name, video_info, analysis, transcript)
            print(f"    ✅ 已保存")
            
            # 5. 标记为已分析
            self.config.add_analyzed_video(channel_name, video_id)
            return True
            
        except Exception as e:
            print(f"    ❌ 失败: {e}")
            self.config.add_analyzed_video(channel_name, video_id)
            return False
    
    def _get_transcript(self, video_id: str) -> Optional[str]:
        """获取字幕"""
        if not YT_API_AVAILABLE:
            return None
        
        try:
            languages = ['en', 'zh', 'zh-CN', 'zh-TW']
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return ' '.join([item['text'] for item in transcript_list])
        except:
            return None
    
    def _send_report(self, results: List[Dict], total: int):
        """发送日报"""
        lines = [f"📊 Lip日报 ({datetime.now().strftime('%m-%d')})\n"]
        lines.append(f"今日分析: {total} 条\n")
        
        for r in results:
            name = r.get('channel', 'Unknown')
            count = r.get('analyzed', 0)
            error = r.get('error')
            
            if error:
                lines.append(f"❌ {name}: {error}")
            elif count > 0:
                lines.append(f"✅ {name}: {count} 条")
            else:
                lines.append(f"⏸️  {name}: 无新视频")
        
        print("\n" + "\n".join(lines))


def main():
    analyzer = SimpleLipAnalyzer()
    result = analyzer.run()
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()