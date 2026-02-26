#!/usr/bin/env python3
"""
修复频道ID问题，使用正确的频道ID
"""

import subprocess
import time

# 正确的频道ID映射
CORRECT_CHANNELS = {
    "The Diary Of A CEO": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 这个ID可能不对，需要查找正确ID
    "Dwarkesh Patel": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
    "No Code": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
    "Matthew Berman": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
    "Futurepedia": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
    "AI Foundations": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
    "Jack": "UCWY4H8r9hM4HlGjCk31Q_6g",  # 需要正确ID
}

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def find_channel_id(channel_name):
    """查找频道ID"""
    print(f"🔍 查找 {channel_name} 的频道ID...")
    
    # 尝试搜索YouTube
    search_url = f"https://www.youtube.com/results?search_query={channel_name.replace(' ', '+')}"
    print(f"  搜索URL: {search_url}")
    
    # 这里应该使用YouTube API或网页抓取，但暂时跳过
    return None

def test_channel_id(channel_id):
    """测试频道ID是否有效"""
    if not channel_id:
        return False
    
    try:
        import urllib.request
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        return response.status == 200
    except:
        return False

def main():
    print("🔧 修复频道ID问题")
    print("=" * 60)
    
    # 先测试已知有效的频道
    print("\n✅ 已知有效的频道:")
    valid_channels = {
        "Lex Fridman": "UCSHZKyawb77ixDdsGog4iWA",
        "Joe Rogan": "UCzQUP1qoWDoEbmsQxvdjxgQ",
        "Jordan B Peterson": "UCL_f53ZEJxp8TtlOkHwMV9Q",
    }
    
    for name, channel_id in valid_channels.items():
        if test_channel_id(channel_id):
            print(f"  ✅ {name}: {channel_id}")
        else:
            print(f"  ❌ {name}: {channel_id} (无效)")
    
    print("\n⚠️ 需要修复的频道:")
    for name in CORRECT_CHANNELS.keys():
        print(f"  ❓ {name}: 需要查找正确频道ID")
    
    print("\n🎯 解决方案:")
    print("  1. 手动查找这些频道的正确YouTube频道ID")
    print("  2. 或者使用其他内容源（播客、博客等）")
    print("  3. 或者先专注于已有内容的笔记本")
    
    print("\n📋 建议:")
    print("  ✅ 先使用Lex Fridman和Joe Rogan笔记本（已有内容）")
    print("  ✅ 未知频道笔记本也有12个视频")
    print("  🔄 其他笔记本需要正确频道ID")

if __name__ == "__main__":
    main()