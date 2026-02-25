#!/usr/bin/env python3
"""
Lip 超简化版 - 直接模式
只做一件事：获取视频列表 → 推送到NotebookLM
"""
import os
import sys
import json
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager


class SimpleLip:
    """超简化Lip - 只推送到NotebookLM"""
    
    def __init__(self):
        self.config = config_manager
        self.daily_limit = 5
    
    def run(self) -> Dict:
        """执行每日任务"""
        print(f"\n{'='*60}")
        print(f"🤖 Lip 每日推送 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        channels = self.config.get_all_channels()
        if not channels:
            print("⚠️ 没有监控的博主")
            return {'success': True, 'added': 0}
        
        results = []
        total_added = 0
        
        for channel in channels:
            if channel['status'] != 'active':
                continue
            
            print(f"\n📺 {channel['name']}")
            print("-" * 40)
            
            try:
                result = self._process_channel(channel)
                results.append(result)
                total_added += result.get('added', 0)
            except Exception as e:
                print(f"  ❌ 错误: {e}")
                results.append({'channel': channel['name'], 'error': str(e)})
        
        # 发送报告
        self._send_report(results, total_added)
        
        print(f"\n✅ 完成，共推送 {total_added} 条视频到NotebookLM")
        return {'success': True, 'added': total_added}
    
    def _process_channel(self, channel: Dict) -> Dict:
        """处理单个频道"""
        channel_name = channel['name']
        channel_url = channel['url']
        analyzed_ids = channel.get('analyzed_video_ids', [])
        
        # 获取视频列表（只需要ID和标题）
        videos = self._get_video_list(channel_url)
        if not videos:
            print(f"  ⚠️ 无法获取视频列表")
            return {'channel': channel_name, 'added': 0}
        
        # 筛选未处理的新视频
        new_videos = [v for v in videos if v['id'] not in analyzed_ids]
        if not new_videos:
            print(f"  ✅ 所有视频已处理")
            return {'channel': channel_name, 'added': 0}
        
        to_add = new_videos[:self.daily_limit]
        print(f"  发现 {len(new_videos)} 条新视频，推送 {len(to_add)} 条")
        
        # 推送到NotebookLM
        notebook_title = f"学习笔记 - {channel_name}"
        added_count = 0
        
        for video in to_add:
            success = self._add_to_notebooklm(video, notebook_title)
            if success:
                added_count += 1
                # 标记为已处理
                self.config.add_analyzed_video(channel_name, video['id'])
        
        return {'channel': channel_name, 'added': added_count}
    
    def _get_video_list(self, channel_url: str) -> List[Dict]:
        """获取视频列表（轻量级，不需要cookies）"""
        # 尝试使用简单的HTTP请求获取RSS
        # YouTube频道RSS: https://www.youtube.com/feeds/videos.xml?channel_id=...
        
        # 先提取channel ID或handle
        channel_id = self._extract_channel_identifier(channel_url)
        if not channel_id:
            return []
        
        # 尝试RSS方式
        rss_url = None
        if channel_id.startswith('UC'):
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        elif channel_id.startswith('@'):
            # handle方式，需要先解析
            pass
        
        if rss_url:
            try:
                import urllib.request
                import xml.etree.ElementTree as ET
                
                req = urllib.request.Request(
                    rss_url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = response.read()
                
                # 解析RSS
                root = ET.fromstring(data)
                ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
                
                videos = []
                for entry in root.findall('atom:entry', ns)[:20]:
                    video_id = entry.find('yt:videoId', ns)
                    title = entry.find('atom:title', ns)
                    if video_id is not None and title is not None:
                        videos.append({
                            'id': video_id.text,
                            'title': title.text,
                            'url': f"https://www.youtube.com/watch?v={video_id.text}"
                        })
                
                return videos
            except Exception as e:
                print(f"  RSS获取失败: {e}")
        
        # RSS失败，尝试yt-dlp（只需要列表，不需要详情）
        return self._get_video_list_ytdlp(channel_url)
    
    def _extract_channel_identifier(self, url: str) -> Optional[str]:
        """提取频道标识符"""
        # 尝试提取channel ID
        match = re.search(r'channel/(UC[\w-]+)', url)
        if match:
            return match.group(1)
        
        # 尝试提取handle
        match = re.search(r'@([\w-]+)', url)
        if match:
            return f"@{match.group(1)}"
        
        return None
    
    def _get_video_list_ytdlp(self, channel_url: str) -> List[Dict]:
        """使用yt-dlp获取列表（备选）"""
        # 处理URL
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
                {'id': e.get('id'), 'title': e.get('title', 'Unknown'), 
                 'url': f"https://www.youtube.com/watch?v={e.get('id')}"}
                for e in data.get('entries', []) if e.get('id')
            ]
        except:
            return []
    
    def _add_to_notebooklm(self, video: Dict, notebook_title: str) -> bool:
        """添加视频到NotebookLM"""
        try:
            print(f"    📹 {video['title'][:40]}...")
            
            # 1. 创建或获取notebook
            notebook_id = self._get_or_create_notebook(notebook_title)
            if not notebook_id:
                return False
            
            # 2. 添加视频为source
            cmd = [
                '~/.local/bin/notebooklm', 'source', 'add', video['url']
            ]
            
            result = subprocess.run(
                ' '.join(cmd),
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"      ✅ 已添加")
                return True
            else:
                print(f"      ❌ 失败: {result.stderr[:100]}")
                return False
                
        except Exception as e:
            print(f"      ❌ 错误: {e}")
            return False
    
    def _get_or_create_notebook(self, title: str) -> Optional[str]:
        """获取或创建NotebookLM笔记本"""
        try:
            # 列出所有notebooks
            result = subprocess.run(
                ['~/.local/bin/notebooklm', 'list', '--json'],
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                # 创建新notebook
                result = subprocess.run(
                    f"~/.local/bin/notebooklm create '{title}'",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    # 重新获取ID
                    result = subprocess.run(
                        ['~/.local/bin/notebooklm', 'list', '--json'],
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
            
            # 解析找到notebook ID
            import re
            match = re.search(r'([a-zA-Z0-9_-]+)\s+' + re.escape(title), result.stdout)
            if match:
                return match.group(1)
            
            return None
            
        except Exception as e:
            print(f"  Notebook操作失败: {e}")
            return None
    
    def _send_report(self, results: List[Dict], total: int):
        """发送报告"""
        lines = [f"📊 Lip推送日报 ({datetime.now().strftime('%m-%d')})\n"]
        lines.append(f"今日推送: {total} 条到NotebookLM\n")
        
        for r in results:
            name = r.get('channel', 'Unknown')
            count = r.get('added', 0)
            error = r.get('error')
            
            if error:
                lines.append(f"❌ {name}: {error}")
            elif count > 0:
                lines.append(f"✅ {name}: 推送 {count} 条")
            else:
                lines.append(f"⏸️  {name}: 无新视频")
        
        print("\n" + "\n".join(lines))


def main():
    lip = SimpleLip()
    result = lip.run()
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()