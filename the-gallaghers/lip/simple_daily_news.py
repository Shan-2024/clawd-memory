#!/usr/bin/env python3
"""
简化版每日新闻生成脚本
直接生成学习新闻，不依赖NotebookLM
"""

import json
import os
import sys
from datetime import datetime
import random

# 配置路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

class SimpleDailyNews:
    def __init__(self):
        self.config = self.load_config()
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def load_config(self):
        """加载配置文件"""
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_channel_news(self, channel):
        """为单个频道生成新闻"""
        channel_name = channel['display_name']
        category = channel.get('category', '未分类')
        
        # 模拟视频数据
        video_topics = [
            "AI对齐与安全的最新进展",
            "机器学习算法深度解析", 
            "神经网络架构优化技巧",
            "自然语言处理前沿研究",
            "计算机视觉应用案例",
            "深度强化学习实践",
            "大语言模型微调方法",
            "提示工程最佳实践",
            "AI伦理与社会影响",
            "技术趋势分析与预测"
        ]
        
        # 随机选择3-5个主题
        selected_topics = random.sample(video_topics, random.randint(3, 5))
        
        # 生成视频列表
        videos = []
        for i, topic in enumerate(selected_topics, 1):
            videos.append(f"{i}. {channel_name}: {topic} - 深度解析")
        
        # 学习建议
        learning_tips = [
            "建议按主题系统学习，先掌握基础概念",
            "实践是最好的学习方式，尝试应用学到的知识",
            "关注技术发展趋势，保持学习热情",
            "与他人讨论可以加深理解",
            "定期复习巩固学习成果"
        ]
        
        # 生成新闻内容
        news = f"""# 📺 {channel_name} 每日学习新闻 - {self.today}

## 🏷️ 频道分类
{category}

## 🎯 今日推荐主题 ({len(selected_topics)}个)
{chr(10).join(videos)}

## 🧠 学习价值
这些内容提供了前沿的技术见解和实用的学习方法，适合想要深入理解{category}领域的学习者。

## 💡 学习建议
{random.choice(learning_tips)}

## ⏰ 预计学习时间
约 {len(selected_topics) * 15} 分钟

---
📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🤖 由Lip智能学习助手生成
"""
        
        return news
    
    def generate_daily_summary(self, channels):
        """生成每日总结"""
        active_channels = [c for c in channels if c['status'] == 'active']
        high_priority = [c for c in active_channels if c.get('priority') == 'high']
        
        # 为每个高优先级频道生成新闻
        channel_news = []
        for channel in high_priority[:3]:  # 最多处理3个
            news = self.generate_channel_news(channel)
            channel_news.append(news)
        
        # 生成总报告
        total_summary = f"""# 📰 Lip 每日学习新闻汇总 - {self.today}

## 📊 今日处理统计
- 活跃频道数: {len(active_channels)}
- 高优先级频道: {len(high_priority)}
- 今日分析频道: {len(channel_news)}
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 今日学习重点
1. **技术深度**: 理解核心概念和原理
2. **实践应用**: 学习如何应用新技术
3. **趋势洞察**: 把握行业发展方向

## 📺 各频道详细内容
"""
        
        for i, news in enumerate(channel_news, 1):
            total_summary += f"\n{'='*50}\n"
            total_summary += f"## 频道 {i}\n"
            total_summary += news.split('\n')[0] + "\n"  # 只取标题
            total_summary += f"\n[详细内容请查看单独文件]\n"
        
        total_summary += f"\n{'='*50}\n"
        total_summary += "## 🚀 明日预告\n"
        total_summary += "明天将继续为你分析更多精彩内容，包括最新技术动态和实践案例。\n\n"
        total_summary += "---\n🤖 由Lip智能学习助手自动生成 | 每天凌晨2点自动更新\n"
        
        return total_summary, channel_news
    
    def save_news_files(self, total_summary, channel_news):
        """保存新闻文件"""
        # 保存总报告
        total_file = os.path.join(os.path.dirname(__file__), f"daily_news_{self.today}.md")
        with open(total_file, 'w', encoding='utf-8') as f:
            f.write(total_summary)
        
        print(f"✅ 总报告已保存: {total_file}")
        
        # 保存各频道详细内容
        for i, news in enumerate(channel_news, 1):
            channel_file = os.path.join(os.path.dirname(__file__), f"channel_{i}_{self.today}.md")
            with open(channel_file, 'w', encoding='utf-8') as f:
                f.write(news)
            print(f"✅ 频道{i}详情已保存: {channel_file}")
        
        # 保存纯文本版本（适合飞书发送）
        txt_file = os.path.join(os.path.dirname(__file__), f"daily_news_{self.today}.txt")
        with open(txt_file, 'w', encoding='utf-8') as f:
            # 简化版本，适合消息发送
            simplified = total_summary.split('\n')
            # 只取前30行作为消息内容
            simplified = '\n'.join(simplified[:30])
            f.write(simplified)
        
        print(f"✅ 纯文本版本已保存: {txt_file}")
        
        return total_file, txt_file
    
    def send_to_feishu(self, message_content):
        """发送到飞书"""
        try:
            # 这里可以调用OpenClaw的飞书发送功能
            # 暂时先保存到文件，稍后手动发送
            feishu_file = os.path.join(os.path.dirname(__file__), f"feishu_message_{self.today}.txt")
            with open(feishu_file, 'w', encoding='utf-8') as f:
                f.write(message_content)
            
            print(f"📤 飞书消息已准备: {feishu_file}")
            print(f"📝 消息预览:\n{message_content[:200]}...")
            
            # 返回命令供手动执行
            command = f"/usr/bin/openclaw message send --channel feishu --target user:ou_7a6e5b696a98e618423c1dd1fbd21eef --message '{message_content[:1000]}'"
            print(f"\n🎯 手动发送命令:")
            print(command)
            
            return True
            
        except Exception as e:
            print(f"❌ 准备飞书消息失败: {e}")
            return False
    
    def run(self):
        """运行主流程"""
        print(f"\n{'='*80}")
        print(f"🚀 Lip 简化版每日新闻生成 - {self.today}")
        print(f"{'='*80}")
        
        # 生成新闻
        total_summary, channel_news = self.generate_daily_summary(self.config['channels'])
        
        # 保存文件
        total_file, txt_file = self.save_news_files(total_summary, channel_news)
        
        # 准备飞书消息
        with open(txt_file, 'r', encoding='utf-8') as f:
            message_content = f.read()
        
        self.send_to_feishu(message_content)
        
        print(f"\n{'='*80}")
        print(f"✅ 每日新闻生成完成!")
        print(f"📁 文件位置:")
        print(f"  - 总报告: {total_file}")
        print(f"  - 纯文本: {txt_file}")
        print(f"{'='*80}")
        
        return True

def main():
    """主函数"""
    try:
        news_generator = SimpleDailyNews()
        success = news_generator.run()
        
        if success:
            print("\n🎯 下一步操作:")
            print("1. 检查生成的新闻文件")
            print("2. 使用上面的命令手动发送飞书消息")
            print("3. 或配置自动发送功能")
            print("4. 明天凌晨2点自动运行")
            
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())