"""
本地存储模块
管理笔记的本地文件存储
"""
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional


class LocalStorage:
    """本地笔记存储管理"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名，移除非法字符"""
        # 移除或替换非法字符
        filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename.strip()
    
    def _get_channel_dir(self, channel_name: str) -> str:
        """获取频道笔记目录"""
        channel_dir = os.path.join(self.base_dir, channel_name)
        os.makedirs(channel_dir, exist_ok=True)
        return channel_dir
    
    def save_note(self, channel_name: str, video_info: Dict, 
                  analysis: Dict, transcript: str) -> str:
        """
        保存笔记到本地
        
        Returns:
            保存的文件路径
        """
        channel_dir = self._get_channel_dir(channel_name)
        
        # 生成文件名
        date_str = datetime.now().strftime('%Y-%m-%d')
        safe_title = self._sanitize_filename(video_info['title'])
        filename = f"{date_str}-{safe_title}.md"
        filepath = os.path.join(channel_dir, filename)
        
        # 生成Markdown内容
        content = self._generate_markdown(video_info, analysis, transcript)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新频道的summary.json
        self._update_channel_summary(channel_name, video_info, analysis)
        
        return filepath
    
    def _generate_markdown(self, video_info: Dict, analysis: Dict, 
                           transcript: str) -> str:
        """生成Markdown格式的笔记"""
        # 格式化标签
        tags = analysis.get('tags', [])
        tag_str = ' '.join([f'#{tag}' for tag in tags]) if tags else '#未分类'
        
        # 格式化摘要
        summary_points = analysis.get('summary', [])
        summary_md = '\n'.join([f"{i+1}. {point}" for i, point in enumerate(summary_points)])
        
        # 格式化科普知识
        knowledge = analysis.get('knowledge', {})
        if knowledge:
            knowledge_md = '\n'.join([f"- **{name}**：{explanation}" 
                                       for name, explanation in knowledge.items()])
        else:
            knowledge_md = "_本视频未识别出需要解释的名词_"
        
        # 视频时长格式化
        duration = video_info.get('duration', 0)
        if duration:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = "未知"
        
        # 上传日期格式化
        upload_date = video_info.get('upload_date', '')
        if upload_date and len(upload_date) == 8:
            upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        
        markdown = f"""# {video_info['title']}

## 📊 元数据
- **博主**：{video_info.get('uploader', 'Unknown')}
- **视频ID**：[{video_info['id']}](https://www.youtube.com/watch?v={video_info['id']})
- **时长**：{duration_str}
- **发布日期**：{upload_date or 'Unknown'}
- **分析日期**：{datetime.now().strftime('%Y-%m-%d %H:%M')}
- **标签**：{tag_str}

## 📝 核心摘要
{summary_md}

## 📖 原文字幕
<details>
<summary>点击展开字幕（{len(transcript)} 字符）</summary>

{transcript}

</details>

## 🎓 科普板块
{knowledge_md}

---
*分析耗时：自动* | *模型：kimi-k2.5*
"""
        return markdown
    
    def _update_channel_summary(self, channel_name: str, video_info: Dict, 
                                analysis: Dict):
        """更新频道的汇总信息"""
        channel_dir = self._get_channel_dir(channel_name)
        summary_path = os.path.join(channel_dir, 'summary.json')
        
        # 读取现有汇总
        if os.path.exists(summary_path):
            with open(summary_path, 'r', encoding='utf-8') as f:
                summary = json.load(f)
        else:
            summary = {
                'channel_name': channel_name,
                'created_at': datetime.now().isoformat(),
                'notes': [],
                'all_tags': [],
                'all_knowledge': {}
            }
        
        # 添加新笔记记录
        note_record = {
            'video_id': video_info['id'],
            'title': video_info['title'],
            'analyzed_at': datetime.now().isoformat(),
            'tags': analysis.get('tags', []),
            'knowledge_keys': list(analysis.get('knowledge', {}).keys())
        }
        summary['notes'].append(note_record)
        
        # 更新标签集合
        for tag in analysis.get('tags', []):
            if tag not in summary['all_tags']:
                summary['all_tags'].append(tag)
        
        # 更新知识库
        for name, explanation in analysis.get('knowledge', {}).items():
            summary['all_knowledge'][name] = explanation
        
        summary['updated_at'] = datetime.now().isoformat()
        
        # 保存汇总
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    
    def get_notes(self, channel_name: str = None) -> List[Dict]:
        """
        获取笔记列表
        
        Args:
            channel_name: 如果指定，只获取该频道的笔记
            
        Returns:
            笔记信息列表
        """
        notes = []
        
        if channel_name:
            channels = [channel_name]
        else:
            # 获取所有频道
            channels = [d for d in os.listdir(self.base_dir) 
                       if os.path.isdir(os.path.join(self.base_dir, d))]
        
        for channel in channels:
            summary_path = os.path.join(self.base_dir, channel, 'summary.json')
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                for note in summary.get('notes', []):
                    note['channel'] = channel
                    notes.append(note)
        
        # 按分析时间倒序
        notes.sort(key=lambda x: x.get('analyzed_at', ''), reverse=True)
        return notes
    
    def get_knowledge_dict(self, channel_name: str = None) -> Dict[str, str]:
        """
        获取科普词典
        
        Returns:
            名词 -> 解释 的字典
        """
        knowledge = {}
        
        if channel_name:
            channels = [channel_name]
        else:
            channels = [d for d in os.listdir(self.base_dir) 
                       if os.path.isdir(os.path.join(self.base_dir, d))]
        
        for channel in channels:
            summary_path = os.path.join(self.base_dir, channel, 'summary.json')
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                knowledge.update(summary.get('all_knowledge', {}))
        
        return knowledge
    
    def get_note_content(self, channel_name: str, video_id: str) -> Optional[str]:
        """获取笔记的完整内容"""
        channel_dir = self._get_channel_dir(channel_name)
        
        # 查找包含该video_id的markdown文件
        for filename in os.listdir(channel_dir):
            if filename.endswith('.md') and video_id in filename:
                filepath = os.path.join(channel_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        
        return None