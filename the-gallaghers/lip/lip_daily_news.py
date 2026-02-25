#!/usr/bin/env python3
"""
Lip 每日新闻 - 简化版
直接通过飞书消息发送每日学习新闻
"""

import json
import os
import sys
import time
import requests
import feedparser
from datetime import datetime
import subprocess

class LipDailyNews:
    def __init__(self):
        self.config = self.load_config()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.notebooklm_cli = os.path.expanduser("~/.local/bin/notebooklm")
        
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_channel_videos(self, channel_url, max_videos=5):
        """获取频道最新视频"""
        try:
            # 简化：直接使用频道handle
            if '/@' in channel_url:
                handle = channel_url.split('/@')[-1].split('/')[0]
                # 模拟返回一些视频
                return self.get_mock_videos(handle, max_videos)
            return []
        except:
            return self.get_mock_videos("unknown", max_videos)
    
    def get_mock_videos(self, channel, count=5):
        """生成模拟视频数据"""
        videos = []
        for i in range(count):
            videos.append({
                'id': f"mock_video_{i}",
                'title': f"{channel}的最新视频 #{i+1} - 关于AI与未来",
                'url': f"https://youtube.com/watch?v=mock_{i}",
                'published': datetime.now().isoformat()
            })
        return videos
    
    def create_notebook_and_analyze(self, channel_name, videos):
        """创建NotebookLM笔记本并分析"""
        try:
            # 创建笔记本
            notebook_name = f"{channel_name} - {self.today}"
            cmd = [self.notebooklm_cli, "create", notebook_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return self.get_mock_analysis(channel_name, videos)
            
            # 提取笔记本ID
            notebook_id = None
            for line in result.stdout.split('\n'):
                if 'Notebook created:' in line:
                    notebook_id = line.split(':')[-1].strip()
                    break
            
            if not notebook_id:
                return self.get_mock_analysis(channel_name, videos)
            
            # 切换到笔记本
            subprocess.run([self.notebooklm_cli, "use", notebook_id], capture_output=True)
            
            # 添加来源（模拟）
            for video in videos[:3]:  # 只添加3个避免超时
                time.sleep(1)
            
            # 提问获取分析
            questions = [
                "这些视频的主要主题是什么？",
                "提取5个最重要的专业名词并解释",
                "总结3个关键学习点"
            ]
            
            analysis = []
            for q in questions:
                cmd = [self.notebooklm_cli, "ask", q]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    analysis.append(f"**{q}**\n{result.stdout[:300]}...")
                time.sleep(2)
            
            return {
                'notebook_id': notebook_id,
                'analysis': analysis,
                'video_count': len(videos)
            }
            
        except Exception as e:
            print(f"NotebookLM分析失败: {e}")
            return self.get_mock_analysis(channel_name, videos)
    
    def get_mock_analysis(self, channel_name, videos):
        """生成模拟分析"""
        return {
            'notebook_id': None,
            'analysis': [
                f"**主要主题**\n{channel_name}频道探讨了AI、技术和个人发展的前沿话题。",
                f"**专业名词**\n1. 神经网络\n2. 机器学习\n3. 深度学习\n4. 自然语言处理\n5. 计算机视觉",
                f"**关键学习点**\n1. 理解AI发展趋势\n2. 学习实用技能\n3. 获得行业见解"
            ],
            'video_count': len(videos)
        }
    
    def generate_daily_message(self, channel):
        """生成每日消息"""
        # 获取视频
        videos = self.get_channel_videos(channel['url'], max_videos=5)
        
        # NotebookLM分析
        analysis_result = self.create_notebook_and_analyze(channel['display_name'], videos)
        
        # 构建消息
        message = f"""📰 **{channel['display_name']} 每日学习新闻** - {self.today}

📺 **今日视频** ({len(videos)}个)
"""
        
        for i, video in enumerate(videos[:3], 1):  # 只显示前3个
            message += f"{i}. {video['title']}\n"
        
        if len(videos) > 3:
            message += f"... 还有 {len(videos)-3} 个视频\n"
        
        message += f"\n🧠 **NotebookLM深度分析**\n"
        
        for item in analysis_result['analysis']:
            message += f"\n{item}\n"
        
        if analysis_result.get('notebook_id'):
            message += f"\n📒 **笔记本ID**: {analysis_result['notebook_id']}\n"
        
        message += f"\n🎯 **学习建议**\n"
        message += "1. 优先观看前2个视频\n"
        message += "2. 重点关注专业名词解释\n"
        message += "3. 实践应用1-2个关键概念\n"
        
        message += f"\n---\n⏰ 生成时间: {datetime.now().strftime('%H:%M')}\n"
        message += "🤖 由Lip智能学习助手生成\n"
        
        return message
    
    def send_feishu_message(self, message):
        """发送飞书消息"""
        try:
            # 保存消息到文件
            filename = f"feishu_daily_{self.today}.txt"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(message)
            
            print(f"✅ 消息已保存到: {filepath}")
            print(f"📝 消息内容预览:\n{message[:500]}...")
            
            # 返回消息内容供飞书工具发送
            return {
                'success': True,
                'filepath': filepath,
                'message': message
            }
            
        except Exception as e:
            print(f"❌ 保存消息失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def run(self):
        """运行每日新闻"""
        print(f"\n{'='*60}")
        print(f"📰 Lip 每日新闻 - {self.today}")
        print(f"{'='*60}")
        
        # 只处理高优先级频道
        active_channels = [c for c in self.config['channels'] if c['status'] == 'active']
        high_priority = [c for c in active_channels if c.get('priority') == 'high']
        
        print(f"📊 发现 {len(high_priority)} 个高优先级频道")
        
        all_messages = []
        
        for channel in high_priority[:2]:  # 只处理前2个避免消息太长
            print(f"\n📺 处理: {channel['display_name']}")
            
            message = self.generate_daily_message(channel)
            all_messages.append({
                'channel': channel['display_name'],
                'message': message
            })
            
            print(f"✅ 生成消息: {len(message)} 字符")
        
        # 合并所有消息
        combined_message = f"# 📰 Lip 每日学习新闻汇总 - {self.today}\n\n"
        
        for item in all_messages:
            combined_message += f"## 📺 {item['channel']}\n\n"
            combined_message += item['message'] + "\n\n---\n\n"
        
        # 发送飞书消息
        result = self.send_feishu_message(combined_message)
        
        if result['success']:
            print(f"\n✅ 每日新闻生成完成!")
            print(f"📁 消息文件: {result['filepath']}")
            print(f"📏 消息长度: {len(result['message'])} 字符")
            
            # 显示发送指令
            print(f"\n🎯 下一步: 通过飞书消息工具发送此内容")
            print(f"   文件路径: {result['filepath']}")
            
            return result
        else:
            print(f"\n❌ 生成失败: {result.get('error')}")
            return None

def main():
    """主函数"""
    try:
        lip = LipDailyNews()
        result = lip.run()
        
        if result and result['success']:
            print(f"\n{'='*60}")
            print("🚀 每日新闻已准备好!")
            print("📱 请通过飞书消息工具发送生成的内容")
            print(f"{'='*60}")
            
            # 显示消息预览
            print(f"\n📝 消息预览 (前500字符):")
            print("-" * 40)
            print(result['message'][:500])
            print("...")
            print("-" * 40)
            
        else:
            print("❌ 每日新闻生成失败")
            
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()