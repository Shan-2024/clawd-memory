#!/usr/bin/env python3
"""
Lip Web API 服务器
为前端提供数据接口
"""
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from youtube.parser import YouTubeURLParser
from youtube.extractor import YouTubeExtractor
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage

# CORS允许的来源（开发用）
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "file://",  # 本地文件
]


class LipAPIHandler(BaseHTTPRequestHandler):
    """API请求处理器"""
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[API] {self.address_string()} - {format % args}")
    
    def _set_headers(self, status=200):
        """设置响应头"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        
        # CORS头
        origin = self.headers.get('Origin', '')
        if any(origin.startswith(allowed) for allowed in ALLOWED_ORIGINS):
            self.send_header('Access-Control-Allow-Origin', origin)
        else:
            self.send_header('Access-Control-Allow-Origin', '*')
        
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self._set_headers()
    
    def do_GET(self):
        """处理GET请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # 解析路径
        parts = path.strip('/').split('/')
        
        if path == '/api/status':
            self._handle_get_status()
        elif path == '/api/channels':
            self._handle_get_channels()
        elif path == '/api/notes':
            self._handle_get_notes(params)
        elif path == '/api/knowledge':
            self._handle_get_knowledge(params)
        elif path == '/api/notebooklm/notebooks':
            self._handle_get_notebooklm_list()
        elif path == '/api/test':
            self._handle_test()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_POST(self):
        """处理POST请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode())
            return
        
        if path == '/api/channels':
            self._handle_add_channel(data)
        elif path == '/api/channels/delete':
            self._handle_delete_channel(data)
        elif path == '/api/analyze':
            self._handle_analyze_now(data)
        elif path == '/api/analyze/pass-through':
            self._handle_analyze_pass_through(data)
        elif path == '/api/sync/notebooklm':
            self._handle_sync_notebooklm(data)
        elif path == '/api/sync/feishu':
            self._handle_sync_feishu(data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def do_GET(self):
        """处理GET请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # 解析路径
        parts = path.strip('/').split('/')
        
        if path == '/api/status':
            self._handle_get_status()
        elif path == '/api/channels':
            self._handle_get_channels()
        elif path == '/api/notes':
            self._handle_get_notes(params)
        elif path == '/api/knowledge':
            self._handle_get_knowledge(params)
        elif path == '/api/notebooklm/notebooks':
            self._handle_get_notebooklm_list()
        elif path == '/api/test':
            self._handle_test()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _handle_get_status(self):
        """获取系统状态"""
        try:
            channels = config_manager.get_all_channels()
            storage = LocalStorage()
            
            # 统计
            total_channels = len(channels)
            active_channels = sum(1 for c in channels if c['status'] == 'active')
            total_videos = sum(c['stats']['total_videos'] for c in channels)
            analyzed_videos = sum(c['stats']['analyzed_count'] for c in channels)
            
            # 获取所有笔记
            notes = storage.get_notes()
            
            # 获取知识词条数
            knowledge = storage.get_knowledge_dict()
            
            result = {
                'success': True,
                'data': {
                    'total_channels': total_channels,
                    'active_channels': active_channels,
                    'total_videos': total_videos,
                    'analyzed_videos': analyzed_videos,
                    'total_notes': len(notes),
                    'knowledge_count': len(knowledge),
                    'progress_percent': (analyzed_videos / total_videos * 100) if total_videos > 0 else 0,
                    'version': config_manager.load().get('version', '1.0')
                }
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_get_channels(self):
        """获取频道列表"""
        try:
            channels = config_manager.get_all_channels()
            
            # 添加进度信息
            for ch in channels:
                total = ch['stats']['total_videos']
                analyzed = ch['stats']['analyzed_count']
                ch['progress'] = {
                    'total': total,
                    'analyzed': analyzed,
                    'percent': (analyzed / total * 100) if total > 0 else 0,
                    'remaining_days': ((total - analyzed + 4) // 5) if total > analyzed else 0
                }
            
            self._set_headers()
            self.wfile.write(json.dumps({'success': True, 'data': channels}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_get_notes(self, params):
        """获取笔记列表"""
        try:
            storage = LocalStorage()
            channel = params.get('channel', [None])[0]
            search = params.get('search', [None])[0]
            
            notes = storage.get_notes(channel)
            
            # 搜索过滤
            if search:
                search_lower = search.lower()
                notes = [n for n in notes if search_lower in n.get('title', '').lower()]
            
            # 限制数量
            limit = int(params.get('limit', [50])[0])
            notes = notes[:limit]
            
            self._set_headers()
            self.wfile.write(json.dumps({'success': True, 'data': notes, 'total': len(notes)}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_get_knowledge(self, params):
        """获取知识词典"""
        try:
            storage = LocalStorage()
            channel = params.get('channel', [None])[0]
            
            knowledge = storage.get_knowledge_dict(channel)
            
            # 转换为列表格式
            items = [{'name': k, 'explanation': v} for k, v in knowledge.items()]
            
            # 支持搜索
            search = params.get('search', [None])[0]
            if search:
                search_lower = search.lower()
                items = [i for i in items if search_lower in i['name'].lower()]
            
            self._set_headers()
            self.wfile.write(json.dumps({'success': True, 'data': items, 'total': len(items)}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_add_channel(self, data):
        """添加频道"""
        try:
            url = data.get('url', '').strip()
            
            if not url:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'URL is required'}).encode())
                return
            
            # 解析URL
            parser = YouTubeURLParser()
            parsed = parser.parse(url)
            
            if parsed['type'] != 'channel':
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Invalid channel URL'}).encode())
                return
            
            # 检查是否已存在
            channel_name = parsed['id']
            existing = config_manager.get_channel(channel_name)
            if existing:
                self._set_headers(200)
                self.wfile.write(json.dumps({'success': True, 'message': 'Channel already exists', 'data': existing}, ensure_ascii=False).encode())
                return
            
            # 获取频道信息
            extractor = YouTubeExtractor(proxy=None)
            videos = extractor.get_channel_videos(url, limit=1)
            
            if not videos:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Failed to fetch channel info'}).encode())
                return
            
            # 添加到配置
            channel = config_manager.add_channel(
                url=url,
                name=channel_name,
                display_name=videos[0].get('uploader', channel_name)
            )
            
            # 更新总视频数
            all_videos = extractor.get_channel_videos(url, limit=1000)
            config_manager.update_channel_stats(channel_name, total_videos=len(all_videos))
            
            self._set_headers(201)
            self.wfile.write(json.dumps({'success': True, 'message': 'Channel added', 'data': channel}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_delete_channel(self, data):
        """删除频道"""
        try:
            name = data.get('name', '').strip()
            
            if not name:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Channel name is required'}).encode())
                return
            
            if config_manager.remove_channel(name):
                self._set_headers(200)
                self.wfile.write(json.dumps({'success': True, 'message': f'Channel {name} removed'}, ensure_ascii=False).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Channel not found'}).encode())
                
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_analyze_now(self, data):
        """立即分析"""
        try:
            channel_name = data.get('channel', '').strip()
            
            # 后台运行分析任务
            import subprocess
            
            if channel_name:
                # 分析特定频道
                cmd = f"cd /home/admin/.openclaw/workspace/the-gallaghers/lip && python3 -c \"from cron_job import DailyAnalyzer; a = DailyAnalyzer(); a._analyze_channel({config_manager.get_channel(channel_name)})\""
            else:
                # 分析所有频道
                cmd = "cd /home/admin/.openclaw/workspace/the-gallaghers/lip && python3 cron_job.py"
            
            # 后台运行
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            self._set_headers(200)
            self.wfile.write(json.dumps({'success': True, 'message': 'Analysis started in background'}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_analyze_pass_through(self, data):
        """直通模式分析 - 让NotebookLM直接抓取YouTube"""
        try:
            from youtube.notebooklm_pipeline import process_youtube_channel
            
            channel_name = data.get('channel', '').strip()
            
            if not channel_name:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Channel name is required'}, ensure_ascii=False).encode())
                return
            
            # 直通模式处理
            result = process_youtube_channel(channel_name)
            
            self._set_headers(200)
            self.wfile.write(json.dumps({'success': True, 'data': result}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_sync_notebooklm(self, data):
        """同步到NotebookLM"""
        try:
            from storage.notebooklm_sync import NotebookLMSync
            
            channel_name = data.get('channel', '').strip()
            
            sync = NotebookLMSync()
            
            if channel_name:
                # 同步特定频道
                notebooks_dir = os.path.join(os.path.dirname(__file__), 'notebooks')
                channel_dir = os.path.join(notebooks_dir, channel_name)
                
                if not os.path.exists(channel_dir):
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': 'Channel not found'}, ensure_ascii=False).encode())
                    return
                
                result = sync.sync_channel(channel_name, channel_dir)
            else:
                # 同步所有频道
                notebooks_dir = os.path.join(os.path.dirname(__file__), 'notebooks')
                results = sync.sync_all(notebooks_dir)
                result = {
                    'success': True,
                    'channels': len(results),
                    'total_added': sum(r.get('added', 0) for r in results),
                    'total_skipped': sum(r.get('skipped', 0) for r in results),
                    'details': results
                }
            
            self._set_headers(200)
            self.wfile.write(json.dumps({'success': True, 'data': result}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_sync_feishu(self, data):
        """同步到飞书文档"""
        try:
            from storage.feishu_sync import sync_to_feishu
            
            channel_name = data.get('channel', '').strip()
            
            result = sync_to_feishu(channel_name)
            
            self._set_headers(200)
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_get_notebooklm_list(self):
        """获取NotebookLM笔记本列表"""
        try:
            from storage.notebooklm_sync import NotebookLMSync
            
            sync = NotebookLMSync()
            notebooks = sync.list_notebooks()
            
            self._set_headers()
            self.wfile.write(json.dumps({'success': True, 'data': notebooks, 'total': len(notebooks)}, ensure_ascii=False).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_test(self):
        """测试接口"""
        self._set_headers()
        self.wfile.write(json.dumps({'success': True, 'message': 'API is working!'}, ensure_ascii=False).encode())


def run_server(port=8888):
    """启动API服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LipAPIHandler)
    print(f"🚀 Lip Web API 服务器已启动")
    print(f"   地址: http://localhost:{port}")
    print(f"   API文档:")
    print(f"     GET  /api/status              - 系统状态")
    print(f"     GET  /api/channels            - 频道列表")
    print(f"     POST /api/channels            - 添加频道")
    print(f"     POST /api/channels/delete     - 删除频道")
    print(f"     GET  /api/notes               - 笔记列表")
    print(f"     GET  /api/knowledge               - 知识词典")
    print(f"     POST /api/analyze                 - 立即分析（本地AI）")
    print(f"     POST /api/analyze/pass-through    - 直通模式（YouTube→NotebookLM）")
    print(f"     GET  /api/notebooklm/notebooks    - NotebookLM笔记本列表")
    print(f"     POST /api/sync/notebooklm         - 同步本地笔记到NotebookLM")
    print(f"     POST /api/sync/feishu             - 同步本地笔记到飞书文档")
    print(f"\n按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    run_server(port)