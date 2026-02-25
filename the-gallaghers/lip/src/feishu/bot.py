"""
飞书交互模块
处理飞书消息和命令
"""
import re
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.manager import config_manager
from youtube.parser import YouTubeURLParser
from youtube.extractor import YouTubeExtractor
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage


class LipFeishuBot:
    """Lip飞书机器人"""
    
    def __init__(self):
        self.config = config_manager
        self.parser = YouTubeURLParser()
        self.storage = LocalStorage()
    
    def handle_message(self, message: str) -> str:
        """
        处理飞书消息
        
        Returns:
            回复消息
        """
        message = message.strip()
        
        # 解析命令
        if '添加博主' in message or '添加频道' in message:
            return self._handle_add_channel(message)
        
        elif '状态' in message or '进度' in message:
            return self._handle_status()
        
        elif '删除博主' in message or '删除频道' in message:
            return self._handle_remove_channel(message)
        
        elif '同步' in message and 'NotebookLM' in message:
            return self._handle_sync_notebooklm(message)
        
        elif '科普词典' in message or '知识库' in message:
            return self._handle_knowledge_dict()
        
        elif '帮助' in message or 'help' in message.lower():
            return self._handle_help()
        
        # 检查是否是YouTube链接
        if self.parser.is_valid_youtube_url(message):
            parsed = self.parser.parse(message)
            if parsed['type'] == 'channel':
                return self._handle_add_channel(f"添加博主 {message}")
            else:
                return "请提供频道/博主链接，而不是单个视频链接。"
        
        return "抱歉，我没听懂。发送「帮助」查看可用命令。"
    
    def _handle_add_channel(self, message: str) -> str:
        """处理添加博主命令"""
        # 提取URL
        urls = re.findall(r'https?://[^\s]+', message)
        if not urls:
            return "请提供YouTube频道链接。例如：`添加博主 https://youtube.com/@channelname`"
        
        url = urls[0]
        
        # 解析URL
        parsed = self.parser.parse(url)
        if parsed['type'] != 'channel':
            return "请提供有效的YouTube频道链接（支持 @username、/c/name、/channel/UCxxx 格式）"
        
        # 获取频道信息
        try:
            extractor = YouTubeExtractor(proxy=None)
            videos = extractor.get_channel_videos(url, limit=1)
            
            if not videos:
                return "无法获取该频道信息，请检查链接是否正确。"
            
            # 确定频道名称
            channel_name = parsed['id']
            
            # 检查是否已存在
            existing = self.config.get_channel(channel_name)
            if existing:
                return f"博主 **{channel_name}** 已在监控列表中。"
            
            # 添加到配置
            channel = self.config.add_channel(
                url=url,
                name=channel_name,
                display_name=videos[0].get('uploader', channel_name)
            )
            
            # 更新总视频数
            all_videos = extractor.get_channel_videos(url, limit=1000)
            self.config.update_channel_stats(
                channel_name, 
                total_videos=len(all_videos)
            )
            
            return f"""✅ 已添加博主 **{channel_name}**

📊 频道信息：
- 当前共有 {len(all_videos)} 个视频
- 将从最新视频开始分析
- 每天自动分析 5 条

⏰ 预计完成时间：{len(all_videos) // 5} 天

发送「状态」查看所有博主进度。"""
            
        except Exception as e:
            return f"添加博主失败：{str(e)}"
    
    def _handle_status(self) -> str:
        """处理状态查询命令"""
        channels = self.config.get_all_channels()
        
        if not channels:
            return "当前没有监控任何博主。发送「添加博主 <YouTube链接>」开始添加。"
        
        lines = [f"📊 当前监控 **{len(channels)}** 个博主\n"]
        
        for ch in channels:
            stats = ch['stats']
            total = stats['total_videos']
            analyzed = stats['analyzed_count']
            
            if total > 0:
                progress = (analyzed / total) * 100
                bar_len = 10
                filled = int(bar_len * progress / 100)
                bar = '█' * filled + '░' * (bar_len - filled)
                
                lines.append(f"**{ch['name']}**")
                lines.append(f"进度：{bar} {progress:.1f}% ({analyzed}/{total})")
                lines.append(f"预计剩余：{(total - analyzed + 4) // 5} 天\n")
            else:
                lines.append(f"**{ch['name']}** - 等待首次分析\n")
        
        return '\n'.join(lines)
    
    def _handle_remove_channel(self, message: str) -> str:
        """处理删除博主命令"""
        # 提取博主名
        parts = message.split()
        if len(parts) < 3:
            return "请指定要删除的博主名称。例如：`删除博主 @channelname`"
        
        channel_name = parts[2]
        
        if self.config.remove_channel(channel_name):
            return f"✅ 已删除博主 **{channel_name}** 及其所有笔记。"
        else:
            return f"未找到博主 **{channel_name}**，请检查名称是否正确。"
    
    def _handle_sync_notebooklm(self, message: str) -> str:
        """处理同步到NotebookLM命令"""
        # 提取博主名
        parts = message.split()
        if len(parts) < 2:
            return "请指定要同步的博主。例如：`同步 @channelname 到NotebookLM`"
        
        channel_name = parts[1]
        
        channel = self.config.get_channel(channel_name)
        if not channel:
            return f"未找到博主 **{channel_name}**"
        
        # 检查notebooklm CLI是否可用
        import subprocess
        result = subprocess.run(['notebooklm', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            return "NotebookLM CLI 未配置，请检查环境。"
        
        # 获取该博主的所有笔记
        notes = self.storage.get_notes(channel_name)
        if not notes:
            return f"博主 **{channel_name}** 暂无已分析的笔记。"
        
        # 创建NotebookLM笔记本
        notebook_name = f"学习笔记 - {channel_name}"
        # TODO: 实现具体的同步逻辑
        
        return f"🔄 正在同步 **{channel_name}** 到 NotebookLM...\n（共 {len(notes)} 条笔记）"
    
    def _handle_knowledge_dict(self) -> str:
        """处理科普词典查询"""
        knowledge = self.storage.get_knowledge_dict()
        
        if not knowledge:
            return "暂无科普知识。请先添加博主并分析一些视频。"
        
        # 按名词排序
        items = sorted(knowledge.items())[:20]  # 只显示前20条
        
        lines = [f"📚 科普词典（共 {len(knowledge)} 条）\n"]
        for name, explanation in items:
            lines.append(f"**{name}**：{explanation[:50]}...")
        
        if len(knowledge) > 20:
            lines.append(f"\n...还有 {len(knowledge) - 20} 条，请查看本地文件")
        
        return '\n'.join(lines)
    
    def _handle_help(self) -> str:
        """处理帮助命令"""
        return """🤖 **Lip 智能学习助手** 使用指南

**添加博主**
`添加博主 <YouTube频道链接>`
支持格式：youtube.com/@username、/c/name、/channel/UCxxx

**查看进度**
`状态` 或 `进度`

**删除博主**
`删除博主 <博主名>`

**同步到NotebookLM**
`同步 <博主名> 到NotebookLM`

**查看科普词典**
`科普词典` 或 `知识库`

**帮助**
`帮助` 或 `help`

---
📌 每天自动分析5条最新视频，完成后会通知你。"""


# 便捷函数
def process_message(message: str) -> str:
    """处理飞书消息的便捷函数"""
    bot = LipFeishuBot()
    return bot.handle_message(message)