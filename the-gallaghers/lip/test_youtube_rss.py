#!/usr/bin/env python3
"""
测试YouTube RSS解析
"""

import feedparser
import sys

def test_channel_rss(channel_url):
    """测试频道RSS解析"""
    print(f"\n测试频道: {channel_url}")
    
    # 尝试不同的RSS格式
    rss_formats = [
        # 格式1: 标准频道ID
        f"https://www.youtube.com/feeds/videos.xml?channel_id=UCvixJtaXuNdMPUGdOPcY8Ag",  # Lex Fridman
        # 格式2: 用户handle
        "https://www.youtube.com/feeds/videos.xml?user=lexfridman",
        # 格式3: 频道名称
        "https://www.youtube.com/feeds/videos.xml?channel_name=LexFridman",
    ]
    
    for i, rss_url in enumerate(rss_formats, 1):
        print(f"\n尝试格式 {i}: {rss_url}")
        try:
            feed = feedparser.parse(rss_url)
            print(f"  状态: {feed.status}")
            print(f"  条目数: {len(feed.entries)}")
            
            if feed.entries:
                print(f"  第一个视频标题: {feed.entries[0].title}")
                print(f"  第一个视频链接: {feed.entries[0].link}")
            else:
                print("  没有找到视频条目")
                
        except Exception as e:
            print(f"  错误: {e}")

def main():
    """主函数"""
    print("测试YouTube RSS解析")
    print("=" * 50)
    
    # 测试几个频道
    channels = [
        "https://www.youtube.com/@lexfridman",
        "https://www.youtube.com/@JordanBPeterson",
        "https://www.youtube.com/@joerogan",
    ]
    
    for channel in channels:
        test_channel_rss(channel)
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()