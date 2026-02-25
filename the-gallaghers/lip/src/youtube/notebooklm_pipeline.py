"""
YouTube NotebookLM 直通模式
绕过IP限制，直接让NotebookLM抓取YouTube
"""
import os
import sys
from typing import List, Dict
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.manager import config_manager
from youtube.parser import YouTubeURLParser
from youtube.extractor import YouTubeExtractor
from storage.notebooklm_sync import NotebookLMSync


class YouTubeNotebookLMPipeline:
    """
    YouTube → NotebookLM 直通管道
    避免服务器IP被YouTube封禁
    """
    
    def __init__(self):
        self.parser = YouTubeURLParser()
        self.extractor = YouTubeExtractor(proxy=None)
        self.sync = NotebookLMSync()
    
    def process_channel(self, channel_name: str) -> Dict:
        """
        处理整个频道 - 直通模式
        
        流程：
        1. 获取频道视频列表（只获取元数据，不下载）
        2. 为每个视频创建NotebookLM笔记（让NotebookLM自己去抓）
        3. 本地只保存视频元数据索引
        """
        print(f"\n{'='*60}")
        print(f"🚀 直通模式处理: {channel_name}")
        print(f"{'='*60}\n")
        
        # 获取频道信息
        channel = config_manager.get_channel(channel_name)
        if not channel:
            return {'success': False, 'error': 'Channel not found'}
        
        # 获取或创建NotebookLM笔记本
        notebook_title = f"学习笔记 - {channel_name}"
        try:
            notebook_id = self.sync.get_or_create_notebook(notebook_title)
            print(f"📚 NotebookLM笔记本: {notebook_title}")
            print(f"   ID: {notebook_id}")
        except Exception as e:
            return {'success': False, 'error': f'Failed to get/create notebook: {e}'}
        
        # 获取视频列表
        print(f"\n正在获取视频列表...")
        try:
            # 使用 --flat-playlist 只获取元数据，不下载
            videos = self.extractor.get_channel_videos(channel['url'], limit=5)
            print(f"✅ 找到 {len(videos)} 个视频")
        except Exception as e:
            return {'success': False, 'error': f'Failed to get video list: {e}'}
        
        # 获取已有的sources避免重复
        existing_sources = self.sync.list_sources(notebook_id)
        existing_urls = {s.get('url', '') for s in existing_sources if s.get('url')}
        existing_titles = {s.get('title', '') for s in existing_sources}
        
        added = 0
        skipped = 0
        failed = 0
        
        print(f"\n开始同步到NotebookLM...")
        print(f"现有 {len(existing_sources)} 个sources\n")
        
        for i, video in enumerate(videos, 1):
            video_url = video['url']
            video_title = video['title']
            video_id = video['id']
            
            print(f"[{i}/{len(videos)}] {video_title[:50]}...")
            
            # 检查是否已存在
            if video_url in existing_urls or video_title in existing_titles:
                print(f"   ⏭️  已存在，跳过")
                skipped += 1
                config_manager.add_analyzed_video(channel_name, video_id)
                continue
            
            # 直接添加YouTube URL到NotebookLM
            # 让NotebookLM自己去抓取，避免IP限制
            try:
                if self.sync.add_youtube_video(notebook_id, video_url, video_title):
                    print(f"   ✅ 已添加到NotebookLM")
                    added += 1
                    
                    # 本地保存元数据（可选）
                    self._save_video_metadata(channel_name, video)
                    
                    # 标记为已处理
                    config_manager.add_analyzed_video(channel_name, video_id)
                else:
                    print(f"   ❌ 添加失败")
                    failed += 1
                    
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                failed += 1
        
        # 更新统计
        config_manager.update_channel_stats(
            channel_name,
            total_videos=len(videos),
            last_analyzed_at=datetime.now().isoformat()
        )
        
        result = {
            'success': True,
            'channel': channel_name,
            'notebook_id': notebook_id,
            'notebook_title': notebook_title,
            'total': len(videos),
            'added': added,
            'skipped': skipped,
            'failed': failed
        }
        
        print(f"\n{'='*60}")
        print(f"✅ 完成: 新增 {added}, 跳过 {skipped}, 失败 {failed}")
        print(f"{'='*60}\n")
        
        return result
    
    def _save_video_metadata(self, channel_name: str, video: Dict):
        """保存视频元数据到本地（供Web面板使用）"""
        # 简化版元数据保存
        metadata_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 
            'notebooks', channel_name
        )
        os.makedirs(metadata_dir, exist_ok=True)
        
        # 创建简单的元数据文件
        import json
        meta_file = os.path.join(metadata_dir, f"{video['id']}_meta.json")
        
        metadata = {
            'video_id': video['id'],
            'title': video['title'],
            'url': video['url'],
            'duration': video.get('duration'),
            'upload_date': video.get('upload_date'),
            'thumbnail': video.get('thumbnail'),
            'processed_at': datetime.now().isoformat(),
            'mode': 'notebooklm_pass_through'
        }
        
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)


# 便捷函数
def process_youtube_channel(channel_name: str) -> Dict:
    """处理YouTube频道的便捷函数"""
    pipeline = YouTubeNotebookLMPipeline()
    return pipeline.process_channel(channel_name)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        result = process_youtube_channel(sys.argv[1])
        print(result)
    else:
        print("Usage: python youtube_notebooklm_pipeline.py <channel_name>")