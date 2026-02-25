#!/usr/bin/env python3
"""
Lip 完整工作流
RSS获取视频 → NotebookLM分析 → AI生成科普 → 同步飞书
"""
import os
import sys
import json
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage


class LipWorkflow:
    """Lip完整工作流"""
    
    def __init__(self):
        self.config = config_manager
        self.analyzer = AIAnalyzer()
        self.storage = LocalStorage()
        self.daily_limit = 5
        self.notebooklm_bin = os.path.expanduser('~/.local/bin/notebooklm')
    
    def run(self) -> Dict:
        """执行每日完整工作流"""
        print(f"\n{'='*60}")
        print(f"🤖 Lip 每日工作流 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        channels = self.config.get_all_channels()
        if not channels:
            print("⚠️ 没有监控的博主")
            return {'success': True, 'processed': 0}
        
        results = []
        total_processed = 0
        
        for channel in channels:
            if channel['status'] != 'active':
                continue
            
            print(f"\n📺 {channel['name']}")
            print("-" * 40)
            
            try:
                result = self._process_channel(channel)
                results.append(result)
                total_processed += result.get('processed', 0)
            except Exception as e:
                print(f"  ❌ 错误: {e}")
                import traceback
                traceback.print_exc()
                results.append({'channel': channel['name'], 'error': str(e)})
        
        # 同步到飞书
        print(f"\n📱 同步到飞书...")
        self._sync_to_feishu()
        
        # 发送报告
        self._send_report(results, total_processed)
        
        print(f"\n✅ 完成，共处理 {total_processed} 条视频")
        return {'success': True, 'processed': total_processed}
    
    def _process_channel(self, channel: Dict) -> Dict:
        """处理单个频道"""
        channel_name = channel['name']
        analyzed_ids = channel.get('analyzed_video_ids', [])
        
        # 1. 获取视频列表（RSS方式，无需cookies）
        videos = self._get_videos_rss(channel)
        if not videos:
            print(f"  ⚠️ 无法获取视频列表")
            return {'channel': channel_name, 'processed': 0}
        
        # 筛选新视频
        new_videos = [v for v in videos if v['id'] not in analyzed_ids]
        if not new_videos:
            print(f"  ✅ 所有视频已处理")
            return {'channel': channel_name, 'processed': 0}
        
        to_process = new_videos[:self.daily_limit]
        print(f"  发现 {len(new_videos)} 条新视频，处理 {len(to_process)} 条")
        
        # 2. 处理每个视频
        processed_count = 0
        for video in to_process:
            success = self._process_video(channel_name, video)
            if success:
                processed_count += 1
                self.config.add_analyzed_video(channel_name, video['id'])
        
        return {'channel': channel_name, 'processed': processed_count}
    
    def _get_videos_rss(self, channel: Dict) -> List[Dict]:
        """通过RSS获取视频列表"""
        channel_name = channel['name']
        
        # 尝试构建RSS URL
        # 优先使用channel_id，如果没有则尝试handle
        channel_id = channel.get('channel_id')
        
        if not channel_id:
            # 尝试从URL提取
            url = channel.get('url', '')
            match = re.search(r'channel/(UC[\w-]+)', url)
            if match:
                channel_id = match.group(1)
                # 保存到配置
                channel['channel_id'] = channel_id
                self.config.save()
        
        if channel_id:
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            videos = self._fetch_rss(rss_url)
            if videos:
                return videos
        
        # RSS失败，尝试yt-dlp获取列表（只需要视频ID）
        return self._get_videos_ytdlp(channel.get('url', ''))
    
    def _fetch_rss(self, rss_url: str) -> List[Dict]:
        """获取RSS feed"""
        try:
            req = urllib.request.Request(
                rss_url,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; Bot/0.1)'}
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()
            
            # 解析XML
            root = ET.fromstring(data)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'yt': 'http://www.youtube.com/xml/schemas/2015',
                'media': 'http://search.yahoo.com/mrss/'
            }
            
            videos = []
            for entry in root.findall('atom:entry', ns)[:20]:
                video_id = entry.find('yt:videoId', ns)
                title = entry.find('atom:title', ns)
                published = entry.find('atom:published', ns)
                
                if video_id is not None and title is not None:
                    videos.append({
                        'id': video_id.text,
                        'title': title.text,
                        'url': f"https://www.youtube.com/watch?v={video_id.text}",
                        'published': published.text if published is not None else ''
                    })
            
            return videos
            
        except Exception as e:
            print(f"  RSS获取失败: {e}")
            return []
    
    def _get_videos_ytdlp(self, channel_url: str) -> List[Dict]:
        """使用yt-dlp获取视频列表（备选）"""
        if not channel_url:
            return []
        
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
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return []
            
            data = json.loads(result.stdout)
            return [
                {
                    'id': e.get('id'),
                    'title': e.get('title', 'Unknown'),
                    'url': f"https://www.youtube.com/watch?v={e.get('id')}",
                    'published': ''
                }
                for e in data.get('entries', []) if e.get('id')
            ]
            
        except Exception as e:
            print(f"  yt-dlp获取失败: {e}")
            return []
    
    def _process_video(self, channel_name: str, video: Dict) -> bool:
        """处理单个视频"""
        print(f"\n  📹 {video['title'][:50]}...")
        
        try:
            # 1. 添加到NotebookLM
            notebook_title = f"学习笔记 - {channel_name}"
            added = self._add_to_notebooklm(video, notebook_title)
            
            if not added:
                print(f"    ⚠️ NotebookLM添加失败，继续本地处理")
            else:
                print(f"    ✅ 已添加到NotebookLM")
            
            # 2. 生成科普名词解释（基于NotebookLM摘要）
            print(f"    生成科普解释...")
            knowledge = self._generate_knowledge(video, notebook_title)
            
            # 3. 保存到本地（包含NotebookLM链接和科普）
            note_data = {
                'video': video,
                'knowledge': knowledge,
                'notebooklm_added': added,
                'processed_at': datetime.now().isoformat()
            }
            
            self._save_note(channel_name, note_data)
            print(f"    ✅ 已保存笔记（含{len(knowledge)}条科普）")
            
            return True
            
        except Exception as e:
            print(f"    ❌ 处理失败: {e}")
            return False
    
    def _add_to_notebooklm(self, video: Dict, notebook_title: str) -> bool:
        """添加视频到NotebookLM"""
        try:
            # 获取或创建notebook
            notebook_id = self._get_or_create_notebook(notebook_title)
            if not notebook_id:
                return False
            
            # 切换到该notebook
            subprocess.run(
                [self.notebooklm_bin, 'use', notebook_id],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=30
            )
            
            # 添加视频source
            result = subprocess.run(
                [self.notebooklm_bin, 'source', 'add', video['url']],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"    NotebookLM错误: {e}")
            return False
    
    def _get_or_create_notebook(self, title: str) -> Optional[str]:
        """获取或创建NotebookLM笔记本"""
        try:
            # 列出notebooks
            result = subprocess.run(
                [self.notebooklm_bin, 'list'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            # 查找现有notebook
            for line in result.stdout.split('\n'):
                if title in line:
                    # 提取ID（第一列）
                    parts = line.split()
                    if parts:
                        return parts[0]
            
            # 创建新notebook
            result = subprocess.run(
                [self.notebooklm_bin, 'create', title],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # 重新获取ID
                result = subprocess.run(
                    [self.notebooklm_bin, 'list'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=30
                )
                
                for line in result.stdout.split('\n'):
                    if title in line:
                        parts = line.split()
                        if parts:
                            return parts[0]
            
            return None
            
        except Exception as e:
            print(f"  Notebook操作失败: {e}")
            return None
    
    def _generate_knowledge(self, video: Dict, notebook_title: str) -> Dict[str, str]:
        """生成科普名词解释"""
        # 从NotebookLM获取视频分析摘要
        summary = self._get_notebooklm_summary(notebook_title, video['title'])
        
        if not summary:
            print(f"    ⚠️ 无法从NotebookLM获取摘要")
            return {}
        
        # 用AI基于摘要生成科普
        try:
            from ai.analyzer import AIAnalyzer
            analyzer = AIAnalyzer()
            
            print(f"    基于NotebookLM摘要生成科普...")
            knowledge = analyzer.generate_knowledge_from_summary(video['title'], summary)
            
            print(f"    生成 {len(knowledge)} 条科普")
            return knowledge
            
        except Exception as e:
            print(f"    科普生成失败: {e}")
            return {}
    
    def _get_notebooklm_summary(self, notebook_title: str, video_title: str) -> str:
        """从NotebookLM获取视频分析摘要"""
        try:
            # 先切换到对应notebook
            notebook_id = self._get_or_create_notebook(notebook_title)
            if not notebook_id:
                return ""
            
            subprocess.run(
                [self.notebooklm_bin, 'use', notebook_id],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=30
            )
            
            # 向NotebookLM询问视频摘要
            question = f"请总结视频'{video_title}'的核心内容和主要观点（3-5句话）"
            
            result = subprocess.run(
                [self.notebooklm_bin, 'ask', question],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            
            return ""
            
        except Exception as e:
            print(f"    获取NotebookLM摘要失败: {e}")
            return ""
    
    def _save_note(self, channel_name: str, note_data: Dict):
        """保存笔记到本地"""
        # 保存为JSON
        channel_dir = os.path.join(self.storage.base_dir, channel_name)
        os.makedirs(channel_dir, exist_ok=True)
        
        video_id = note_data['video']['id']
        filepath = os.path.join(channel_dir, f"{video_id}_workflow.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)
    
    def _sync_to_feishu(self):
        """同步到飞书"""
        try:
            from storage.feishu_sync import FeishuDocSync
            
            sync = FeishuDocSync()
            
            # 遍历所有频道的笔记
            for channel_name in os.listdir(self.storage.base_dir):
                channel_dir = os.path.join(self.storage.base_dir, channel_name)
                if not os.path.isdir(channel_dir):
                    continue
                
                # 获取所有workflow笔记
                workflow_files = [f for f in os.listdir(channel_dir) if f.endswith('_workflow.json')]
                if not workflow_files:
                    continue
                
                print(f"  同步 {channel_name}: {len(workflow_files)} 条笔记")
                
                # 生成飞书文档内容
                content = self._generate_feishu_content(channel_name, channel_dir, workflow_files)
                
                # 获取或创建文档
                doc_url = sync.get_or_create_channel_doc(channel_name)
                if doc_url:
                    # 写入内容
                    sync.write_to_feishu_doc(doc_url, content)
                    print(f"    ✅ 已同步到飞书")
                
        except Exception as e:
            print(f"  ❌ 飞书同步失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_feishu_content(self, channel_name: str, channel_dir: str, workflow_files: list) -> str:
        """生成飞书文档内容"""
        from datetime import datetime
        
        lines = [f"# 学习笔记 - {channel_name}\n"]
        lines.append(f"*最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        lines.append("---\n\n")
        
        # 按时间倒序排列
        workflow_files.sort(reverse=True)
        
        for filename in workflow_files:
            filepath = os.path.join(channel_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            video = data.get('video', {})
            knowledge = data.get('knowledge', {})
            processed_at = data.get('processed_at', '')
            
            # 视频标题和链接
            lines.append(f"## {video.get('title', 'Untitled')}\n")
            lines.append(f"📺 [观看视频]({video.get('url', '')})\n")
            lines.append(f"⏰ 处理时间: {processed_at[:10] if processed_at else 'N/A'}\n\n")
            
            # NotebookLM链接
            notebooklm_added = data.get('notebooklm_added', False)
            if notebooklm_added:
                lines.append(f"🤖 已在NotebookLM中分析\n\n")
            
            # 科普知识
            if knowledge:
                lines.append("### 🎓 科普知识\n")
                for term, explanation in knowledge.items():
                    lines.append(f"- **{term}**: {explanation}\n")
                lines.append("\n")
            
            lines.append("---\n\n")
        
        return ''.join(lines)
    
    def _send_report(self, results: List[Dict], total: int):
        """发送报告"""
        lines = [f"📊 Lip日报 ({datetime.now().strftime('%m-%d')})\n"]
        lines.append(f"今日处理: {total} 条视频\n")
        
        for r in results:
            name = r.get('channel', 'Unknown')
            count = r.get('processed', 0)
            error = r.get('error')
            
            if error:
                lines.append(f"❌ {name}: {error}")
            elif count > 0:
                lines.append(f"✅ {name}: 处理 {count} 条")
            else:
                lines.append(f"⏸️  {name}: 无新视频")
        
        print("\n" + "\n".join(lines))


def main():
    workflow = LipWorkflow()
    result = workflow.run()
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()