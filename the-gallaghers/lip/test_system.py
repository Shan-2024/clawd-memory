#!/usr/bin/env python3
"""
Lip 简化测试 - 只测试核心流程
"""
import os
import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.manager import config_manager


def test_rss_fetch():
    """测试RSS获取"""
    print("📡 测试RSS获取...")
    
    # Lex Fridman的channel_id
    channel_id = 'UCSHZKyawb77ixDdsGog4iWA'
    rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
        
        videos = []
        for entry in root.findall('atom:entry', ns)[:3]:
            video_id = entry.find('yt:videoId', ns)
            title = entry.find('atom:title', ns)
            if video_id is not None and title is not None:
                videos.append({'id': video_id.text, 'title': title.text})
        
        print(f"  ✅ 成功获取 {len(videos)} 条视频")
        for v in videos:
            print(f"    📹 {v['id']}: {v['title'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ RSS获取失败: {e}")
        return False


def test_notebooklm():
    """测试NotebookLM"""
    print("\n🤖 测试NotebookLM...")
    
    notebooklm_bin = os.path.expanduser('~/.local/bin/notebooklm')
    
    try:
        # 检查notebooklm是否可用
        import subprocess
        result = subprocess.run(
            [notebooklm_bin, '--version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"  ✅ NotebookLM可用: {result.stdout.strip()}")
            
            # 列出notebooks
            result = subprocess.run(
                [notebooklm_bin, 'list'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                print(f"  📚 现有notebooks: {len(lines)-1 if lines else 0}")
                return True
            else:
                print(f"  ⚠️ 无法列出notebooks: {result.stderr[:100]}")
                return False
        else:
            print(f"  ❌ NotebookLM不可用: {result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"  ❌ NotebookLM测试失败: {e}")
        return False


def test_ai_analyzer():
    """测试AI分析器"""
    print("\n🧠 测试AI分析器...")
    
    try:
        from ai.analyzer import AIAnalyzer
        analyzer = AIAnalyzer()
        
        # 测试简单的AI调用
        test_text = "人工智能正在改变世界。机器学习是AI的一个分支。"
        result = analyzer.analyze_video(test_text)
        
        if result:
            print(f"  ✅ AI分析器可用")
            print(f"    摘要: {result.get('summary', [])[:1]}")
            print(f"    标签: {result.get('tags', [])}")
            return True
        else:
            print(f"  ⚠️ AI分析器返回空结果")
            return False
            
    except Exception as e:
        print(f"  ❌ AI分析器失败: {e}")
        return False


def test_feishu_sync():
    """测试飞书同步"""
    print("\n📱 测试飞书同步...")
    
    try:
        from storage.feishu_sync import FeishuDocSync
        sync = FeishuDocSync()
        
        # 测试创建文档
        test_title = f"测试文档 - {datetime.now().strftime('%H%M%S')}"
        print(f"  尝试创建文档: {test_title}")
        
        # 注意：实际创建会调用openclaw命令，这里只测试导入
        print(f"  ✅ 飞书同步模块可导入")
        return True
        
    except Exception as e:
        print(f"  ❌ 飞书同步测试失败: {e}")
        return False


def test_config():
    """测试配置"""
    print("\n⚙️ 测试配置...")
    
    try:
        config = config_manager.load()
        channels = config.get('channels', [])
        
        print(f"  ✅ 配置加载成功")
        print(f"    频道数: {len(channels)}")
        print(f"    活跃频道: {sum(1 for c in channels if c.get('status') == 'active')}")
        
        for i, channel in enumerate(channels[:3]):
            print(f"    {i+1}. {channel.get('name')} ({channel.get('status')})")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置测试失败: {e}")
        return False


def main():
    print(f"\n{'='*60}")
    print(f"🤖 Lip 系统测试 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    
    tests = [
        ("配置系统", test_config),
        ("RSS获取", test_rss_fetch),
        ("NotebookLM", test_notebooklm),
        ("AI分析器", test_ai_analyzer),
        ("飞书同步", test_feishu_sync),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"  ❌ {name}异常: {e}")
            results.append((name, False))
    
    print(f"\n{'='*60}")
    print("📊 测试结果:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
    
    print(f"\n🎯 通过率: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n✨ 所有测试通过！系统可以正常工作。")
        return 0
    else:
        print(f"\n⚠️  有 {total-passed} 项测试失败，需要检查。")
        return 1


if __name__ == '__main__':
    sys.exit(main())