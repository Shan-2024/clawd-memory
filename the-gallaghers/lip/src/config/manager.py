"""
配置管理模块
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
NOTEBOOKS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')


class ConfigManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or CONFIG_PATH
        self.notebooks_dir = NOTEBOOKS_DIR
        self._config = None
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.notebooks_dir, exist_ok=True)
    
    def load(self) -> Dict:
        """加载配置文件"""
        if self._config is None:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            else:
                self._config = self._default_config()
        return self._config
    
    def save(self):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "version": "1.0",
            "max_channels": 10,
            "daily_limit_per_channel": 5,
            "channels": [],
            "settings": {
                "auto_sync_feishu": False,
                "auto_sync_notebooklm": False,
                "analysis_model": "kimi-k2.5",
                "proxy": None
            }
        }
    
    def add_channel(self, url: str, name: str, display_name: str = None) -> Dict:
        """添加新频道"""
        config = self.load()
        
        if len(config['channels']) >= config['max_channels']:
            raise ValueError(f"已达到最大频道数量限制 ({config['max_channels']})")
        
        # 生成唯一ID
        channel_id = f"ch_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        channel = {
            "id": channel_id,
            "url": url,
            "name": name,
            "display_name": display_name or name,
            "added_at": datetime.now().isoformat(),
            "status": "active",
            "analysis_mode": "local",  # 分析模式: local=本地AI, pass_through=直通模式
            "stats": {
                "total_videos": 0,
                "analyzed_count": 0,
                "last_analyzed_at": None
            },
            "sync_to_feishu": False,
            "feishu_doc_token": None,
            "analyzed_video_ids": []  # 已分析的视频ID列表
        }
        
        config['channels'].append(channel)
        self.save()
        
        # 创建博主笔记本目录
        channel_dir = os.path.join(self.notebooks_dir, name)
        os.makedirs(channel_dir, exist_ok=True)
        
        return channel
    
    def remove_channel(self, name: str) -> bool:
        """删除频道"""
        config = self.load()
        original_count = len(config['channels'])
        config['channels'] = [c for c in config['channels'] if c['name'] != name]
        
        if len(config['channels']) < original_count:
            self.save()
            return True
        return False
    
    def get_channel(self, name: str) -> Optional[Dict]:
        """获取频道信息"""
        config = self.load()
        for channel in config['channels']:
            if channel['name'] == name or channel['display_name'] == name:
                return channel
        return None
    
    def get_all_channels(self) -> List[Dict]:
        """获取所有频道"""
        config = self.load()
        return config['channels']
    
    def update_channel_stats(self, name: str, total_videos: int = None, 
                            analyzed_count: int = None, 
                            last_analyzed_at: str = None):
        """更新频道统计信息"""
        config = self.load()
        for channel in config['channels']:
            if channel['name'] == name:
                if total_videos is not None:
                    channel['stats']['total_videos'] = total_videos
                if analyzed_count is not None:
                    channel['stats']['analyzed_count'] = analyzed_count
                if last_analyzed_at is not None:
                    channel['stats']['last_analyzed_at'] = last_analyzed_at
                self.save()
                return True
        return False
    
    def add_analyzed_video(self, channel_name: str, video_id: str):
        """添加已分析的视频ID"""
        config = self.load()
        for channel in config['channels']:
            if channel['name'] == channel_name:
                if 'analyzed_video_ids' not in channel:
                    channel['analyzed_video_ids'] = []
                if video_id not in channel['analyzed_video_ids']:
                    channel['analyzed_video_ids'].append(video_id)
                    channel['stats']['analyzed_count'] = len(channel['analyzed_video_ids'])
                    self.save()
                return True
        return False
    
    def is_video_analyzed(self, channel_name: str, video_id: str) -> bool:
        """检查视频是否已分析"""
        config = self.load()
        for channel in config['channels']:
            if channel['name'] == channel_name:
                return video_id in channel.get('analyzed_video_ids', [])
        return False
    
    def get_channel_notebook_dir(self, name: str) -> str:
        """获取频道的笔记目录"""
        return os.path.join(self.notebooks_dir, name)
    
    def set_channel_analysis_mode(self, name: str, mode: str) -> bool:
        """
        设置频道的分析模式
        
        Args:
            name: 频道名称
            mode: 分析模式 ('local' 或 'pass_through')
        
        Returns:
            是否成功
        """
        if mode not in ['local', 'pass_through']:
            raise ValueError("分析模式必须是 'local' 或 'pass_through'")
        
        config = self.load()
        for channel in config['channels']:
            if channel['name'] == name:
                channel['analysis_mode'] = mode
                self.save()
                return True
        return False


# 全局配置管理器实例
config_manager = ConfigManager()