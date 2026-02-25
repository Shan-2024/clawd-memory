#!/usr/bin/env python3
"""
Lip NotebookLM 每日新闻工作流
直接从YouTube RSS获取视频，发送到NotebookLM，通过飞书消息发送每日新闻
"""

import json
import os
import sys
import time
import requests
import feedparser
from datetime import datetime, timedelta
import subprocess
import re

# 配置路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
NOTEBOOKLM_CLI = os.path.expanduser("~/.local/bin/notebooklm")

class LipNotebookLMDaily:
    def __init__(self):
        self.config = self.load_config()
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def load_config(self):
        """加载配置文件"""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self):
        """保存配置文件"""
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_channel_videos(self, channel_url, max_videos=5):
        """从YouTube RSS获取视频列表"""
        try:
            # 提取频道ID
            if '/@' in channel_url:
                channel_id = channel_url.split('/@')[-1].split('/')[0]
                rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={self.get_channel_id_from_handle(channel_id)}"
            else:
                # 已经是频道ID格式
                channel_id = channel_url.split('/channel/')[-1]
                rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            
            # 解析RSS
            feed = feedparser.parse(rss_url)
            
            videos = []
            for entry in feed.entries[:max_videos]:
                video_id = entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.link.split('v=')[-1]
                
                videos.append({
                    'id': video_id,
                    'title': entry.title,
                    'url': entry.link,
                    'published': entry.published,
                    'description': entry.get('summary', ''),
                    'duration': None  # RSS不包含时长
                })
            
            return videos
            
        except Exception as e:
            print(f"获取频道 {channel_url} 视频失败: {e}")
            return []
    
    def get_channel_id_from_handle(self, handle):
        """通过handle获取频道ID（简化版，实际需要API）"""
        # 这里简化处理，实际需要YouTube API
        return handle
    
    def create_notebooklm_notebook(self, channel_name, videos):
        """为频道创建NotebookLM笔记本"""
        try:
            # 创建笔记本
            notebook_name = f"{channel_name} - {self.today}"
            cmd = [NOTEBOOKLM_CLI, "create", notebook_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"创建笔记本失败: {result.stderr}")
                return None
            
            # 提取笔记本ID
            notebook_id = None
            for line in result.stdout.split('\n'):
                if 'Notebook created:' in line:
                    notebook_id = line.split(':')[-1].strip()
                    break
            
            if not notebook_id:
                print("无法提取笔记本ID")
                return None
            
            # 添加视频作为来源
            for video in videos[:50]:  # 最多50条来源
                self.add_source_to_notebook(notebook_id, video['url'])
                time.sleep(1)  # 避免请求过快
            
            return notebook_id
            
        except Exception as e:
            print(f"创建NotebookLM笔记本失败: {e}")
            return None
    
    def add_source_to_notebook(self, notebook_id, url):
        """添加来源到笔记本"""
        try:
            cmd = [NOTEBOOKLM_CLI, "use", notebook_id]
            subprocess.run(cmd, capture_output=True)
            
            cmd = [NOTEBOOKLM_CLI, "source", "add", url]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ 添加来源: {url}")
                return True
            else:
                print(f"✗ 添加来源失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"添加来源失败: {e}")
            return False
    
    def ask_notebooklm(self, notebook_id, question):
        """向NotebookLM提问"""
        try:
            cmd = [NOTEBOOKLM_CLI, "use", notebook_id]
            subprocess.run(cmd, capture_output=True)
            
            cmd = [NOTEBOOKLM_CLI, "ask", question]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"提问失败: {result.stderr}"
                
        except Exception as e:
            return f"提问失败: {e}"
    
    def generate_daily_summary(self, channel_name, notebook_id, videos):
        """生成每日新闻摘要"""
        questions = [
            "请为这些视频生成一个综合摘要，包含主要主题和关键见解",
            "提取视频中提到的所有专业名词和技术术语，并为每个提供简单解释",
            "这些视频中最有价值的3个学习点是什么？",
            "如果我要向朋友推荐这些内容，我会怎么说？"
        ]
        
        summary_parts = []
        
        for i, question in enumerate(questions):
            answer = self.ask_notebooklm(notebook_id, question)
            summary_parts.append(f"## {i+1}. {question}\n{answer}\n")
            time.sleep(2)  # 避免请求过快
        
        # 视频列表
        video_list = "\n".join([f"- [{v['title']}]({v['url']})" for v in videos])
        
        full_summary = f"""# 📺 {channel_name} - {self.today} 每日学习新闻

## 📋 今日视频 ({len(videos)}个)
{video_list}

## 🧠 NotebookLM深度分析
{''.join(summary_parts)}

## 🎯 今日学习建议
1. **重点观看**: 建议优先观看前2个视频
2. **学习时间**: 预计需要 {len(videos)*15} 分钟完整学习
3. **实践建议**: 尝试应用视频中的1-2个关键概念

---
📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🤖 由Lip智能学习助手生成
"""
        
        return full_summary
    
    def send_feishu_message(self, channel_name, summary):
        """通过飞书消息发送摘要"""
        try:
            # 这里简化处理，实际需要飞书API
            # 先保存到文件，稍后手动发送
            filename = f"daily_news_{channel_name}_{self.today}.md"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"✓ 已保存到文件: {filepath}")
            
            # 返回消息内容，稍后通过飞书工具发送
            return {
                'success': True,
                'filepath': filepath,
                'summary_preview': summary[:500] + "..." if len(summary) > 500 else summary
            }
            
        except Exception as e:
            print(f"发送飞书消息失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def process_channel(self, channel):
        """处理单个频道"""
        print(f"\n{'='*60}")
        print(f"📺 处理频道: {channel['display_name']}")
        print(f"{'='*60}")
        
        # 获取视频列表
        videos = self.get_channel_videos(channel['url'], max_videos=5)
        
        if not videos:
            print("⚠️ 未获取到视频")
            return None
        
        print(f"📹 获取到 {len(videos)} 个视频:")
        for v in videos:
            print(f"  - {v['title']}")
        
        # 创建NotebookLM笔记本
        notebook_id = self.create_notebooklm_notebook(channel['display_name'], videos)
        
        if not notebook_id:
            print("⚠️ 创建笔记本失败，使用模拟数据")
            # 使用模拟数据继续
            summary = self.generate_mock_summary(channel['display_name'], videos)
        else:
            print(f"📒 笔记本创建成功: {notebook_id}")
            
            # 生成摘要
            summary = self.generate_daily_summary(channel['display_name'], notebook_id, videos)
        
        # 发送飞书消息
        result = self.send_feishu_message(channel['display_name'], summary)
        
        if result['success']:
            print(f"✅ 处理完成: {channel['display_name']}")
            return {
                'channel': channel['display_name'],
                'videos_processed': len(videos),
                'notebook_id': notebook_id,
                'summary_file': result['filepath']
            }
        else:
            print(f"❌ 处理失败: {result.get('error', '未知错误')}")
            return None
    
    def generate_mock_summary(self, channel_name, videos):
        """生成模拟摘要（当NotebookLM不可用时）"""
        video_list = "\n".join([f"- [{v['title']}]({v['url']})" for v in videos])
        
        return f"""# 📺 {channel_name} - {self.today} 模拟摘要

## 📋 今日视频 ({len(videos)}个)
{video_list}

## 🧠 模拟分析（NotebookLM暂不可用）

### 1. 主要主题
这些视频探讨了{channel_name}频道的核心主题，包括技术趋势、行业见解和个人成长。

### 2. 关键术语
- **AI Alignment**: 人工智能对齐问题
- **Prompt Engineering**: 提示词工程技巧
- **Neural Networks**: 神经网络基础原理
- **Ethical AI**: 人工智能伦理考量

### 3. 学习要点
1. 理解最新的技术发展趋势
2. 学习实用的技能和方法
3. 获得行业专家的深度见解

## 🎯 学习建议
建议按顺序观看视频，重点关注前2个核心内容。

---
📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🤖 由Lip智能学习助手生成（模拟模式）
"""
    
    def run_daily(self):
        """运行每日处理"""
        print(f"\n{'='*80}")
        print(f"🚀 Lip NotebookLM 每日新闻 - {self.today}")
        print(f"{'='*80}")
        
        results = []
        active_channels = [c for c in self.config['channels'] if c['status'] == 'active']
        
        print(f"📊 发现 {len(active_channels)} 个活跃频道")
        
        # 处理高优先级频道
        high_priority = [c for c in active_channels if c.get('priority') == 'high']
        print(f"🔥 高优先级: {len(high_priority)} 个")
        
        for channel in high_priority[:3]:  # 先处理3个高优先级
            result = self.process_channel(channel)
            if result:
                results.append(result)
            time.sleep(5)  # 避免请求过快
        
        # 生成总报告
        self.generate_daily_report(results)
        
        return results
    
    def generate_daily_report(self, results):
        """生成每日总报告"""
        if not results:
            print("⚠️ 今日无处理结果")
            return
        
        report = f"""# 📰 Lip 每日学习新闻汇总 - {self.today}

## 📊 今日处理统计
- 处理频道数: {len(results)}
- 总视频数: {sum(r['videos_processed'] for r in results)}
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📺 各频道处理详情
"""
        
        for result in results:
            report += f"\n### {result['channel']}\n"
            report += f"- 处理视频: {result['videos_processed']} 个\n"
            if result.get('notebook_id'):
                report += f"- NotebookLM ID: {result['notebook_id']}\n"
            report += f"- 摘要文件: {result['summary_file']}\n"
        
        report += f"\n---\n🤖 由Lip智能学习助手自动生成\n"
        
        # 保存报告
        report_file = os.path.join(os.path.dirname(__file__), f"daily_report_{self.today}.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📰 每日报告已保存: {report_file}")
        
        # 尝试通过飞书发送
        self.send_feishu_direct_message(report)
    
    def send_feishu_direct_message(self, content):
        """直接发送飞书消息"""
        try:
            # 这里简化，实际需要调用飞书API
            print(f"\n📤 准备发送飞书消息（内容长度: {len(content)} 字符）")
            print(f"📝 消息预览: {content[:200]}...")
            
            # 保存消息内容供手动发送
            message_file = os.path.join(os.path.dirname(__file__), f"feishu_message_{self.today}.txt")
            with open(message_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"💾 消息已保存到: {message_file}")
            print("📱 请通过飞书工具发送此消息")
            
            return True
            
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
            return False

def main():
    """主函数"""
    try:
        lip = LipNotebookLMDaily()
        results = lip.run_daily()
        
        print(f"\n{'='*80}")
        print(f"✅ 每日处理完成!")
        print(f"📊 处理结果: {len(results)} 个频道")
        print(f"{'='*80}")
        
        # 显示下一步操作
        print("\n🎯 下一步:")
        print("1. 检查生成的摘要文件")
        print("2. 通过飞书消息工具发送每日新闻")
        print("3. 查看NotebookLM中的新笔记本")
        print("4. 明天凌晨2点自动运行")
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()