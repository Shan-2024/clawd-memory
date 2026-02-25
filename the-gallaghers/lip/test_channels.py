#!/usr/bin/env python3
"""
测试新添加的YouTube频道
"""

import json
import os
from datetime import datetime

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_channel_summary():
    """打印频道摘要"""
    config = load_config()
    
    print("=" * 80)
    print("📺 Lip系统 - YouTube频道监控列表")
    print("=" * 80)
    
    # 统计信息
    active_channels = [c for c in config['channels'] if c['status'] == 'active']
    inactive_channels = [c for c in config['channels'] if c['status'] == 'inactive']
    
    print(f"\n📊 统计信息:")
    print(f"  总频道数: {len(config['channels'])}")
    print(f"  活跃频道: {len(active_channels)}")
    print(f"  非活跃频道: {len(inactive_channels)}")
    print(f"  每日限制: {config['daily_limit_per_channel']} 视频/频道")
    print(f"  定时任务: {config['settings']['cron_schedule']}")
    
    # 按分类显示
    print(f"\n🎯 频道分类:")
    categories = {}
    for channel in active_channels:
        cat = channel.get('category', '未分类')
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in categories.items():
        print(f"  {cat}: {count}个频道")
    
    # 详细列表
    print(f"\n📋 活跃频道列表:")
    for i, channel in enumerate(active_channels, 1):
        priority_emoji = {
            'high': '🔥',
            'medium': '⭐',
            'low': '📌'
        }.get(channel.get('priority', 'low'), '📌')
        
        sync_emoji = '📝' if channel.get('sync_to_feishu', False) else '📄'
        
        print(f"\n  {i}. {priority_emoji} {channel['display_name']}")
        print(f"     类别: {channel.get('category', '未分类')}")
        print(f"     优先级: {channel.get('priority', 'low')}")
        print(f"     飞书同步: {sync_emoji} {'是' if channel.get('sync_to_feishu', False) else '否'}")
        print(f"     已分析视频: {channel['stats']['analyzed_count']}")
        print(f"     URL: {channel['url']}")
    
    print(f"\n⏰ 定时任务详情:")
    print(f"  下次运行: 每天凌晨2点 (北京时间)")
    print(f"  工作目录: {os.path.dirname(__file__)}")
    print(f"  命令: /usr/bin/python3 lip_workflow.py")
    print(f"  日志文件: /tmp/lip_workflow.log")
    
    print(f"\n🎯 今晚2点将处理:")
    print(f"  1. 检查所有活跃频道的新视频")
    print(f"  2. 每个频道最多处理{config['daily_limit_per_channel']}个视频")
    print(f"  3. 生成NotebookLM级别的学习笔记")
    print(f"  4. 自动同步到飞书文档")
    print(f"  5. 记录日志到 /tmp/lip_workflow.log")
    
    print(f"\n📝 飞书文档:")
    for channel in active_channels:
        if channel.get('feishu_doc_token'):
            print(f"  {channel['display_name']}: https://feishu.cn/docx/{channel['feishu_doc_token']}")

if __name__ == "__main__":
    print_channel_summary()