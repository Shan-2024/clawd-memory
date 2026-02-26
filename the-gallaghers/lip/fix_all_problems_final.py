#!/usr/bin/env python3
"""
最终修复脚本 - 使用完全兼容的subprocess调用
"""

import json
import os
import sys
import time
import feedparser
from datetime import datetime
import subprocess
import re

# 配置路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
NOTEBOOKLM_CLI = os.path.expanduser("~/.local/bin/notebooklm")

class LipFixer:
    def __init__(self):
        self.config = self.load_config()
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def load_config(self):
        """加载配置文件"""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_command(self, cmd):
        """运行命令（完全兼容）"""
        try:
            result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = result.communicate()
            return result.returncode, stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore')
        except Exception as e:
            return 1, "", str(e)
    
    def get_channel_id_from_url(self, url):
        """从YouTube URL提取频道ID"""
        if '/@' in url:
            handle = url.split('/@')[-1].split('/')[0]
            return self.convert_handle_to_channel_id(handle)
        elif '/channel/' in url:
            return url.split('/channel/')[-1].split('/')[0]
        elif '/c/' in url:
            custom = url.split('/c/')[-1].split('/')[0]
            return custom
        else:
            return None
    
    def convert_handle_to_channel_id(self, handle):
        """将@handle转换为频道ID"""
        handle_to_id = {
            'lexfridman': 'UCSHZKyawb77ixDdsGog4iWA',
            'JordanBPeterson': 'UCL_f53ZEJxp8TtlOkHwMV9Q',
            'joerogan': 'UCzQUP1qoWDoEbmsQxvdjxgQ',
            'wearenocode': 'UCvqRdlKsE5Q8mf8YXbdIJLw',
            'Itssssss_Jack': 'UCjc1vfduI7BhVMXBLJLDjmA'
        }
        return handle_to_id.get(handle, handle)
    
    def get_channel_videos(self, channel_url, max_videos=3):
        """从YouTube RSS获取视频列表"""
        try:
            channel_id = self.get_channel_id_from_url(channel_url)
            if not channel_id:
                print(f"无法提取频道ID: {channel_url}")
                return []
            
            rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            print(f"   RSS: {rss_url}")
            
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print(f"   没有视频")
                return []
            
            videos = []
            for entry in feed.entries[:max_videos]:
                video_id = entry.get('yt_videoid', '')
                if not video_id and 'link' in entry:
                    match = re.search(r'v=([a-zA-Z0-9_-]+)', entry.link)
                    video_id = match.group(1) if match else ''
                
                videos.append({
                    'id': video_id,
                    'title': entry.title,
                    'url': entry.link,
                    'published': entry.published,
                    'description': entry.get('summary', '')[:100]
                })
            
            print(f"   获取到 {len(videos)} 个视频")
            return videos
            
        except Exception as e:
            print(f"   获取失败: {e}")
            return []
    
    def test_notebooklm(self):
        """测试NotebookLM CLI是否可用"""
        print("测试NotebookLM CLI...")
        returncode, stdout, stderr = self.run_command([NOTEBOOKLM_CLI, "list"])
        
        if returncode == 0:
            print("✓ NotebookLM CLI可用")
            return True
        else:
            print(f"✗ NotebookLM CLI不可用: {stderr}")
            return False
    
    def manual_fix_summary(self):
        """生成手动修复摘要"""
        print("\n" + "=" * 60)
        print("手动修复方案")
        print("=" * 60)
        
        summary = []
        
        # 分析每个频道
        active_channels = [c for c in self.config['channels'] if c.get('status') == 'active']
        
        for channel in active_channels[:8]:  # 只显示前8个
            channel_url = channel['url']
            channel_name = channel.get('display_name', channel['name'])
            
            videos = self.get_channel_videos(channel_url, max_videos=2)
            
            if videos:
                summary.append({
                    'name': channel_name,
                    'url': channel_url,
                    'video_count': len(videos),
                    'latest_video': videos[0]['title'][:50] + "..." if len(videos[0]['title']) > 50 else videos[0]['title']
                })
        
        # 输出摘要
        print(f"\n📊 发现 {len(summary)} 个有视频的频道:")
        for item in summary:
            print(f"  • {item['name']}: {item['video_count']}个视频")
            print(f"    最新: {item['latest_video']}")
        
        return summary
    
    def generate_fix_instructions(self):
        """生成修复指令"""
        print("\n" + "=" * 60)
        print("立即修复步骤")
        print("=" * 60)
        
        instructions = """
## 🔧 立即修复凌晨2点任务失败的问题

### 问题根源
1. **Python版本兼容性问题** - subprocess调用失败
2. **YouTube RSS限制** - 部分频道无法通过RSS访问
3. **NotebookLM集成不完整** - 只处理了部分频道

### 手动修复方案

#### 1. 直接运行NotebookLM命令
```bash
# 为Lex Fridman添加视频
~/.local/bin/notebooklm create "学习笔记 - Lex Fridman 修复"
~/.local/bin/notebooklm use <笔记本ID>
~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=最新视频ID"

# 为Jordan Peterson添加视频  
~/.local/bin/notebooklm create "学习笔记 - Jordan Peterson 修复"
~/.local/bin/notebooklm use <笔记本ID>
~/.local/bin/notebooklm source add "https://www.youtube.com/watch?v=最新视频ID"
```

#### 2. 修复cron任务
```bash
# 检查cron任务
crontab -l

# 修改cron脚本，添加错误日志
0 2 * * * /bin/bash /home/admin/.openclaw/workspace/the-gallaghers/lip/lip_cron_daily.sh >> /tmp/lip_cron.log 2>&1
```

#### 3. 创建飞书文档
1. 手动创建飞书文档，标题："Lip每日学习新闻 2026-02-26"
2. 包含所有频道的视频摘要
3. 通过飞书消息发送链接

### 长期解决方案
1. 升级Python到3.7+版本
2. 使用YouTube Data API替代RSS
3. 添加错误监控和通知
4. 定期验证cron任务执行结果
"""
        
        print(instructions)
        
        # 保存指令到文件
        instructions_path = os.path.join(os.path.dirname(__file__), f"fix_instructions_{self.today}.md")
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"\n📝 修复指令已保存: {instructions_path}")
        
        return instructions
    
    def create_feishu_content(self):
        """创建飞书文档内容"""
        content = f"""# 📚 Lip每日学习新闻 - {self.today}

## 🕒 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ⚠️ 系统状态
**凌晨2点定时任务执行不完整**，需要手动修复。

## 🔧 问题详情
1. **NotebookLM同步不完整** - 只添加了Lex Fridman的2个视频
2. **其他YouTuber未处理** - Joe Rogan、Dwarkesh Patel等频道未同步
3. **飞书内容未生成** - 缺少每日学习新闻文档

## 📊 受影响频道
根据配置，以下频道应该每日同步：

### 深度访谈类
- Lex Fridman (@lexfridman) - 2个视频已添加
- Jordan B Peterson (@JordanBPeterson) - 17个视频（昨天添加）
- Joe Rogan Experience (@joerogan) - 未同步
- The Diary Of A CEO (@TheDiaryOfACEO) - 未同步

### AI/技术类  
- No Code (@wearenocode) - 未同步
- Dwarkesh Patel (@DwarkeshPatel) - 未同步
- Matthew Berman (@matthew_berman) - 未同步
- Futurepedia (@futurepedia_io) - 未同步
- AI Foundations (@ai-foundations) - 未同步

### 其他
- Jack (@Itssssss_Jack) - 未同步

## 🚀 立即行动
1. **检查NotebookLM** - 验证现有内容
2. **手动添加缺失视频** - 使用修复脚本
3. **监控明天凌晨任务** - 确保cron正常工作
4. **设置错误通知** - 任务失败时收到提醒

## 📞 技术支持
如需帮助，请联系系统管理员或查看修复文档。

---
*Lip学习助手系统 | 自动生成*"""
        
        return content
    
    def run(self):
        """运行主修复流程"""
        print("=" * 60)
        print(f"Lip系统全面诊断 - {self.today}")
        print("=" * 60)
        
        # 1. 测试NotebookLM
        notebooklm_ok = self.test_notebooklm()
        
        # 2. 分析频道状态
        summary = self.manual_fix_summary()
        
        # 3. 生成修复指令
        instructions = self.generate_fix_instructions()
        
        # 4. 创建飞书内容
        feishu_content = self.create_feishu_content()
        
        # 保存飞书内容
        feishu_path = os.path.join(os.path.dirname(__file__), f"feishu_content_{self.today}.md")
        with open(feishu_path, 'w', encoding='utf-8') as f:
            f.write(feishu_content)
        
        print(f"\n📄 飞书内容已保存: {feishu_path}")
        print(f"\n📋 内容预览:")
        print("-" * 40)
        print(feishu_content[:500] + "...")
        print("-" * 40)
        
        print("\n" + "=" * 60)
        print("诊断完成!")
        print("=" * 60)
        
        return {
            'notebooklm_ok': notebooklm_ok,
            'channels_analyzed': len(summary),
            'feishu_content_path': feishu_path,
            'instructions_path': os.path.join(os.path.dirname(__file__), f"fix_instructions_{self.today}.md")
        }

def main():
    fixer = LipFixer()
    result = fixer.run()
    
    print(f"\n🎯 下一步:")
    print(f"1. 查看飞书内容: {result['feishu_content_path']}")
    print(f"2. 按照修复指令操作: {result['instructions_path']}")
    print(f"3. 手动发送飞书消息给Vec")
    print(f"4. 验证明天凌晨2点的cron任务")

if __name__ == "__main__":
    main()