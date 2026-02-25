"""
NotebookLM同步模块
将Lip学习笔记同步到NotebookLM
"""
import os
import re
import subprocess
import json
from typing import List, Dict, Optional
from datetime import datetime


NOTEBOOKLM_BIN = os.path.expanduser('~/.local/bin/notebooklm')


class NotebookLMSync:
    """NotebookLM同步管理器"""
    
    def __init__(self):
        self.notebooklm_bin = NOTEBOOKLM_BIN
        self._check_availability()
    
    def _check_availability(self):
        """检查NotebookLM CLI是否可用"""
        if not os.path.exists(self.notebooklm_bin):
            raise Exception("NotebookLM CLI not found at ~/.local/bin/notebooklm")
    
    def _run_notebooklm(self, args: List[str]) -> tuple:
        """运行NotebookLM命令"""
        cmd = [self.notebooklm_bin] + args
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    
    def list_notebooks(self) -> List[Dict]:
        """获取所有NotebookLM笔记本列表"""
        try:
            returncode, stdout, stderr = self._run_notebooklm(['list', '--json'])
            if returncode == 0:
                data = json.loads(stdout)
                # notebooklm返回的是 {"notebooks": [...]} 格式
                return data.get('notebooks', [])
            return []
        except Exception as e:
            print(f"  获取笔记本列表失败: {e}")
            return []
    
    def create_notebook(self, title: str) -> Optional[str]:
        """
        创建新的NotebookLM笔记本
        
        Returns:
            笔记本ID
        """
        returncode, stdout, stderr = self._run_notebooklm(['create', title])
        
        if returncode != 0:
            raise Exception(f"创建笔记本失败: {stderr}")
        
        # 从输出中提取ID
        # 格式通常是：Created notebook: <id> 或直接在列表中
        notebooks = self.list_notebooks()
        for nb in notebooks:
            if nb.get('title') == title or title in nb.get('title', ''):
                return nb.get('id')
        
        return None
    
    def find_notebook_by_title(self, title: str) -> Optional[Dict]:
        """根据标题查找笔记本"""
        notebooks = self.list_notebooks()
        for nb in notebooks:
            if title.lower() in nb.get('title', '').lower():
                return nb
        return None
    
    def get_or_create_notebook(self, title: str) -> str:
        """获取或创建笔记本，返回笔记本ID"""
        # 先查找
        existing = self.find_notebook_by_title(title)
        if existing:
            print(f"  使用现有笔记本: {existing.get('title')} ({existing.get('id')})")
            return existing.get('id')
        
        # 创建新的
        print(f"  创建新笔记本: {title}")
        return self.create_notebook(title)
    
    def add_source(self, notebook_id: str, file_path: str, title: str = None) -> bool:
        """
        添加笔记文件到笔记本
        
        Args:
            notebook_id: NotebookLM笔记本ID
            file_path: Markdown文件路径
            title: 自定义标题（可选）
        """
        if not os.path.exists(file_path):
            print(f"  ⚠️  文件不存在: {file_path}")
            return False
        
        # 确保文件是Markdown格式
        if not file_path.endswith('.md'):
            print(f"  ⚠️  跳过非Markdown文件: {file_path}")
            return False
        
        args = ['source', 'add', file_path]
        if title:
            args.extend(['--title', title])
        
        returncode, stdout, stderr = self._run_notebooklm(args)
        
        if returncode != 0:
            print(f"  ❌ 添加失败: {stderr}")
            return False
        
        return True
    
    def list_sources(self, notebook_id: str) -> List[Dict]:
        """获取笔记本的所有source"""
        # 先切换到该笔记本
        self._run_notebooklm(['use', notebook_id])
        
        returncode, stdout, stderr = self._run_notebooklm(['source', 'list', '--json'])
        
        if returncode == 0:
            try:
                data = json.loads(stdout)
                # source list返回 {"sources": [...]} 格式
                return data.get('sources', [])
            except:
                pass
        return []
    
    def sync_channel(self, channel_name: str, channel_dir: str) -> Dict:
        """
        同步单个频道的所有笔记到NotebookLM
        
        Args:
            channel_name: 频道名称
            channel_dir: 频道笔记目录
            
        Returns:
            同步结果统计
        """
        print(f"\n📚 同步博主: {channel_name}")
        
        # 获取或创建笔记本
        notebook_title = f"学习笔记 - {channel_name}"
        try:
            notebook_id = self.get_or_create_notebook(notebook_title)
        except Exception as e:
            print(f"  ❌ 无法创建/获取笔记本: {e}")
            return {'success': False, 'added': 0, 'skipped': 0, 'error': str(e)}
        
        if not notebook_id:
            return {'success': False, 'added': 0, 'skipped': 0, 'error': 'No notebook ID'}
        
        # 获取已有sources
        existing_sources = self.list_sources(notebook_id)
        existing_titles = {s.get('title', '') for s in existing_sources}
        
        # 查找所有Markdown文件
        md_files = [f for f in os.listdir(channel_dir) if f.endswith('.md') and f != 'summary.json']
        
        added = 0
        skipped = 0
        
        for filename in md_files:
            # 从文件名提取标题（去掉日期前缀）
            title_match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md$', filename)
            if title_match:
                note_title = title_match.group(1)
            else:
                note_title = filename.replace('.md', '')
            
            # 检查是否已存在
            if note_title in existing_titles:
                print(f"  ⏭️  已存在: {note_title}")
                skipped += 1
                continue
            
            # 添加source
            file_path = os.path.join(channel_dir, filename)
            print(f"  📄 添加: {note_title}")
            
            if self.add_source(notebook_id, file_path, note_title):
                added += 1
            else:
                skipped += 1
        
        result = {
            'success': True,
            'notebook_id': notebook_id,
            'notebook_title': notebook_title,
            'added': added,
            'skipped': skipped,
            'total': len(md_files)
        }
        
        print(f"  ✅ 完成: 新增 {added} 条, 跳过 {skipped} 条")
        return result
    
    def sync_all(self, notebooks_dir: str) -> List[Dict]:
        """
        同步所有频道到NotebookLM
        
        Args:
            notebooks_dir: 笔记根目录
            
        Returns:
            各频道同步结果
        """
        print("\n" + "="*60)
        print("🔄 开始同步到 NotebookLM")
        print("="*60)
        
        results = []
        
        # 遍历所有频道目录
        for channel_name in os.listdir(notebooks_dir):
            channel_dir = os.path.join(notebooks_dir, channel_name)
            
            if not os.path.isdir(channel_dir):
                continue
            
            # 检查是否有Markdown文件
            md_files = [f for f in os.listdir(channel_dir) if f.endswith('.md')]
            if not md_files:
                print(f"\n⏭️  跳过 {channel_name}: 无笔记文件")
                continue
            
            result = self.sync_channel(channel_name, channel_dir)
            results.append(result)
        
        # 汇总
        total_added = sum(r.get('added', 0) for r in results)
        total_skipped = sum(r.get('skipped', 0) for r in results)
        
        print("\n" + "="*60)
        print(f"📊 同步完成: 新增 {total_added} 条, 跳过 {total_skipped} 条")
        print("="*60 + "\n")
        
        return results


# 便捷函数
def sync_to_notebooklm(channel_name: str = None, notebooks_dir: str = None) -> Dict:
    """
    同步到NotebookLM的便捷函数
    
    Args:
        channel_name: 如果指定，只同步该频道；否则同步所有
        notebooks_dir: 笔记根目录，默认使用项目目录
    """
    if notebooks_dir is None:
        notebooks_dir = os.path.join(os.path.dirname(__file__), '..', 'notebooks')
    
    sync = NotebookLMSync()
    
    if channel_name:
        channel_dir = os.path.join(notebooks_dir, channel_name)
        if os.path.exists(channel_dir):
            return sync.sync_channel(channel_name, channel_dir)
        else:
            return {'success': False, 'error': f'Channel {channel_name} not found'}
    else:
        return {'results': sync.sync_all(notebooks_dir)}