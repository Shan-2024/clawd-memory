"""
飞书文档同步模块
将Lip学习笔记同步到飞书文档
"""
import os
import re
import json
from typing import List, Dict, Optional
from datetime import datetime


class FeishuDocSync:
    """飞书文档同步管理器"""
    
    def __init__(self, folder_token: str = None):
        self.folder_token = folder_token
        self.channel_docs = {}  # 缓存频道文档映射
    
    def create_feishu_doc(self, title: str) -> Optional[str]:
        """
        创建飞书文档
        
        Returns:
            文档URL
        """
        try:
            # 使用feishu_doc工具创建文档
            # 注意：这里假设我们在OpenClaw环境中运行，可以直接调用工具
            # 实际上应该通过OpenClaw的API调用
            
            # 方法1: 尝试直接调用工具
            try:
                # 导入工具函数
                from feishu_doc import feishu_doc
                
                # 创建文档
                result = feishu_doc(
                    action='create',
                    title=title,
                    folder_token=self.folder_token
                )
                
                if result and result.get('document_token'):
                    doc_token = result['document_token']
                    doc_url = f"https://feishu.cn/docx/{doc_token}"
                    print(f"  ✅ 文档创建成功: {doc_url}")
                    return doc_url
                    
            except ImportError:
                # 方法2: 使用subprocess调用openclaw agent
                import subprocess
                import json
                
                # 构造命令
                cmd = ['openclaw', 'agent', '--model', 'kimi/kimi-k2.5', '--task', f'创建飞书文档: {title}']
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # 尝试从输出中提取URL
                    output = result.stdout
                    import re
                    url_match = re.search(r'https?://[^\s]+', output)
                    if url_match:
                        print(f"  ✅ 文档创建成功: {url_match.group(0)}")
                        return url_match.group(0)
            
            print(f"  ❌ 无法创建文档")
            return None
                
        except Exception as e:
            print(f"  ❌ 创建飞书文档错误: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def write_to_feishu_doc(self, doc_url: str, content: str) -> bool:
        """
        写入内容到飞书文档
        
        Args:
            doc_url: 飞书文档URL
            content: Markdown内容
            
        Returns:
            是否成功
        """
        try:
            # 提取文档token
            doc_token = self.extract_doc_token(doc_url)
            if not doc_token:
                print(f"  ❌ 无法提取文档token")
                return False
            
            # 方法1: 尝试直接调用工具
            try:
                from feishu_doc import feishu_doc
                
                result = feishu_doc(
                    action='write',
                    doc_token=doc_token,
                    content=content
                )
                
                if result and result.get('success'):
                    print(f"  ✅ 写入成功")
                    return True
                    
            except ImportError:
                # 方法2: 使用临时文件
                import subprocess
                import tempfile
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                    f.write(content)
                    temp_path = f.name
                
                try:
                    # 通过openclaw agent写入
                    cmd = ['openclaw', 'agent', '--model', 'kimi/kimi-k2.5', '--task', f'写入飞书文档 {doc_token}']
                    
                    result = subprocess.run(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        input=f"请将以下内容写入飞书文档 {doc_token}:\n\n{content[:2000]}...",
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        return True
                    else:
                        print(f"  ❌ 写入失败: {result.stderr[:200]}")
                        return False
                finally:
                    os.unlink(temp_path)
            
            return False
                
        except Exception as e:
            print(f"  ❌ 写入飞书文档错误: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def append_to_feishu_doc(self, doc_url: str, content: str) -> bool:
        """
        追加内容到飞书文档
        
        Args:
            doc_url: 飞书文档URL
            content: Markdown内容
            
        Returns:
            是否成功
        """
        try:
            import subprocess
            import tempfile
            
            # 提取文档token
            doc_token = self.extract_doc_token(doc_url)
            if not doc_token:
                print(f"  ❌ 无法提取文档token")
                return False
            
            # 追加内容 - 使用临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                f.write(content)
                temp_path = f.name
            
            try:
                result = subprocess.run(
                    ['openclaw', 'feishu', 'doc', 'append', doc_token, temp_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    return True
                else:
                    print(f"  ❌ 追加失败: {result.stderr}")
                    return False
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            print(f"  ❌ 追加飞书文档错误: {e}")
            return False
    
    def extract_doc_token(self, url: str) -> Optional[str]:
        """从飞书文档URL提取token"""
        # 格式: https://xxx.feishu.cn/docx/TOKEN 或 /doc/TOKEN
        patterns = [
            r'/docx/([a-zA-Z0-9]+)',
            r'/doc/([a-zA-Z0-9]+)',
            r'/wiki/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_or_create_channel_doc(self, channel_name: str) -> Optional[str]:
        """
        获取或创建频道的飞书文档
        
        Returns:
            飞书文档URL
        """
        # 检查缓存
        if channel_name in self.channel_docs:
            return self.channel_docs[channel_name]
        
        # 检查配置中是否已有文档
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from config.manager import config_manager
        
        channel = config_manager.get_channel(channel_name)
        if channel and channel.get('feishu_doc_token'):
            # 已有文档，构造URL
            doc_url = f"https://feishu.cn/docx/{channel['feishu_doc_token']}"
            self.channel_docs[channel_name] = doc_url
            print(f"  📄 使用已有飞书文档: {doc_url}")
            return doc_url
        
        # 创建新文档
        doc_title = f"学习笔记 - {channel_name}"
        print(f"  📄 创建飞书文档: {doc_title}")
        
        doc_url = self.create_feishu_doc(doc_title)
        
        if doc_url and channel:
            # 保存到配置
            doc_token = self.extract_doc_token(doc_url)
            if doc_token:
                channel['feishu_doc_token'] = doc_token
                config_manager.save()
            
            self.channel_docs[channel_name] = doc_url
        
        return doc_url
    
    def sync_note(self, channel_name: str, video_info: Dict, analysis: Dict, transcript: str) -> bool:
        """
        同步单个笔记到飞书文档
        
        Args:
            channel_name: 频道名称
            video_info: 视频信息
            analysis: AI分析结果
            transcript: 字幕内容
            
        Returns:
            是否成功
        """
        # 获取或创建文档
        doc_url = self.get_or_create_channel_doc(channel_name)
        if not doc_url:
            return False
        
        # 生成Markdown内容
        content = self._generate_note_content(video_info, analysis, transcript)
        
        print(f"  ⏳ 追加到飞书文档...")
        if self.append_to_feishu_doc(doc_url, content):
            print(f"  ✅ 已同步到飞书文档")
            return True
        else:
            print(f"  ❌ 同步失败")
            return False
    
    def _generate_note_content(self, video_info: Dict, analysis: Dict, transcript: str) -> str:
        """生成笔记内容（Markdown格式）"""
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
        
        content = f"""# {video_info['title']}

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
        return content
    
    def sync_local_notes(self, channel_name: str, notebooks_dir: str = None) -> Dict:
        """
        同步本地笔记到飞书文档
        
        Args:
            channel_name: 频道名称
            notebooks_dir: 笔记根目录
            
        Returns:
            同步结果
        """
        if notebooks_dir is None:
            notebooks_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
        
        channel_dir = os.path.join(notebooks_dir, channel_name)
        
        if not os.path.exists(channel_dir):
            return {'success': False, 'error': f'Channel {channel_name} not found'}
        
        print(f"\n📚 同步 {channel_name} 到飞书文档")
        
        # 获取所有Markdown文件
        md_files = [f for f in os.listdir(channel_dir) if f.endswith('.md') and f != 'summary.json']
        
        if not md_files:
            return {'success': True, 'added': 0, 'skipped': 0, 'message': 'No notes to sync'}
        
        # 获取或创建文档
        doc_url = self.get_or_create_channel_doc(channel_name)
        if not doc_url:
            return {'success': False, 'error': 'Failed to create document'}
        
        # 合并所有笔记内容
        all_content = []
        for filename in sorted(md_files, reverse=True):  # 最新的在前面
            filepath = os.path.join(channel_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                all_content.append(content)
                all_content.append("\n\n---\n\n")  # 分隔线
        
        # 写入文档
        full_content = '\n'.join(all_content)
        
        print(f"  共 {len(md_files)} 条笔记，总长度 {len(full_content)} 字符")
        
        # 由于飞书文档有长度限制，可能需要分批写入
        # 简化处理：先写入前10000字符
        if len(full_content) > 10000:
            full_content = full_content[:10000] + "\n\n...（内容已截断，请查看本地完整笔记）"
        
        # 首次写入覆盖，后续追加
        if self.write_to_feishu_doc(doc_url, full_content):
            return {
                'success': True,
                'doc_url': doc_url,
                'notes_count': len(md_files),
                'message': f'Synced {len(md_files)} notes to Feishu Doc'
            }
        else:
            return {'success': False, 'error': 'Failed to write to document'}


# 便捷函数
def sync_to_feishu(channel_name: str = None) -> Dict:
    """同步到飞书的便捷函数"""
    sync = FeishuDocSync()
    
    if channel_name:
        return sync.sync_local_notes(channel_name)
    else:
        # 同步所有频道
        notebooks_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks')
        results = []
        
        for name in os.listdir(notebooks_dir):
            channel_dir = os.path.join(notebooks_dir, name)
            if os.path.isdir(channel_dir):
                result = sync.sync_local_notes(name)
                results.append(result)
        
        return {
            'success': True,
            'channels': len(results),
            'results': results
        }