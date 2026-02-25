#!/usr/bin/env python3
"""
Lip 系统测试脚本
"""
import os
import sys
import json

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager
from youtube.parser import YouTubeURLParser
from ai.analyzer import AIAnalyzer
from storage.local import LocalStorage
from feishu.bot import process_message


def test_config_manager():
    """测试配置管理"""
    print("🧪 测试配置管理...")
    
    # 测试添加频道
    channel = config_manager.add_channel(
        url="https://www.youtube.com/@testchannel",
        name="@testchannel",
        display_name="测试频道"
    )
    
    print(f"✅ 添加频道: {channel['name']}")
    
    # 测试获取频道
    channels = config_manager.get_all_channels()
    print(f"✅ 获取频道列表: {len(channels)} 个")
    
    # 测试更新统计
    config_manager.update_channel_stats("@testchannel", total_videos=100)
    print("✅ 更新频道统计")
    
    # 测试保存配置
    config_manager.save()
    print("✅ 保存配置")
    
    return True


def test_url_parser():
    """测试URL解析"""
    print("\n🧪 测试URL解析...")
    
    parser = YouTubeURLParser()
    
    test_urls = [
        "https://www.youtube.com/@testuser",
        "https://www.youtube.com/channel/UC123456789",
        "https://www.youtube.com/c/CustomName",
        "https://www.youtube.com/watch?v=abc123",
        "https://youtu.be/abc123",
    ]
    
    for url in test_urls:
        parsed = parser.parse(url)
        print(f"  {url}")
        print(f"    → 类型: {parsed['type']}, ID: {parsed['id']}")
    
    return True


def test_ai_analyzer():
    """测试AI分析"""
    print("\n🧪 测试AI分析...")
    
    analyzer = AIAnalyzer()
    
    # 测试文本
    test_transcript = """
    今天我们来聊聊人工智能的发展。人工智能是计算机科学的一个分支，它试图让机器模拟人类的智能。
    机器学习是人工智能的一种方法，它让计算机从数据中学习规律。深度学习是机器学习的一个子领域，
    它使用多层神经网络来处理复杂的数据。
    """
    
    # 测试摘要生成
    summary = analyzer.generate_summary(test_transcript)
    print(f"✅ 摘要生成: {len(summary)} 条")
    for i, point in enumerate(summary):
        print(f"  {i+1}. {point}")
    
    # 测试标签生成
    tags = analyzer.generate_tags(test_transcript)
    print(f"✅ 标签生成: {tags}")
    
    # 测试知识提取
    knowledge = analyzer.extract_knowledge(test_transcript)
    print(f"✅ 知识提取: {len(knowledge)} 个名词")
    for name, explanation in knowledge.items():
        print(f"  - {name}: {explanation[:50]}...")
    
    return True


def test_storage():
    """测试存储"""
    print("\n🧪 测试存储...")
    
    storage = LocalStorage()
    
    # 测试保存笔记
    video_info = {
        'id': 'test123',
        'title': '测试视频标题',
        'uploader': '测试博主',
        'duration': 600,
        'upload_date': '20250115'
    }
    
    analysis = {
        'summary': ['要点1', '要点2', '要点3'],
        'tags': ['测试', 'AI', '教程'],
        'knowledge': {'人工智能': '计算机科学的一个分支'}
    }
    
    transcript = "这是测试视频的字幕内容..."
    
    filepath = storage.save_note("@testchannel", video_info, analysis, transcript)
    print(f"✅ 保存笔记: {filepath}")
    
    # 测试获取笔记列表
    notes = storage.get_notes()
    print(f"✅ 获取笔记列表: {len(notes)} 条")
    
    # 测试获取知识词典
    knowledge = storage.get_knowledge_dict()
    print(f"✅ 获取知识词典: {len(knowledge)} 条")
    
    return True


def test_feishu_bot():
    """测试飞书机器人"""
    print("\n🧪 测试飞书机器人...")
    
    # 测试帮助命令
    response = process_message("帮助")
    print(f"✅ 帮助命令: {response[:50]}...")
    
    # 测试状态命令
    response = process_message("状态")
    print(f"✅ 状态命令: {response[:50]}...")
    
    # 测试添加命令（模拟）
    response = process_message("添加博主 https://www.youtube.com/@test")
    print(f"✅ 添加命令: {response[:50]}...")
    
    return True


def main():
    """主测试函数"""
    print("🚀 Lip 智能学习助手 - 系统测试")
    print("=" * 60)
    
    try:
        test_config_manager()
        test_url_parser()
        test_ai_analyzer()
        test_storage()
        test_feishu_bot()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！系统基本功能正常。")
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 测试YouTube提取: 需要yt-dlp")
        print("3. 配置OpenClaw定时任务")
        print("4. 在飞书中测试实际命令")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())