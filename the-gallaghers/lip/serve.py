#!/usr/bin/env python3
"""
简单的HTTP服务器，提供Lip系统状态页面
"""

import http.server
import socketserver
import json
import os
from datetime import datetime

PORT = 8080
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

class LipHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/channels':
            self.send_channels_api()
            return
        elif self.path == '/api/config':
            self.send_config_api()
            return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send_channels_api(self):
        """发送频道数据API"""
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            channels = []
            for channel in config['channels']:
                if channel['status'] == 'active':
                    channels.append({
                        'name': channel['display_name'],
                        'category': channel.get('category', '未分类'),
                        'priority': channel.get('priority', 'low'),
                        'url': channel['url'],
                        'analyzed': channel['stats']['analyzed_count'],
                        'feishu': f"https://feishu.cn/docx/{channel['feishu_doc_token']}" if channel.get('feishu_doc_token') else None
                    })
            
            response = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'channels': channels,
                    'total': len(channels),
                    'daily_limit': config['daily_limit_per_channel'],
                    'schedule': config['settings']['cron_schedule']
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def send_config_api(self):
        """发送配置数据API"""
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            response = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'data': {
                    'version': config['version'],
                    'settings': config['settings'],
                    'stats': {
                        'total_channels': len(config['channels']),
                        'active_channels': len([c for c in config['channels'] if c['status'] == 'active']),
                        'daily_limit_per_channel': config['daily_limit_per_channel'],
                        'max_videos_per_run': config['settings']['max_videos_per_run']
                    }
                }
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    with socketserver.TCPServer(("", PORT), LipHandler) as httpd:
        print(f"🚀 Lip系统状态页面已启动")
        print(f"📡 访问地址: http://localhost:{PORT}")
        print(f"📊 API端点: http://localhost:{PORT}/api/channels")
        print(f"⚙️  配置API: http://localhost:{PORT}/api/config")
        print(f"\n📺 监控频道: 11个")
        print(f"📝 每日处理: 5视频/频道")
        print(f"⏰ 定时任务: 每天2:00 AM")
        print(f"\n按 Ctrl+C 停止服务器")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")

if __name__ == "__main__":
    main()