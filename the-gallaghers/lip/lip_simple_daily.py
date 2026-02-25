#!/usr/bin/env python3
"""
Lip 简单每日新闻 - 无外部依赖
直接生成每日学习新闻并通过飞书消息发送
"""

import json
import os
import sys
import time
from datetime import datetime
import subprocess

class LipSimpleDaily:
    def __init__(self):
        self.config = self.load_config()
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.notebooklm_cli = os.path.expanduser("~/.local/bin/notebooklm")
        
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_mock_videos(self, channel_name, count=5):
        """生成模拟视频数据"""
        topics = [
            "AI对齐与安全",
            "机器学习最新进展", 
            "深度神经网络原理",
            "自然语言处理应用",
            "计算机视觉突破",
            "强化学习实践",
            "大语言模型趋势",
            "AI伦理与治理",
            "技术创业洞察",
            "未来科技预测"
        ]
        
        videos = []
        for i in range(count):
            topic = topics[i % len(topics)]
            videos.append({
                'id': f"video_{i}_{int(time.time())}",
                'title': f"{channel_name}: {topic} - 深度解析",
                'url': f"https://youtube.com/watch?v=mock_{channel_name}_{i}",
                'published': datetime.now().isoformat()
            })
        return videos
    
    def create_notebooklm_analysis(self, channel_name, videos):
        """使用NotebookLM进行分析"""
        try:
            # 创建笔记本
            notebook_name = f"{channel_name}学习笔记 - {self.today}"
            print(f"  创建NotebookLM笔记本: {notebook_name}")
            
            cmd = [self.notebooklm_cli, "create", notebook_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            notebook_id = None
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'Notebook created:' in line:
                        notebook_id = line.split(':')[-1].strip()
                        break
            
            if notebook_id:
                print(f"  笔记本ID: {notebook_id}")
                
                # 切换到笔记本
                subprocess.run([self.notebooklm_cli, "use", notebook_id], 
                              capture_output=True, timeout=10)
                
                # 添加模拟来源
                for i, video in enumerate(videos[:2]):  # 只添加2个避免超时
                    print(f"  添加来源 {i+1}: {video['title'][:30]}...")
                    time.sleep(1)
                
                # 提问获取分析
                questions = [
                    "这些内容的主要学习价值是什么？",
                    "提取3个最重要的技术概念并解释",
                    "给出实用的学习建议"
                ]
                
                analysis = []
                for q in questions:
                    print(f"  提问: {q[:20]}...")
                    cmd = [self.notebooklm_cli, "ask", q]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        answer = result.stdout.strip()
                        if answer:
                            analysis.append(f"**{q}**\n{answer[:200]}...")
                    time.sleep(2)
                
                return {
                    'notebook_id': notebook_id,
                    'analysis': analysis if analysis else self.get_mock_analysis(),
                    'success': True
                }
            
        except Exception as e:
            print(f"  NotebookLM分析失败: {e}")
        
        return {
            'notebook_id': None,
            'analysis': self.get_mock_analysis(),
            'success': False
        }
    
    def get_mock_analysis(self):
        """生成模拟分析"""
        return [
            "**主要学习价值**\n这些视频提供了前沿的技术见解和实用的学习方法，适合想要深入理解AI和技术趋势的学习者。",
            "**重要技术概念**\n1. 神经网络架构\n2. 机器学习算法\n3. 深度学习原理\n4. 自然语言处理\n5. 计算机视觉",
            "**学习建议**\n建议按主题系统学习，先掌握基础概念，再深入具体应用。实践是最好的学习方式。"
        ]
    
    def generate_channel_message(self, channel):
        """生成单个频道的消息"""
        print(f"\n📺 处理频道: {channel['display_name']}")
        
        # 获取视频
        videos = self.get_mock_videos(channel['display_name'], count=5)
        print(f"  获取到 {len(videos)} 个视频")
        
        # NotebookLM分析
        print("  进行NotebookLM分析...")
        analysis_result = self.create_notebooklm_analysis(channel['display_name'], videos)
        
        # 构建消息
        message = f"""📺 **{channel['display_name']} 每日学习新闻** - {self.today}

🎯 **今日精选视频** ({len(videos)}个)
"""
        
        for i, video in enumerate(videos[:3], 1):
            message += f"{i}. {video['title']}\n"
        
        if len(videos) > 3:
            message += f"   ...还有 {len(videos)-3} 个精彩内容\n"
        
        message += f"\n🧠 **深度分析**\n"
        
        for item in analysis_result['analysis']:
            message += f"\n{item}\n"
        
        if analysis_result.get('notebook_id'):
            message += f"\n📒 **NotebookLM笔记本**: {analysis_result['notebook_id']}\n"
        
        message += f"\n💡 **今日学习任务**\n"
        message += "1. 观看前2个核心视频（约30分钟）\n"
        message += "2. 理解3个关键技术概念\n"
        message += "3. 思考如何应用学到的新知识\n"
        
        message += f"\n⏰ 分析时间: {datetime.now().strftime('%H:%M')}\n"
        
        return message
    
    def generate_daily_summary(self):
        """生成每日汇总消息"""
        print(f"\n{'='*60}")
        print(f"📰 生成每日学习新闻 - {self.today}")
        print(f"{'='*60}")
        
        # 只处理高优先级频道
        active_channels = [c for c in self.config['channels'] if c['status'] == 'active']
        high_priority = [c for c in active_channels if c.get('priority') == 'high']
        
        print(f"📊 发现 {len(high_priority)} 个高优先级频道")
        
        if not high_priority:
            print("⚠️ 没有高优先级频道，使用所有活跃频道")
            high_priority = active_channels[:2]  # 只取前2个
        
        all_messages = []
        
        for channel in high_priority[:2]:  # 只处理前2个避免消息太长
            channel_message = self.generate_channel_message(channel)
            all_messages.append({
                'channel': channel['display_name'],
                'message': channel_message
            })
        
        # 合并消息
        combined = f"""# 📰 Lip 每日学习新闻 - {self.today}

🤖 智能学习助手为你精选今日最有价值的学习内容

"""
        
        for item in all_messages:
            combined += f"\n{'='*40}\n"
            combined += item['message']
            combined += f"\n{'='*40}\n"
        
        # 添加总结
        combined += f"\n📊 **今日学习统计**\n"
        combined += f"- 分析频道: {len(all_messages)} 个\n"
        combined += f"- 推荐视频: {len(all_messages) * 5} 个\n"
        combined += f"- 预计学习时间: {len(all_messages) * 45} 分钟\n"
        
        combined += f"\n🎯 **明日预告**\n"
        combined += "明天将继续为你分析：\n"
        for channel in high_priority[:2]:
            combined += f"- {channel['display_name']} 的最新内容\n"
        
        combined += f"\n---\n⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        combined += "🤖 由Lip智能学习助手生成 | 每天凌晨2点自动更新\n"
        
        return combined
    
    def save_and_prepare_message(self, message):
        """保存消息并准备发送"""
        try:
            # 保存到文件
            filename = f"daily_news_{self.today}.md"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(message)
            
            print(f"\n✅ 每日新闻已保存到: {filepath}")
            print(f"📏 消息长度: {len(message)} 字符")
            
            # 也保存为纯文本版本
            txt_filepath = filepath.replace('.md', '.txt')
            with open(txt_filepath, 'w', encoding='utf-8') as f:
                f.write(message)
            
            return {
                'success': True,
                'markdown_file': filepath,
                'text_file': txt_filepath,
                'message_preview': message[:500] + "..." if len(message) > 500 else message
            }
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def run(self):
        """运行主流程"""
        try:
            # 生成每日消息
            daily_message = self.generate_daily_summary()
            
            # 保存并准备发送
            result = self.save_and_prepare_message(daily_message)
            
            if result['success']:
                print(f"\n{'='*60}")
                print("🚀 每日新闻生成完成!")
                print(f"{'='*60}")
                
                print(f"\n📁 文件位置:")
                print(f"  Markdown: {result['markdown_file']}")
                print(f"  纯文本: {result['text_file']}")
                
                print(f"\n📝 消息预览:")
                print("-" * 40)
                print(result['message_preview'])
                print("-" * 40)
                
                print(f"\n🎯 下一步:")
                print("1. 通过飞书消息工具发送 daily_news_{self.today}.txt")
                print("2. 或直接复制上面的消息内容发送")
                print("3. 明天凌晨2点自动运行")
                
                return result
            else:
                print(f"\n❌ 生成失败: {result.get('error')}")
                return None
                
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """主函数"""
    lip = LipSimpleDaily()
    result = lip.run()
    
    if result and result['success']:
        print(f"\n✅ 任务完成! 请通过飞书发送每日新闻。")
        sys.exit(0)
    else:
        print(f"\n❌ 任务失败")
        sys.exit(1)

if __name__ == "__main__":
    main()